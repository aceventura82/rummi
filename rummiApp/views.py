from django.shortcuts import render, redirect
from django.conf import settings
from .services import logger
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import gettext as _


def index(request):
    return render(request, "index.html")


def Err(request, context):
    if request.user.is_staff:
        return render(request, "404.html", context)
    return render(request, "404.html", context)


def checkMsg(request, context):
    if request.session.get('msg', False):
        context['msg'] = request.session.get('msg', '')
    if request.session.get('msg1', False):
        context['msg'] += request.session.get('msg1', '')
    request.session['msg1'] = None
    request.session['msg'] = None
    return context


@csrf_exempt
def testing(request):
    from django.http import HttpResponse
    from .games import viewMyGames
    data = viewMyGames(request.POST.get("userId"))
    result = ""
    for dato in data:
        if "," + str(dato.gameId.id) + "," not in request.POST.get("ignore", ""):
            result += APIViews.dataToJSON([dato.gameId])
    return HttpResponse(result)


def joinGame(request, code):
    return render(request, "open_in_app.html")


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


class PlayerAdminViews():

    @staff_member_required(login_url='login')
    def playersIndex(request):
        try:
            context = {}
            if request.POST.get('searchBT', False):
                from .players import listPlayers
                context = listPlayers(request)
            else:
                request.session['criteria'] = ''
            context = checkMsg(request, context)
            return render(request, "admin/player/home.html", context)
        except Exception as ex:
            logger("errors", str(ex))
            return Err(request, {'msg': str(ex)})

    @staff_member_required(login_url='login')
    def playersDetails(request, userId):
        try:
            if request.POST.get('editBT', False):
                from .players import editPlayer
                editPlayer(request, True)
            elif request.POST.get('notifBT', False):
                from .notifications import newNotifMsg
                newNotifMsg(request)
            elif request.POST.get('deleteBT', False):
                from .services import deleteFile
                from .players import editPlayer
                deleteFile(request, userId, 'avatar')
                editPlayer(request, True)
            try:
                from .players import detailsPlayer
                context = detailsPlayer(userId)
            except Http404:
                request.session['msg'] = _('UserNotFound')
                return redirect('/' + settings.ADMIN_URL + "player/")
            context['status'] = "checked"
            if context['data'].status != '1':
                context['status'] = ""
            context = checkMsg(request, context)
            return render(request, "admin/player/details.html", context)
        except Exception as ex:
            logger("errors", str(ex))
            return Err(request, {'msg': str(ex)})


