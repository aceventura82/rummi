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
    # Validate user in Game
    get_object_or_404(GameSet, gameId=request.POST.get("gameId"), userId=request.user.id, set=1)
    from .services import logger
    logger("errors", str(request.user.id))
    formData = GameMessagesForm(request.POST)
    if formData.is_valid():
        objMsg = formData.save(commit=False)
        objMsg.userId = request.user
        objMsg.save()
