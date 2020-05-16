from django.shortcuts import render, redirect
from django.conf import settings
from .services import logger
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, "index.html")


def Err(request, context):
    if request.user.is_staff:
        return render(request, "404.html", context)
    return render(request, "404.html", context)


def testing(request):
    return render(request, "index.html")


def changelang(request, lang):
    try:
        request.session['languages'] = settings.LANGUAGES
        langsS = dict(settings.LANGUAGES)
        if lang in langsS:
            from django.utils import translation
            translation.activate(lang)
            request.session[translation.LANGUAGE_SESSION_KEY] = lang
            request.session['lang'] = lang
        try:
            return redirect(request.META['HTTP_REFERER'])
        except Exception:
            return redirect('/')
    except Exception as ex:
        logger("errors", str(ex))
        return Err(request, {'msg': str(ex)})


class APIViews():

    def login(request):
        from django.http import HttpResponse
        if not APIViews.valApiKey(request.POST.get('apiKey', '')) and request.META.get("REMOTE_ADDR", "") != "199.167.148.17":
            return HttpResponse("ERR")
        from .players import loginUserPass
        context = loginUserPass(request)
        if 'auth' in context:
            return HttpResponse(context['auth']+"|"+request.user.password)
        else:
            return HttpResponse(context['msg'])

    def valApiKey(key, user=""):
        from .players import getUserHash
        import hmac
        import hashlib
        import pytz
        append = ""
        if user != "":
            append = getUserHash(user)
        salt = bytes('OYG7)Of*lW-zVSy=winnSM=1OZGbW0(u', 'utf-8')
        import datetime
        t1 = pytz.timezone('America/Bogota').localize(datetime.datetime.now() - datetime.timedelta(minutes=1)).strftime("%Y%m%d%H%M")+append
        t2 = pytz.timezone('America/Bogota').localize(datetime.datetime.now()).strftime("%Y%m%d%H%M")+append
        t3 = pytz.timezone('America/Bogota').localize(datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%Y%m%d%H%M")+append
        dig1 = hmac.new(salt, bytes(t1, 'utf-8'), hashlib.sha256).hexdigest()
        dig2 = hmac.new(salt, bytes(t2, 'utf-8'), hashlib.sha256).hexdigest()
        dig3 = hmac.new(salt, bytes(t3, 'utf-8'), hashlib.sha256).hexdigest()
        if key == dig1 or key == dig2 or key == dig3:
            return True
        return False

    @csrf_exempt
    def getData(request):
        try:
            from django.http import HttpResponse
            oper = request.POST.get('oper', '')
            publicAccess = "tournaments,teams,login"
            # Set Language
            APIViews.lang(request)
            # check API Key for Non public Opers
            if oper not in publicAccess:
                from .players import loginUserRequestsApp
                # Validate application Key
                if not APIViews.valApiKey(request.POST.get('apiKey', ''), request.POST.get('usernameUser', '')) and request.META.get("REMOTE_ADDR", "") != "199.167.148.17":
                    return HttpResponse("No Access")
                # create user for current request
                user = loginUserRequestsApp(request)
                # check User Still Exist and Active
                try:
                    user.id
                except Exception:
                    return HttpResponse(str(user)+"123")
            # get data
            return HttpResponse(getattr(APIViews, oper)(request))
        except Exception as ex:
            logger("errors", str(ex))
            return HttpResponse("--")

    def lang(request):
        lang = request.POST.get('lang', 'es')
        from django.utils import translation
        translation.activate(lang)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang

    def dataToJSON(dataORG, append=''):
        result = ''
        for data in dataORG:
            result += '{'
            for attr, value in data.__dict__.items():
                if attr == '_state':
                    continue
                elif ","+attr in ',date,startDate,endDate':
                    import datetime
                    import pytz
                    dd = pytz.timezone('America/Bogota').localize(datetime.datetime.strptime(str(value)[0:19], '%Y-%m-%d %H:%M:%S')) + datetime.timedelta(hours=-5)
                    result += '"'+append+attr+'":"'+APIViews.valValue(str(dd.strftime('%Y-%m-%d %H:%M:%S')))+'",'
                else:
                    result += '"'+append+attr+'":"'+APIViews.valValue(str(value))+'",'
            result = result[:-1] + '}\n'
        return result

    def valValue(data):
        return "" if data is None or data == "None" else str(data)
