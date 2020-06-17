from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils.translation import gettext as _


def listPlayers(request):
    from .models import Player
    search = request.POST.get('search', False)
    if search is False:
        search = request.session.get('criteria', '')
    if search.isnumeric():
        playersData = Player.objects.filter(id=search).order_by('name')
    elif '@' in search:
        playersData = Player.objects.filter(userId__email=search).order_by('name')
    elif search == '' or len(search) < 3:
        return {"msg": _("NarrowSearch")}
    else:
        from django.db.models import Q
        playersData = Player.objects.filter(Q(name__icontains=search) | Q(lastname__icontains=search)).order_by('name')
    request.session['criteria'] = search
    from django.conf import settings
    paginator = Paginator(playersData, settings.PAGINATION)
    players = paginator.get_page(request.GET.get('page'))
    return {'players': players, 'criteria': search}


def registerUser(request):
    context = {"msg": "", "value": ""}
    if (request.POST.get('valEmailBT', False) and request.POST.get('PINEmail', '') == request.session.get('userpin', '-1')) or request.session.get('valURL', False):
        # PIN ok, try to authenticate
        valAuth = authCreate(request)
        if valAuth is False:
            context['msg'] = _('AuthenticationFailed')
        elif valAuth == -1:
            context['msg'] = _('UserDeactivated')
        else:
            context['value'] = 'registered'
            context['msg'] = 'registered'
            context['auth'] = valAuth
            return context
    # Send PIN
    elif request.POST.get('sendEmailBT', False):
        valUserRes = valUserEmail(request, context)
        if valUserRes != 1:
            context['value'] = 'AlreadyEmail'
            return context
        if len(request.POST.get('passwordEmail', "")) < 6 or all(c.isalpha() == request.POST.get('passwordEmail', "").isalpha() for c in request.POST.get('passwordEmail', "")):
            context['msg'] = _('NotValidPass')
            return context
        if request.POST.get('passwordEmail', '-1') != request.POST.get('passwordEmail2', '-1'):
            context['msg'] = _('DiffPass')
            return context
        request.session['user_email'] = request.POST.get('email', False)
        request.session['user_pass'] = request.POST.get('passwordEmail', False)
        from .services import sendPin
        sendPin(request)
        if request.POST.get('oper') == 'register':
            from .models import tmpPIN, tmpPINForm
            dataOldPin = tmpPIN.objects.filter(email=request.POST.get('email', False))
            dataOldPin.delete()
            formData = tmpPINForm({"email": request.POST.get('email', False), "pin": request.session.get('userpin', '-1')})
            formData.save()
        context['msg'] = _('PINSent')
        context['value'] = 'sent'
    elif request.POST.get('valEmailBT', False) and request.POST.get('PINEmail', '') != request.session.get('userpin', '-1'):
        # Wrong Pin
        context['value'] = 'sent'
        context['msg'] = _('WrongPIN')
    return context


def valUserEmail(request, context):
    from .models import Player
    email = request.POST.get('email', False)
    # check if email not empty
    if len(email) < 2:
        context['msg'] = _('UsernameNotValid')
        return context
    try:
        # check if user exits
        Player.objects.get(userId__email=email)
        if request.path == '/register/':
            # if registering return error
            context['msg'] = _('AlreadyUsed')
            return context
        return 1
    except Exception:
        # if not registering, user does not exits
        if request.path != '/register/' and request.POST.get('oper') != 'register':
            context['msg'] = _('NotRegistered')
            return context
        # New User
        try:
            # check email not in use
            User.objects.get(email=email)
            context['msg'] = _('RegisteredDifferentEMAIL')
            return context
        except Exception:
            try:
                # check if username exits
                Player.objects.get(userId__username=email)
                context['msg'] = _('RegisteredDifferentEMAIL')
                return context
            except Exception:
                return 1


def loginUserPass(request):
    context = {'msg': ''}
    from django.contrib.auth import authenticate, login
    userN = request.POST.get('usernameUser', False)
    password = request.POST.get('password', False)
    if User.objects.filter(username=userN).exists():
        user = authenticate(username=userN, password=password)
        if user:
            userObj = findPlayerUserId(user.id)
            if user.is_staff:
                context['auth'] = 'OK_STAFF'
            elif userObj.status != '1':
                context['msg'] = _('UserDeactivated')
                return context
            elif user.id != 0 and userObj == -1:
                addPlayer(request, {'userId': user.id, 'status': '1', 'phone': userN})
                userObj = findPlayerUserId(user.id)
            if user is not None:
                login(request, user)
            if user.id:
                if not user.is_staff:
                    request.session['username'] = userObj.nickname
                    context['auth'] = 'OK'
            else:
                context['msg'] = _('AuthenticationFailed')
        else:
            context['msg'] = _('AuthenticationFailed')
    else:
        context['msg'] = _('UserNotFound')
    return context