class APIViews():

    def login(request):
        from django.http import HttpResponse
        if not APIViews.valApiKey(request.POST.get('apiKey', '')) and request.META.get("REMOTE_ADDR", "") != "186.85.5.164":
            return HttpResponse('--')
        from .players import loginUserPass
        context = loginUserPass(request)
        if 'auth' in context:
            return HttpResponse(context['auth'] + "|" + request.user.password)
        else:
            return HttpResponse(context['msg'])

    def register(request):
        from django.http import HttpResponse
        if not APIViews.valApiKey(request.POST.get('apiKey', '')) and request.META.get("REMOTE_ADDR", "") != "186.85.5.164":
            return HttpResponse('--')
        from .players import registerUser
        from .models import tmpPIN
        if request.POST.get('valEmailBT', '') != '':
            try:
                request.session['userpin'] = tmpPIN.objects.filter(email=request.POST.get('email', '-1')).order_by('id')[0].pin
            except Exception as ex:
                request.session['userpin'] = str(ex)
        context = registerUser(request)
        if context['value'] == 'registered':
            return HttpResponse("1|" + context['msg'])
        if context['value'] == 'sent' and context['msg'] == _('PINSent'):
            return HttpResponse("1|" + context['msg'])
        if context['value'] == 'registered':
            return HttpResponse(context['msg'])
        else:
            return HttpResponse(context['msg'])

    def errors(request):
        from django.http import HttpResponse
        logger("users_errors", str(request.POST.get("data")))
        HttpResponse("OK")

    def valApiKey(key, user=""):
        return True
        from .players import getUserHash
        from django.conf import settings
        import hmac
        import hashlib
        import datetime
        import pytz
        append = ""
        if user != "":
            append = getUserHash(user)
        salt = bytes(settings.APIKEY, 'utf-8')
        t1 = pytz.timezone('America/Bogota').localize(datetime.datetime.now() - datetime.timedelta(minutes=1)).strftime("%Y%m%d%H%M") + append
        t2 = pytz.timezone('America/Bogota').localize(datetime.datetime.now()).strftime("%Y%m%d%H%M") + append
        t3 = pytz.timezone('America/Bogota').localize(datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%Y%m%d%H%M") + append
        dig1 = hmac.new(salt, bytes(t1, 'utf-8'), hashlib.sha256).hexdigest()
        dig2 = hmac.new(salt, bytes(t2, 'utf-8'), hashlib.sha256).hexdigest()
        dig3 = hmac.new(salt, bytes(t3, 'utf-8'), hashlib.sha256).hexdigest()
        if key == dig1 or key == dig2 or key == dig3:
            return True
        return False

    @csrf_exempt
    def getData(request):
        logger("errors", str(request.POST))
        try:
            from django.http import HttpResponse
            oper = request.POST.get('oper', '')
            publicAccess = "login,register,errors,checkVersion,sendEmailPass,updPasswordCode"
            # Set Language
            APIViews.lang(request)
            # check API Key for Non public Opers
            if oper not in publicAccess:
                from .players import loginUserRequestsApp
                # Validate application Key
                if request.POST.get('usernameUser', '') == '':
                    return HttpResponse("No Access")
                if not APIViews.valApiKey(request.POST.get('apiKey', ''), request.POST.get('usernameUser', '')):
                    return HttpResponse("No Access")
                # create user for current request
                user = loginUserRequestsApp(request)
                # check User Still Exist and Active
                try:
                    user.id
                except Exception as ex:
                    return HttpResponse('--'+str(ex))
            # get data
            return HttpResponse(getattr(APIViews, oper)(request))
        except Exception as ex:
            return HttpResponse('--'+str(ex))

    def checkVersion(request):
        from django.http import HttpResponse
        version = request.POST.get("version", "")
        f = open(settings.BASE_DIR + '/rummiApp/logs/version.log', 'r')
        curVer = float(f.read().rstrip())
        if version != "" and float(version) > curVer:
            w = open(settings.BASE_DIR + '/rummiApp/logs/version.log', 'w')
            w.write(version)
        elif version != "" and float(version) < curVer:
            return HttpResponse(str(curVer))
        return HttpResponse("OK")

    def bundleData(request):
        from .models import Player
        from django.shortcuts import get_object_or_404
        import datetime
        import pytz
        if request.POST.get("update_date", "") != "":
            dd = pytz.timezone('UTC').localize(datetime.datetime.strptime(request.POST.get("update_date"), '%Y-%m-%d %H:%M:%S'))
            if get_object_or_404(Player, userId=request.user.id).update_date <= dd:
                return 'OK'
        res = APIViews.gameDetailInfo(request)
        res += '{"messages":1}\n'
        res += APIViews.getMessages(request)
        res += '{"flow":1}\n'
        return res + APIViews.getFlow(request)

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
                elif "," + attr in ',date,startDate,endDate':
                    import datetime
                    import pytz
                    dd = pytz.timezone('America/Bogota').localize(datetime.datetime.strptime(str(value)[0:19], '%Y-%m-%d %H:%M:%S')) + datetime.timedelta(hours=-5)
                    result += '"' + append + attr + '":"' + APIViews.valValue(str(dd.strftime('%Y-%m-%d %H:%M:%S'))) + '",'
                else:
                    result += '"' + append + attr + '":"' + APIViews.valValue(str(value)) + '",'
            result = result[:-1] + '}\n'
        return result

    def valValue(data):
        return "" if data is None or data == "None" else str(data)

    @login_required
    def addGame(request):
        from .games import addGame
        return addGame(request)

    @login_required
    def editGame(request):
        from .games import editGame
        return editGame(request)

    @login_required
    def hideGame(request):
        from .games import hideGame
        return hideGame(request)

    @login_required
    def startGame(request):
        from .games import startGame
        return startGame(request)

    @login_required
    def deleteGame(request):
        from .games import deleteGame
        return deleteGame(request)

    @login_required
    def joinGame(request):
        from .games import joinGame
        return joinGame(request)

    @login_required
    def leaveGame(request):
        from .games import leaveGame
        return leaveGame(request)

    @login_required
    def dealCards(request):
        from .games import dealCards
        return dealCards(request)

    @login_required
    def pickCard(request):
        from .games import pickCard
        return pickCard(request)

    @login_required
    def cardsOrder(request):
        from .games import cardsOrder
        return cardsOrder(request)

    @login_required
    def discardCard(request):
        from .games import discardCard
        return discardCard(request)

    @login_required
    def draw(request):
        from .games import draw
        return draw(request)

    @login_required
    def drawOver(request):
        from .games import drawOver
        return drawOver(request)

    @login_required
    def gameInfo(request):
        from .games import viewGame
        return APIViews.dataToJSON([viewGame(request.POST.get('gameId'))])

    @login_required
    def gameInfoCode(request):
        from .games import viewGameCode
        return APIViews.dataToJSON([viewGameCode(request.POST.get('code'))])

    @login_required
    def viewMyGames(request):
        from .games import viewMyGames
        data = viewMyGames(request.user.id)
        result = ""
        for dato in data:
            result += APIViews.dataToJSON([dato.gameId])
        return result

    @login_required
    def myTurn(request):
        from .games import myTurn
        return myTurn(request.user.id)

    @login_required
    def gameDetailInfo(request):
        from .games import detailsGameInfo
        from .models import Player
        from django.shortcuts import get_object_or_404
        data = detailsGameInfo(request.POST.get('gameId'), request.user.id)
        result = ""
        for dato in data:
            result += APIViews.dataToJSON([dato.gameId])[:-2] + ","
            result += APIViews.dataToJSON([dato], "set_")[1:]
            name = dato.userId.email.split("@")[0]
            playerData = get_object_or_404(Player, userId=dato.userId.id)
            if playerData.nickname is not None and playerData.nickname != "":
                name = playerData.nickname
            elif playerData.name is not None and playerData.name != "":
                name = playerData.name
            ext = ''
            if playerData.extension is not None:
                ext = playerData.extension
            result = result[:-2] + ',"name":"' + name + '", "extension":"'+ext+'"}\n'
        return result

    @login_required
    def userInfo(request):
        from .players import detailsPlayer
        return APIViews.dataToJSON([detailsPlayer(request.user.id)])

    @login_required
    def editProfile(request):
        from .players import editPlayer
        editPlayer(request)
        if request.POST.get('deleteBT'):
            from .services import deleteFile
            deleteFile(request, request.user.id, 'avatar')
        return request.session.get('msg', _('DataError'))

    @login_required
    def editPass(request):
        from .players import changePass
        changePass(request)
        if request.session.get('msg') == _('PasswordChanged'):
            return 'OK|' + _('PasswordChanged')
        return request.session.get('msg')

    def sendEmailPass(request):
        from .players import sendEmailPass
        res = sendEmailPass(request)
        if res == _('CodeSent'):
            return 'OK|' + res
        return res

    def updPasswordCode(request):
        from .players import updPasswordCode
        res = updPasswordCode(request)
        if res == _('PasswordChanged'):
            return 'OK|' + res
        return res

    @login_required
    def getMessages(request):
        from .messages import getMessages
        return APIViews.dataToJSON(getMessages(request))

    @login_required
    def getFlow(request):
        from .messages import getFlow
        return APIViews.dataToJSON(getFlow(request))

    @login_required
    def addMessage(request):
        from .messages import addMessage
        addMessage(request)
        return ''

    @login_required
    def addToFlow(request):
        from .messages import addToFlow
        addToFlow(request)
        return ''

    @login_required
    def addAudio(request):
        from .messages import addAudio
        addAudio(request)
        return request.session.get('msg')
