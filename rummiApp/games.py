from django.utils.translation import gettext as _


def detailsGameInfo(gameId, userId):
    from .models import GameSet, Player
    from django.shortcuts import get_object_or_404, get_list_or_404
    playerData = get_object_or_404(Player, userId=userId, status='1')
    get_object_or_404(GameSet, gameId=gameId, playerId=playerData.id)
    return get_list_or_404(GameSet, gameId=gameId)


def viewGame(gameId):
    from .models import Game
    from django.shortcuts import get_object_or_404
    return get_object_or_404(Game, id=gameId)


def viewGameCode(code):
    from .models import Game
    from django.shortcuts import get_object_or_404
    return get_object_or_404(Game, code=code)


def viewMyGames(userId):
    from .models import GameSet, Player
    from django.shortcuts import get_list_or_404, get_object_or_404
    playerData = get_object_or_404(Player, userId=userId, status='1')
    return get_list_or_404(GameSet, playerId=playerData.id, set=1)


def addGame(request):
    from .models import GameForm, GameSetForm, Player
    from django.shortcuts import get_object_or_404
    import random
    import string
    playerData = get_object_or_404(Player, userId=request.user.id, status='1')
    formData = GameForm(request.POST)
    if formData.is_valid():
        gameObj = formData.save()
        gameObj.code = ''.join(random.choice(string.ascii_letters) for i in range(4))+str(gameObj.pk)
        gameObj.playersPos = str(request.user.id)+","
        gameObj.save()
        gpObj = GameSetForm({'set': 1, 'fullDraw': request.POST.get('fullDraw')[0:1] == "1",
                            "points": 0, "playerId": playerData.id, "gameId": gameObj.pk, "current_cards": "", "chairPos": 1})
        try:
            gpObj.save()
        except Exception:
            return _('GeneralError')
        return str(gameObj.pk)+"|"+_('GameCreated')
    else:
        return _('WrongData')


def joinGame(request):
    from .models import GameSetForm, GameSet, Player, Game
    from django.shortcuts import get_object_or_404
    from django.http import Http404
    code = request.POST.get('code')
    if request.POST.get("pos") == '' or not request.POST.get("pos").isnumeric() or int(request.POST.get("pos")) >= 5:
        return _('WronPlace')
    pos = int(request.POST.get("pos"))
    playerData = get_object_or_404(Player, userId=request.user.id, status='1')
    gameInfo = get_object_or_404(Game, code=code)
    try:
        get_object_or_404(GameSet, gameId=gameInfo.id, playerId=playerData.id)
        return _('AlreadyInGame')
    except Http404:
        pass
    gpObj = GameSetForm({'set': 1, 'fullDraw': gameInfo.fullDraw[0:1] == "1",
                        "points": 0, "playerId": playerData.id, "gameId": gameInfo.id, "current_cards": "", "chairPos": pos})
    gpObj.save()
    # check if the sit is available
    playerPos = gameInfo.playersPos.strip(",").split(",")
    if len(playerPos) > 5:
        return _('NoSitAvailable')
    # add the userId to the position
    gameInfo.playersPos += str(request.user.id)+","
    gameInfo.save()
    return "1|"+_('Joined')


def editGame(request):
    from .models import Game, GameFormEdit
    from django.shortcuts import get_object_or_404
    gameId = request.POST.get('gameId')
    gameData = get_object_or_404(Game, pk=gameId, userId=request.user.id)
    formData = GameFormEdit(request.POST, instance=gameData)
    if formData.is_valid():
        formData.save()
        return "1|"+_('Edited')
    else:
        return _('WrongData')


# Delete game
def deleteGame(request):
    from .models import Game, GameSet
    from django.shortcuts import get_object_or_404
    gameData = get_object_or_404(Game, pk=request.POST.get('gameId'), userId=request.user.id)
    userCount = GameSet.objects.filter(set=1, gameId=request.POST.get('gameId')).count()
    if userCount > 1:
        return _('CannotDeleteHasUser')
    gameData.delete()
    return "1|"+_('Deleted')