def loginUserRequestsApp(request):
    userN = request.POST.get('usernameUser', False)
    user = User.objects.filter(username=userN)
    if user[0]:
        userObj = findPlayerUserId(user[0].id)
        if user[0].is_staff:
            return _('AuthenticationFailed')
        elif userObj.status != '1':
            return _('UserDeactivated')
        from django.contrib.auth import login
        login(request, user[0])
        request.session['username'] = userObj.nickname
        return user[0]
    else:
        return _('UserNotFound')


def authCreate(request):
    userN = request.session.get('user_email')
    if userN is None:
        userN = request.POST.get("email")
    player = findUser(request, userN)
    user = User.objects.get(id=player.userId.id)
    if user is not None:
        from django.contrib.auth import login
        login(request, user)
    if request.user.id:
        if player.status != '1':
            return -1
        request.session['username'] = player.nickname
        request.session['user_email'] = None
        request.session['user_pass'] = None
        return 'OK'
    else:
        return False


def findUser(request, user):
    # create user first
    password = request.session.get('user_pass')
    if password is None:
        password = request.POST.get("passwordEmail")
    userAux = User.objects.create_user(username=user, password=password, email=user)
    # Validate Player is created, else create it
    player = findPlayerUserId(userAux.id)
    if player == -1 and not userAux.is_staff:
        addPlayer(request, {'userId': userAux.id, 'status': '1', 'notifications': 'OFF'})
        player = findPlayerUserId(userAux.id)
    return player


def addPlayer(request, data=None):
    from .models import PlayerForm
    formData = PlayerForm(request.POST)
    if data is not None:
        formData = PlayerForm(data)
    if formData.is_valid():
        playerObj = formData.save()
        return {'msg': _('PlayerSaved'), 'id': str(playerObj.pk)}
    else:
        return {'msg': _('DataError'), 'form': formData}


def detailsPlayer(pk):
    from .models import Player
    return get_object_or_404(Player, userId=pk)


def findPlayerUserId(pk):
    from .models import Player
    from django.http import Http404
    try:
        return get_object_or_404(Player, userId=pk)
    except Http404:
        return -1


def changePass(request):
    userData = get_object_or_404(User, pk=request.user.id)
    if not request.user.check_password(request.POST.get('old_password', "")):
        request.session['msg'] = _('WrongPass')
        request.session['WrongPass'] = 1
        return
    if request.POST.get('new_password1', "") != request.POST.get('new_password2', ""):
        request.session['msg'] = _('DiffPass')
        request.session['WrongPass'] = 1
        return
    if len(request.POST.get('new_password1', "")) < 6 or all(c.isalpha() == request.POST.get('new_password1', "").isalpha() for c in request.POST.get('new_password1', "")):
        request.session['msg'] = _('NotValidPass') + str(str(request.POST.get('new_password1', "")).isalpha())
        request.session['WrongPass'] = 1
        return
    userData.set_password(request.POST.get('new_password1', ""))
    userData.save()
    request.session['msg'] = _('PasswordChanged')


def editPlayer(request, admin=False):
    from .models import Player, PlayerForm
    if admin:
        playerData = get_object_or_404(Player, userId=request.POST.get('userId'))
    else:
        playerData = get_object_or_404(Player, userId=request.user.id)
    userData = get_object_or_404(User, id=playerData.userId.id)
    currentStatus = playerData.status
    currentExt = playerData.extension
    formData = PlayerForm(request.POST, instance=playerData)
    if formData.is_valid():
        request.session['msg'] = ""
        saveObj = formData.save(commit=False)
        if not admin:
            saveObj.userId = request.user
            saveObj.status = currentStatus
            userData.save()
        if request.POST.get('deleteBT'):
            saveObj.extension = None
        else:
            saveObj.extension = currentExt
        if admin:
            userData.email = request.POST.get('email')
            userData.username = request.POST.get('email')
        userData.userId = playerData.userId
        try:
            if request.FILES.get('avatar').name:
                import os
                filename, file_extension = os.path.splitext(request.FILES.get('avatar').name)
                from .services import fileUpload
                fileUpload(request, request.POST.get('userId', ""), 'avatar')
                saveObj.extension = file_extension
        except Exception:
            pass
        saveObj.save()
        userData.save()
        request.session['msg'] += _('PlayerUpdated')
        request.session['username'] = playerData.nickname
    else:
        request.session['msg'] = _('DataError')


def getUserHash(username):
    UserData = get_object_or_404(User, username=username)
    return username + "|" + UserData.password
