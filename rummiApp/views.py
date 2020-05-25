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
                return redirect('/'+settings.ADMIN_URL+"player/")
            context['status'] = "checked"
            if context['data'].status != '1':
                context['status'] = ""
            context = checkMsg(request, context)
            return render(request, "admin/player/details.html", context)
        except Exception as ex:
            logger("errors", str(ex))
            return Err(request, {'msg': str(ex)})


class PlayerViews():

    @login_required
    def viewTournaments(request):
        try:
            context = {'msg': ''}
            from .tournaments import listTournaments
            context['tournaments'] = listTournaments(request)
            return render(request, "player/game/home.html", context)
        except Exception as ex:
            logger("errors", str(ex))
            return Err(request, {'msg': str(ex)})

    @login_required
    def viewNewGame(request, tournamentId):
        try:
            from .tournaments import detailsTournament
            context = detailsTournament(request, tournamentId)
            from .players import findPlayerUserId
            playerObj = findPlayerUserId(request.user.id)
            if request.POST.get('createBT', False):
                from .games import addGameTournament
                context = addGameTournament(request, tournamentId, playerObj.id)
                if context['id'] is not None:
                    request.session['msg'] = context['msg']
                    return redirect('/game/'+context['id']+"/")
                context['data'] = request.POST
                context['status'] = "checked"
                if request.POST.get("status", False) != '1':
                    context['status'] = ""
            else:
                context['status'] = "checked"
            context['playerId'] = playerObj.id
            context['tournamentId'] = tournamentId
            context = checkMsg(request, context)
            return render(request, "player/game/new.html", context)
        except Exception as ex:
            logger("errors", str(ex))
            return Err(request, {'msg': str(ex)})

    @login_required
    def viewMyGames(request):
        try:
            from .players import findPlayerUserId
            playerObj = findPlayerUserId(request.user.id)
            from .games import listMyGames
            context = listMyGames(request, playerObj.id)
            context = checkMsg(request, context)
            return render(request, "player/game/myGames.html", context)
        except Exception as ex:
            logger("errors", str(ex))
            return Err(request, {'msg': str(ex)})

    @login_required
    def viewGame(request, gameId):
        try:
            context = {'msg': ''}
            from .games import editGameTournament, gameInfo, deleteGameTournament, checkIfGames
            haveGames = checkIfGames(gameId)
            from .players import findPlayerUserId
            playerObj = findPlayerUserId(request.user.id)
            if request.POST.get('editBT', False):
                context1 = editGameTournament(request, gameId, playerObj.id, haveGames)
            if request.POST.get('deleteBT', False):
                if deleteGameTournament(request, gameId, playerObj.id) == 1:
                    return redirect('/myGames/')
            context = gameInfo(gameId, playerObj.id)
            try:
                request.session['msg'] = context1['msg']
                context['form'] = context1['form']
            except Exception:
                pass
            context['status'] = "checked"
            if context['data'].gameId.status != '1':
                context['status'] = ""
            context = checkMsg(request, context)
            context['playerId'] = playerObj.id
            context['gameId'] = gameId
            if haveGames:
                context['haveGames'] = "readonly"
            context['tournamentId'] = context['data'].gameId.tournamentId.id
            return render(request, "player/game/details.html", context)
        except Exception as ex:
            logger("errors", str(ex))
            return Err(request, {'msg': str(ex)})

    @login_required
    def viewMyGame(request, gameId):
        try:
            context = {'msg': ''}
            from .games import gameInfo, viewGame
            from .players import findPlayerUserId
            playerObj = findPlayerUserId(request.user.id)
            try:
                context = gameInfo(gameId, playerObj.id)
            except Http404:
                context = {}
            context['gameId'] = gameId
            context['gameName'] = viewGame(gameId)
            from .games import detailsGamePlayers, detailsGameMatches
            context['players'] = detailsGamePlayers(request, gameId)
            try:
                context['matches'] = detailsGameMatches(request, gameId)
            except Http404:
                context['matches'] = {}
            from .services import tableLabels
            context['tableLabels'] = tableLabels(request.session.get('lang', 'es'))
            return render(request, "player/game/myGameDetails.html", context)
        except Exception as ex:
            logger("errors", str(ex))
            return Err(request, {'msg': str(ex)})

    @login_required
    def joinGame(request, code):
        try:
            context = {'msg': ''}
            from .games import gameInfo, joinGameTournament, viewGame, gameInfoCode
            gameId = gameInfoCode(code)
            from .players import findPlayerUserId
            playerObj = findPlayerUserId(request.user.id)
            if request.POST.get('joinBT', False):
                request.session['msg'] = joinGameTournament(gameId.id, playerObj.id)
                if request.session.get('msg') == _('Joined'):
                    return redirect("/myGame/"+gameId.id)
            try:
                context = gameInfo(gameId.id, playerObj.id)
            except Http404:
                context = {}
            context['gameName'] = viewGame(gameId.id)
            return render(request, "player/game/joinDetails.html", context)
        except Exception as ex:
            logger("errors", str(ex))
            return Err(request, {'msg': str(ex)})

    @login_required
    def viewPlayer(request, gameId, userId):
        try:
            context = {'msg': ''}
            from .games import detailsGamesPlayer
            from .players import findPlayerUserId
            context['data'] = detailsGamesPlayer(request, gameId, userId)
            context['player'] = findPlayerUserId(userId)
            context = checkMsg(request, context)
            from .services import tableLabels
            context['tableLabels'] = tableLabels(request.session.get('lang', 'es'))
            return render(request, "player/game/playerDetails.html", context)
        except Exception as ex:
            logger("errors", str(ex))
            return Err(request, {'msg': str(ex)})

    @login_required
    def matchGameDetails(request, matchGameId):
        context = {'msg': ''}
        try:
            try:
                from .matches import matchPoints
                from .models import MatchGame
                from django.shortcuts import get_object_or_404
                info = get_object_or_404(MatchGame, id=matchGameId)
                context['data'] = info
                context['match_points'] = matchPoints(info.gameId.id, info.matchId.id)
                from .games import detailsMatchGameInfo, getMatchPoints
                context['matchgame'] = detailsMatchGameInfo(info.gameId.id, info.matchId.id, info.playerId.id)
                context['game_points'] = getMatchPoints(info)
            except Http404 as ex:
                context['matchgame'] = {str(ex)}
                pass
            context = checkMsg(request, context)
            return render(request, "player/game/matchGameDetails.html", context)
        except Exception as ex:
            logger("errors", str(ex))
            return Err(request, {'msg': str(ex)})

    @login_required
    def viewProfile(request):
        try:
            from .players import detailsPlayer, editPlayer
            if request.POST.get('editBT', False):
                editPlayer(request)
                from .services import checkImg
                checkImg(request)
            if request.POST.get('deleteBT', False):
                from .services import deleteFile
                deleteFile(request, request.POST.get('userId', False), 'avatar')
                editPlayer(request)
                request.session['userPic'] = '/static/img/user-pic.svg'
            context = {'msg': ''}
            try:
                context = detailsPlayer(request.user.id)
                context['notifications'] = {'OFF': _('OFF'), 'NOW': _('SendAllNotif'), 'HOUR': _('SendHourNoitf'), 'DAY': _('SendDayNotif')}
            except Http404:
                request.session['msg'] = _('UserNotFound')
                return redirect("/err/")
            context = checkMsg(request, context)
            return render(request, "player/account/profile.html", context)
        except Exception as ex:
            logger("errors", str(ex))
            return Err(request, {'msg': str(ex)})

    @login_required
    def viewProfileEditPass(request):
        try:
            context = {'msg': ''}
            if request.POST.get('changePassBT', False):
                from .players import changePass
                changePass(request)
                if request.session.get('msg') == _('PasswordChanged'):
                    from django.contrib.auth import logout
                    logout(request)
                    request.session['msg'] = _('PasswordChanged')
                    return redirect('/')
            context = checkMsg(request, context)
            return render(request, "player/account/changePass.html", context)
        except Exception as ex:
            logger("errors", str(ex))
            return Err(request, {'msg': str(ex)})

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
        if not APIViews.valApiKey(request.POST.get('apiKey', '')) and request.META.get("REMOTE_ADDR", "") != "186.85.5.164":
            return HttpResponse("{'error':'NotAllowed'}")
        from .players import loginUserPass
        context = loginUserPass(request)
        if 'auth' in context:
            return HttpResponse(context['auth']+"|"+request.user.password)
        else:
            return HttpResponse(context['msg'])

    def register(request):
        from django.http import HttpResponse
        if not APIViews.valApiKey(request.POST.get('apiKey', '')) and request.META.get("REMOTE_ADDR", "") != "186.85.5.164":
            return HttpResponse("{'error':'NotAllowed'}")
        from .players import registerUser
        from .models import tmpPIN
        if request.POST.get('valEmailBT', '') != '':
            try:
                request.session['userpin'] = tmpPIN.objects.filter(email=request.POST.get('email', '-1')).order_by('id')[0].pin
            except Exception as ex:
                request.session['userpin'] = str(ex)
        context = registerUser(request)
        if context['value'] == 'sent' or context['value'] == 'registered':
            return HttpResponse("1|"+context['msg'])
        else:
            return HttpResponse(str(context['msg']))

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
        logger("errors", str(request.POST))
        try:
            from django.http import HttpResponse
            oper = request.POST.get('oper', '')
            publicAccess = "tournaments,teams,login,register"
            # Set Language
            APIViews.lang(request)
            # check API Key for Non public Opers
            if oper not in publicAccess:
                from .players import loginUserRequestsApp
                # Validate application Key
                if request.POST.get('usernameUser', '') == '':
                    return HttpResponse("No Access")
                if not APIViews.valApiKey(request.POST.get('apiKey', ''), request.POST.get('usernameUser', '')) and request.META.get("REMOTE_ADDR", "") != "127.0.0.1":
                    return HttpResponse("No Access")
                # create user for current request
                user = loginUserRequestsApp(request)
                # check User Still Exist and Active
                try:
                    user.id
                except Exception:
                    return HttpResponse("{'error':1}")
            # get data
            return HttpResponse(getattr(APIViews, oper)(request))
        except Exception as ex:
            logger("errors", str(ex))
            return HttpResponse("{'error':1}")

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

    @login_required
    def addGame(request):
        from .games import addGame
        return addGame(request)

    @login_required
    def editGame(request):
        from .games import editGame
        return editGame(request)

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
    def dealCards(request):
        from .games import dealCards
        return dealCards(request)

    @login_required
    def pickCard(request):
        from .games import pickCard
        return pickCard(request)

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
        data = viewMyGames(request.POST.get('userId'))
        result = ""
        for dato in data:
            result += APIViews.dataToJSON([dato])
        result = result.replace('Id_id', 'Id')
        return result

    @login_required
    def gameDetailInfo(request):
        from .games import detailsGameInfo
        data = detailsGameInfo(request.POST.get('gameId'), request.POST.get('userId'))
        result = ""
        for dato in data:
            result += APIViews.dataToJSON([dato.gameId])[:-2]
            result += APIViews.dataToJSON([dato], "set_")[1:]
        result = result.replace('Id_id', 'Id')
        return result