def startGame(request):
    from .models import Game
    from django.shortcuts import get_object_or_404
    gameId = request.POST.get('gameId')
    gameData = get_object_or_404(Game, pk=gameId, userId=request.user.id)
    if gameData.started is True:
        return _('GameAlreadyStarted')
    playerPos = gameData.playersPos.split(",")
    val = 0
    for pl in playerPos:
        if pl != '':
            val += 1
    if val > 1:
        gameData.started = True
        gameData.save()
        return "1|"+_('GameStarted')
    return _('CannotStartOneUser')


# Deal cards at the begining of each set
def dealCards(request):
    import random
    cards = [
        'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '0S', 'JS', 'QS', 'KS',
        'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '0H', 'JH', 'QH', 'KH',
        'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '0D', 'JD', 'QD', 'KD',
        'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '0C', 'JC', 'QC', 'KC',
        'XX', 'XX', 'XX', 'XX',
        'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '0S', 'JS', 'QS', 'KS',
        'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '0H', 'JH', 'QH', 'KH',
        'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '0D', 'JD', 'QD', 'KD',
        'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '0C', 'JC', 'QC', 'KC'
    ]
    # Deal stack
    random.shuffle(cards)
    from django.shortcuts import get_object_or_404, get_list_or_404
    from .models import Game, GameSet
    gameId = request.POST.get("gameId")
    gameData = get_object_or_404(Game, id=gameId)
    players = gameData.playersPos.strip(",").split(",")
    if players[gameData.currentPlayerPos] != str(request.user.id):
        return _('YouAreNotDealingThisGame')
    if gameData.current_stack != '':
        return _('AlreadyDealt')
    # get Players list
    players = get_list_or_404(GameSet, gameId=gameId, set=gameData.current_set)
    # set number of cards, 1-4 13, 5,6 15
    cardsNum = 13
    if gameData.current_set > 4:
        cardsNum = 15
    # set the cards for each player
    for player in players:
        # put each 13/15 card in the user current_cards
        for i in range(0, cardsNum):
            # get a randon card position from the card stack
            rand = random.randint(0, len(cards)-1)
            player.current_cards += cards[rand]+","
            del cards[rand]
        player.save()
    # set the remains card to the stack
    gameData.current_stack = ",".join(str(x) for x in cards)+","
    gameData.save()
    return "1|"+_('Dealt')


def pickCard(request):
    from .models import Game, Player, GameSet
    from django.shortcuts import get_object_or_404
    gameId = request.POST.get('gameId')
    playerData = get_object_or_404(Player, userId=request.user.id, status='1')
    gameData = get_object_or_404(Game, pk=gameId)
    gameSetData = get_object_or_404(GameSet, gameId=gameId, playerId=playerData.id, set=gameData.current_set)
    if not canPlay(gameData, playerData.userId.id):
        return _('NotYourTurn')
    if gameSetData.moveStatus != 1:
        return _('AlreadyPick')
    if request.POST.get("stack") == '1':
        return pickFromStack(gameData, gameSetData)
    if request.POST.get("discard") == '1':
        if gameSetData.drawn != '':
            return _('CannotPickFromDiscardAlreadyDrawn')
        return pickFromDiscarded(gameData, gameSetData)
    else:
        return _('GeneralError')


