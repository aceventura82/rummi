def getMessages(request):
    from .models import GameMessages, GameSet
    from django.shortcuts import get_list_or_404, get_object_or_404
    from django.http import Http404
    # Validate user in Game
    get_object_or_404(GameSet, gameId=request.POST.get("gameId"), userId=request.user.id, set=1)
    try:
        return get_list_or_404(GameMessages, gameId=request.POST.get("gameId"), id__gte=request.POST.get("lastId"))
    except Http404:
        return ''


def addMessage(request):
    from .models import GameMessagesForm, GameSet
    from django.shortcuts import get_object_or_404
    from .games import updateDate
    # Validate user in Game
    get_object_or_404(GameSet, gameId=request.POST.get("gameId"), userId=request.user.id, set=1)
    formData = GameMessagesForm(request.POST)
    if formData.is_valid():
        objMsg = formData.save(commit=False)
        objMsg.userId = request.user
        updateDate(request.POST.get("gameId"))
        objMsg.save()


def getFlow(request):
    from .models import GameFlow, GameSet
    from django.shortcuts import get_list_or_404, get_object_or_404
    from django.http import Http404
    # Validate user in Game
    get_object_or_404(GameSet, gameId=request.POST.get("gameId"), userId=request.user.id, set=1)
    try:
        return get_list_or_404(GameFlow, gameId=request.POST.get("gameId"), id__gte=request.POST.get("lastIdF"))
    except Http404:
        return ''


def addToFlow(request):
    from .models import GameFlowForm, GameSet
    from django.shortcuts import get_object_or_404
    # Validate user in Game
    get_object_or_404(GameSet, gameId=request.POST.get("gameId"), userId=request.user.id, set=1)
    formData = GameFlowForm(request.POST)
    if formData.is_valid():
        formData.save()
