from django.conf import settings


def sendPin(request, mail=False):
    import random
    from django.utils.translation import gettext as _
    pin = random.randint(10000, 99999)
    logger('tmp', "PIN:" + str(pin))
    from cryptography.fernet import Fernet
    data = Fernet('RlHONeOuUGIzxLrCRzvCf3RMNxuNIyVATrBRpX5cEAU=').encrypt(str.encode(request.session.get('user_email', '') + "&" + request.session.get('user_pass', '')))
    msg = _("PinMessage").replace('%(pin)', str(pin)).replace('%(url)', 'http://' + request.META['HTTP_HOST'] + '/?q=' + data.decode("utf-8"))
    request.session['userpin'] = str(pin)
    email = request.POST.get('email', False)
    sendMail([email], _('PinSubject'), msg + " " + str(pin))


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
    if field == 'shield':
        path = 'teamShields/'
    elif field == 'avatar':
        path = 'playerAvatars/'
    elif field == 'tournamentLogo':
        path = 'tournament/'
    else:
        return
    if request.FILES and request.FILES[field]:
        import os
        from django.core.files.storage import FileSystemStorage
        file = request.FILES[field]
        filename, file_extension = os.path.splitext(file.name)
        from django.utils.translation import gettext as _
        if not file.name.endswith('.png') and not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.gif'):
            request.session['msg'] = _('FileExtError')
        elif file.size > 5024000:
            request.session['msg'] = _('FileSizeError')
        else:
            fs = FileSystemStorage()
            deleteFile(request, pk, field)
            fs.save(os.path.join(settings.BASE_DIR, 'static/' + path + str(pk) + file_extension), file)


def deleteFile(request, pk, field):
    if field == 'shield':
        path = 'teamShields/'
    elif field == 'avatar':
        path = 'playerAvatars/'
    elif field == 'tournamentLogo':
        path = 'tournament/'
    else:
        return
    import os
    for ext in {'.png', '.jpg', '.jpeg', '.gif'}:
        if os.path.exists(os.path.join(settings.BASE_DIR, 'static/' + path + str(pk) + ext)):
            os.remove(os.path.join(settings.BASE_DIR, 'static/' + path + str(pk) + ext))