def discardCard(request):
    from .models import Game, Player, GameSet
    from django.shortcuts import get_object_or_404
    gameId = request.POST.get('gameId')
    playerData = get_object_or_404(Player, userId=request.user.id, status='1')
    gameData = get_object_or_404(Game, pk=gameId)
    if not canPlay(gameData, playerData.userId.id):
        return _('NotYourTurn')
    if request.POST.get("out", '-1') == '-1':
        return _('PickCardToDiscard')
    card = request.POST.get("out")
    if card == 'XX':
        return _('CannotDiscardJoker')
    # find user discard position
    playerPos = gameData.playersPos.split(",")
    pos = 0
    gameSetData = get_object_or_404(GameSet, gameId=gameId, playerId=playerData.id, set=gameData.current_set)
    if gameSetData.moveStatus == 1:
        return _('PickCardFirst')
    if card+"," not in gameSetData.current_cards:
        return _('CardNotInYourGame')
    # check if pick from discarded, cannot discard same card
    if gameSetData.moveStatus == 3 and gameSetData.current_cards[-3:-1] == card:
        return _('CannotDiscardPickedFromDiscard')
    for player in playerPos:
        if player == '':
            return _('GeneralError')
        if player == str(gameSetData.playerId.userId.id):
            break
        pos += 1
    # add card in discarded pos
    discardPositions = gameData.current_discarded.split('|')
    i = 0
    newDiscard = ''
    for discard in discardPositions:
        if i == pos:
            newDiscard += discard+card+",|"
        else:
            newDiscard += discard+"|"
        i += 1
    gameData.current_discarded = newDiscard[0:-1]
    gameData.save()
    # remove card from user cards
    gameSetData.current_cards = gameSetData.current_cards.replace(card+",", "", 1)
    gameSetData.moveStatus = 1
    gameSetData.save()
    if checkEndSet(gameSetData.current_cards, gameData):
        return "1|"+_('GameEnded')
    # move turn to next player
    moveTurn(gameData)
    return _('Descarted')


# draw own game
# drawCards, 2S,2H,2C|0D,JD,QD,KD|4S,4S,4C
# set, gameId
def draw(request):
    from .models import Player, GameSet, Game
    from django.shortcuts import get_object_or_404
    playerData = get_object_or_404(Player, userId=request.user.id, status='1')
    gameId = request.POST.get('gameId')
    gameData = get_object_or_404(Game, pk=gameId)
    if not canPlay(gameData, playerData.userId.id):
        return _('NotYourTurn')
    gameSetData = get_object_or_404(GameSet, gameId=gameId,
                                    playerId=playerData.id, set=gameData.current_set)
    # check not drawn already
    if gameSetData.drawn != '':
        return _('AlreadyDrawn')
    if gameSetData.moveStatus == 1:
        return _('PickCardFirst')
    if gameSetData.moveStatus == 4:
        return _('AlreadyDrawn')
    # check if cards  in hand
    cardsCheck = request.POST.get('drawCards').replace("|", ",").split(",")
    cardsInHand = gameSetData.current_cards
    for card in cardsCheck:
        if card not in cardsInHand:
            return _('MissingCards')
        cardsInHand = cardsInHand.replace(card+",", "", 1)
    # check if set is fullDraw
    if gameSetData.fullDraw == 1 and not valFullDraw(
            len(request.POST.get('drawCards').replace('|', '').split(',')), gameData.current_set):
        return _('GameIsFullDraw')
    # validate games are valid for the set
    if not valSet(gameData.current_set, request.POST.get('drawCards')):
        return _('GameNotValid')
    # remove drawn cards
    cards = request.POST.get('drawCards').replace('|', '').strip(",").split(',')
    for card in cards:
        gameSetData.current_cards = gameSetData.current_cards.replace(card+',', '', 1)
    # put drawn cards in drawn user
    gameSetData.drawn = request.POST.get('drawCards')
    gameSetData.moveStatus = 4
    gameSetData.save()
    if checkEndSet(gameSetData.current_cards, gameData):
        return "1|"+_('GameEnded')
    return _('Drawn')


# Draw one card in others game
# set, gameId, drawPlayerId, drawPos
def drawOver(request):
    from .models import Player, GameSet, Game
    from django.shortcuts import get_object_or_404
    playerData = get_object_or_404(Player, userId=request.user.id, status='1')
    gameId = request.POST.get('gameId')
    gameData = get_object_or_404(Game, pk=gameId)
    set = gameData.current_set
    gameSetData = get_object_or_404(GameSet, gameId=gameId, playerId=playerData.id, set=set)
    if not canPlay(gameData, playerData.userId.id):
        return _('NotYourTurn')
    drawnGameSetData = get_object_or_404(
        GameSet, gameId=gameId, playerId=request.POST.get('drawPlayerId'), set=set)
    # check both users are drawn
    if gameSetData.drawn == '':
        return _('YoCannoDrawOverYet')
    if drawnGameSetData.drawn == '':
        return _('NoGameToDrawIn')
    if gameSetData.moveStatus == 4:
        return _('NoDrawOverOnDraw')
    if gameSetData.moveStatus == 5:
        return _('JustCanOneDrawOver')
    # get other user drawn info
    drawGame = drawnGameSetData.drawn.split('|')[int(request.POST.get('drawPos'))]
    inCard = request.POST.get('in')
    # check if valid card
    if inCard+"," not in gameSetData.current_cards:
        return _('NotValidCard')
    # check if game is TOAK
    if valThreeOfAKind(drawGame.strip(",")):
        return putCardTOAK(request, inCard, drawGame, gameData, gameSetData, drawnGameSetData, playerData.id)
    # check if game is Straight
    elif valStraight(drawGame.strip(",")):
        return putCardSTR(request, inCard, drawGame, gameData, gameSetData, drawnGameSetData, playerData.id)
    return _('NotValidDrawOver')


