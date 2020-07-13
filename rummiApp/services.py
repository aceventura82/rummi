from django.conf import settings


def sendPin(request, mail=False):
    import random
    from django.utils.translation import gettext as _
    pin = random.randint(10000, 99999)
    logger('errors', "PIN:" + str(pin))
    msg = _("PinMessage").replace('%%PIN%%', str(pin))
    request.session['userpin'] = str(pin)
    email = request.POST.get('email', False)
    sendMail([email], _('PinSubject'), msg)


def sendMail(dest, subject, body, fromEmail=(settings.FROMEMAIL)):
    from django.core.mail import EmailMessage
    email = EmailMessage(subject, body, from_email=fromEmail, to=dest)
    email.content_subtype = "html"
    email.send()


def logger(file, message):
    import datetime
    import pytz
    handle1 = open(settings.BASE_DIR + '/rummiApp/logs/' + file + '_' + pytz.timezone('America/Bogota').localize(datetime.datetime.now()).strftime("%Y-%m-%d") + '.log', 'a')
    handle1.write(pytz.timezone('America/Bogota').localize(datetime.datetime.now()).strftime("%H:%M:%S") + "|" + message + "\n")
    handle1.close()


def runnig(oper, daemon, delF=False):
    import os
    path = settings.LOCKFILEPATH + ".rummi" + oper + "_" + str(daemon)
    if delF:
        os.remove(path)
    elif os.path.exists(path):
        return -1
    else:
        with open(path, 'a'):
            os.utime(path, None)
    return 0


def fileUpload(request, pk, field):
    if field == 'avatar':
        path = 'playerAvatars/'
    elif field == 'audio':
        path = 'audios/'
    else:
        return
    request.session['msg'] = 'ELSE'
    if request.FILES and request.FILES[field]:
        import os
        from django.core.files.storage import FileSystemStorage
        file = request.FILES[field]
        filename, file_extension = os.path.splitext(file.name)
        from django.utils.translation import gettext as _
        if field == 'avatar' and file_extension not in ".jpg,.png,.jpeg,.gif":
            request.session['msg'] = _('FileExtError')
        elif field == 'audio' and file_extension not in ".3gp":
            request.session['msg'] = _('DataError')
        elif file.size > 5024000:
            request.session['msg'] = _('FileSizeError')
        else:
            fs = FileSystemStorage()
            deleteFile(pk, field)
            fs.save(os.path.join(settings.BASE_DIR, 'static/' + path + str(pk) + file_extension), file)
            request.session['msg'] = 'OK'


def deleteFile(pk, field):
    if field == 'audio':
        path = 'audios/'
    elif field == 'avatar':
        path = 'playerAvatars/'
    else:
        return
    import os
    for ext in {'.png', '.jpg', '.jpeg', '.gif', '.3gp'}:
        if os.path.exists(os.path.join(settings.BASE_DIR, 'static/' + path + str(pk) + ext)):
            os.remove(os.path.join(settings.BASE_DIR, 'static/' + path + str(pk) + ext))
