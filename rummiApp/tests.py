from pywebpush import webpush

# Create your tests here.
# mEHt-TcTEoI6vEjp-taAxZuXPEYzpKVuAgapLX8c-7s


def test():
    import ast
    from .models import Player, Game
    from .messages import pushMsg
    from django.shortcuts import get_object_or_404
    userData = get_object_or_404(Player, userId=2)
    gameData = get_object_or_404(Game, playerId=userData.id)

    res = pushMsg('PushWelcome', ast.literal_eval(userData.notifAuth), "info@"+gameData.tournamentId.domain)
    return str(res)