# ********* inner calls **********


def putCardTOAK(request, inCard, drawGame, gameData, gameSetData, drawnGameSetData, playerId):
    # is same number add card
    if inCard[0:1] == drawGame[0:1] or drawGame[0:2] == 'XX' or inCard == 'XX':
        drawnGameSetData.drawn = addToDrawn(drawnGameSetData.drawn, int(request.POST.get('drawPos')), inCard)
        drawnGameSetData.save()
        gameSetData.current_cards = gameSetData.current_cards.replace(inCard+",", "", 1)
        gameSetData.moveStatus = 5
        # if drawn in own game, update own drawn
        if request.POST.get('drawPlayerId') == str(playerId):
            gameSetData.drawn = drawnGameSetData.drawn
        gameSetData.save()
        if checkEndSet(gameSetData.current_cards, gameData):
            return "1|"+_('GameEnded')
        return _('DrawOverMade')


def putCardSTR(request, inCard, drawGame, gameData, gameSetData, drawnGameSetData, playerId):
    # find if put card at begining or end
    if inCard[0:2] != 'XX':
        pos = checkAppenStrCard(drawGame.strip(",").split(','), inCard)
    elif request.POST.get("pos") == '1' or request.POST.get("pos") == '2':
        pos = request.POST.get("pos")
    else:
        return _('NotValidPosJoker')
    if pos == -1:
        return _('NotValidDrawOver')
    # put card in other user drawn
    drawnGameSetData.drawn = addToDrawn(drawnGameSetData.drawn, int(request.POST.get('drawPos')), inCard, pos)
    drawnGameSetData.save()
    # remove drawn card from user
    gameSetData.current_cards = gameSetData.current_cards.replace(inCard+",", "", 1)
    gameSetData.moveStatus = 5
    # if drawn in own game, update own drawn
    if request.POST.get('drawPlayerId') == str(playerId):
        gameSetData.drawn = drawnGameSetData.drawn
    gameSetData.save()
    if checkEndSet(gameSetData.current_cards, gameData):
        return "1|"+_('GameEnded')
    return _('DrawOverMade')


def addToDrawn(drawn, pos, card, strPos=-1):
    drawPos = drawn.split("|")
    i = 0
    newDraw = ''
    for draw in drawPos:
        if i == pos:
            if strPos == 0:
                # put at the begining
                newDraw += card+","+draw+"|"
            else:
                # put at the end
                newDraw += draw+card+",|"
        else:
            newDraw += draw+"|"
        i += 1
    return newDraw[:-1]


# get next card from stack
def pickFromStack(gameData, gameSetData):
    if gameData.current_stack == '':
        # re deal stack
        cards = gameData.current_discarded.replace("|", "").strip(",").split(",")
        import random
        random.shuffle(cards)
        gameData.current_stack = ",".join(str(x) for x in cards)+","
        gameData.current_discarded = ''
        gameData.save()
    card = gameData.current_stack[-3:-1]
    gameData.current_stack = gameData.current_stack[0:-3]
    gameData.save()
    gameSetData.current_cards += card+","
    gameSetData.moveStatus = 2
    gameSetData.save()
    return "1|"+card


# get next card from discarded position
def pickFromDiscarded(gameData, gameSetData):
    # find user discard position
    playerPos = gameData.playersPos.strip(",").split(",")
    pos = 0
    for player in playerPos:
        if player == '':
            return _('GeneralError')
        if player == str(gameSetData.playerId.userId.id):
            break
        pos += 1
    # descart pos is the previous to user Pos
    pos -= 1
    # if pos = -1 the first user pos is the last one
    if pos == -1:
        pos = len(playerPos)-1
    # get discarded card from discard position
    newDiscard = ''
    discardPositions = gameData.current_discarded.split('|')
    i = 0
    card = ''
    for discard in discardPositions:
        if i == pos:
            card = discard[-3:-1]
            newDiscard += discard[0:-3]+"|"
        else:
            newDiscard += discard+"|"
        i += 1
    if card == '':
        return _('NoCardsInDiscard')
    gameData.current_discarded = newDiscard[0:-1]
    gameData.save()
    gameSetData.current_cards += card+","
    gameSetData.moveStatus = 3
    gameSetData.save()
    return "1|"+card


def canPlay(gameData, userId):
    playerPos = gameData.playersPos.split(",")
    if playerPos[gameData.currentPlayerPos] == str(userId):
        return True
    if not gameData.started:
        return False
    return False


def moveTurn(gameData):
    playerPos = gameData.playersPos.strip(",").split(",")
    gameData.currentPlayerPos += 1
    if gameData.currentPlayerPos >= len(playerPos):
        gameData.currentPlayerPos = 0
    gameData.save()


# if set Ends: update users points, and create next set
def checkEndSet(cards, gameData):
    if cards == '':
        from django.shortcuts import get_list_or_404
        from .models import GameSetForm, GameSet
        # get all players info
        players = get_list_or_404(GameSet, gameId=gameData.id, set=gameData.current_set)
        for player in players:
            # set player left points
            if player.current_cards != '':
                setPoints(gameData.id, player.playerId.userId.id, gameData.current_set)
        gameData.current_set += 1
        # if last set end Tournament
        if gameData.current_set > 6:
            return True
        # get all players from set 1
        gameSetData = get_list_or_404(GameSet, gameId=gameData.id, set=1)
        # add new set to all players, check if next set is fullDraw
        for gameSet in gameSetData:
            gpObj = GameSetForm({'set': gameData.current_set, 'fullDraw': gameData.fullDraw[gameData.current_set-1:gameData.current_set] == "1",
                                "points": 0, "playerId": gameSet.playerId.id, "gameId": gameData.id, "current_cards": "", "chairPos": gameSet.chairPos})
            gpObj.save()
        # get players and set who start next round
        playerPos = gameData.playersPos.strip(",").split(",")
        next = gameData.current_set % len(playerPos)-1
        if next == -1:
            next = len(playerPos)-1
        gameData.currentPlayerPos = next
        gameData.current_stack = ''
        gameData.current_discarded = '||||'
        gameData.save()
        return True
    return False


# Check if card fits in straight
def checkAppenStrCard(drawGameCards, inCard):
    # check is same color
    if drawGameCards[0][1:2] != inCard[1:2]:
        return -1
    # make Leters numeric
    cardN = letterToNumber(inCard[0:1])
    cardH = letterToNumber(drawGameCards[0][0:1])
    cardE = letterToNumber(drawGameCards[len(drawGameCards)-1][0:1])
    pos = -1
    if (cardN == cardH-1) or (cardH == 1 and cardN == 13):
        pos = 0
    elif (cardN == cardE+1) or (cardE == 13 and cardN == 1):
        pos = 1
    return pos


# convert card to number to easy compare
def letterToNumber(cardN):
    if cardN == '0':
        cardN = 10
    elif cardN == 'J':
        cardN = 11
    elif cardN == 'Q':
        cardN = 12
    elif cardN == 'K':
        cardN = 13
    elif cardN == 'A':
        cardN = 1
    return int(cardN)


# convert card to number to easy compare
def numberToLetter(cardN):
    if cardN == 10:
        cardN = 0
    elif cardN == 11:
        cardN = 'J'
    elif cardN == 12:
        cardN = 'Q'
    elif cardN == 13:
        cardN = 'K'
    elif cardN == 1:
        cardN = 'A'
    return str(cardN)


# heck if user is drawing all cards
def valFullDraw(cardsCount, set):
    if set < 5 and cardsCount < 13:
        return False
    elif set >= 5 and cardsCount < 15:
        return False
    return True


# check if the games for the set are valid
# set, gameId
# drawCards: 2S,2H,2C,|0D,JD,QD,KD,|4S,4S,4C,
def valSet(set, drawCards):
    gamesList = drawCards.split('|')
    TOAK = 0
    STR = 0
    for game in gamesList:
        if game[-1] != ',':
            return False
        if valThreeOfAKind(game.strip(",")):
            TOAK += 1
        elif valStraight(game.strip(",")):
            STR += 1
        else:
            return False
    if set == 1 and TOAK == 1 and STR == 1:
        return True
    elif set == 2 and TOAK == 3 and STR == 0:
        return True
    elif set == 3 and TOAK == 2 and STR == 1:
        return True
    elif set == 4 and TOAK == 0 and STR == 2:
        return True
    elif set == 5 and TOAK == 1 and STR == 2:
        return True
    elif set == 6 and TOAK == 0 and STR == 3:
        return True
    return False


# check if cards are an straight
def valStraight(cards):
    cardList = cards.split(',')
    if len(cardList) < 4:
        return False
    # remove all initials joker
    cardList = removeInitialJokers(cardList)
    if len(cardList) == 0:
        return False
    # the initial card
    prevCard = cardList[0]
    # the initial card number
    prevCardN = letterToNumber(prevCard[0:1])
    for i in range(1, len(cardList)):
        if cardList[i] == 'XX':
            # if joker, don't validate and set the spected value to the previous card
            prevCard = numberToLetter(letterToNumber(prevCard[0:1])+1)+prevCard[1:2]
            prevCardN = letterToNumber(prevCard[0:1])
            continue
        cc = letterToNumber(cardList[i][0:1])
        # if not the same color
        if cardList[i][1:2] != prevCard[1:2]:
            return False
        if prevCardN == 13:
            prevCardN = 0
        if cc != prevCardN+1:
            return False
        prevCard = cardList[i]
        prevCardN = letterToNumber(cardList[i][0:1])
    return True


def replaceJoker(card):
    if card[0:1] in '2345678':
        return str(int(card[0:1])+1)+card[1:2]
    if card[0:1] == '9':
        return "0"+card[1:2]
    if card[0:1] == '0':
        return "J"+card[1:2]
    if card[0:1] == 'J':
        return "Q"+card[1:2]
    if card[0:1] == '0':
        return "J"+card[1:2]


def removeInitialJokers(cardList):
    # remove all initials joker
    i = 0
    while i < len(cardList):
        if cardList[i] == 'XX':
            del cardList[i]
            i -= 1
        else:
            break
        i += 1
    return cardList


# check if cards are Three Of A Kind
def valThreeOfAKind(cards):
    cardList = cards.split(',')
    if len(cardList) < 3:
        return False
    # remove all initials joker
    cardList = removeInitialJokers(cardList)
    if len(cardList) == 0:
        return False
    prevCard = cardList[0][0:1]
    for i in range(1, len(cardList)):
        if cardList[i] == 'XX':
            continue
        if cardList[i][0:1] != str(prevCard):
            return False
    return True


# set points left in player hand
def setPoints(gameId, userId, set):
    from .models import GameSet, Player
    from django.shortcuts import get_object_or_404
    playerData = get_object_or_404(Player, userId=userId, status='1')
    gameSetData = get_object_or_404(GameSet, gameId=gameId,
                                    playerId=playerData.id, set=set)
    cards = gameSetData.current_cards.strip(",").split(',')
    points = 0
    for card in cards:
        points += cardValue(card)
    gameSetData.points = points
    gameSetData.save()


# get a card value
def cardValue(card):
    if card[0:1] == "0":
        return 10
    if card[0:1].isnumeric():
        return int(card[0:1])
    if card[0:1] in "JQK":
        return 10
    if card[0:1] in "ASAC":
        return 15
    if card[0:1] in "ADAH":
        return 1
    return 100
