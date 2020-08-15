//Move Cards
function raiseCard(card) {
  var childs = document.getElementById('cardsDiv').getElementsByTagName('button');
  var cardPos = -1;
  for (var i = 0; i < childs.length; i++) {
    if (childs[i] == card) {
      cardPos = i;
      break;
    }
  }
  if (card.style.top == '-30px') { //lower card
    card.style.top = '0px';
    IN_CARD = -1;
    IN_CARD_NAME = '';
    DRAWGAME = DRAWGAME.replace(card.name + ',', "");
  } else if (IN_CARD == -1 || MULTI_RAISE == 1) { //raise card
    if (document.getElementById('addDrawBTN').innerHTML == 'Add Game') {
      card.style.top = '-30px';
      IN_CARD = cardPos;
      IN_CARD_NAME = card.name;
      DRAWGAME += card.name + ',';
    }
  } else if (IN_CARD != -1) { //move card
    var cardsObj = document.getElementById('cardsDiv');
    var childs = cardsObj.getElementsByTagName('button');
    var cardList = [];
    for (var i = 0; i < childs.length; i++) {
      if (i == IN_CARD) continue;
      else if (i == cardPos) {
        cardList.push(childs[cardPos].name);
        cardList.push(childs[IN_CARD].name);
      } else
        cardList.push(childs[i].name);
    }
    var startPos = 150;
    cardsObj.innerHTML = '';
    CARDS = '';
    for (var i = 0; i < cardList.length; i++) {
      var rnd = Math.ceil(Math.random() * 100000);
      cardsObj.innerHTML += '<button type="button" class="card" name="' + cardList[i] + '" id="card' + cardList[i] + rnd + '" style="left: ' + startPos + 'px;" onclick="raiseCard(this);"><img src="/static/img/cards/d' + cardList[i] + '.png"></button>';
      startPos += 40;
      CARDS += cardList[i] + ',';
    }
    IN_CARD = -1;
    IN_CARD_NAME = '';
    DRAWGAME = '';
  }
}

function moveCard(card, dest, oper) {
  card.style.zIndex = 100;
  var id = setInterval(frame, 1);
  var rectStart = card.getBoundingClientRect();
  var rectEnd = dest.getBoundingClientRect();
  // start pósition and direction left -1, right 1
  var c = 0;
  const w = card.offsetWidth * 2 + dest.offsetWidth;
  var pos = rectStart.left;
  if(oper == 'drawOver')
  pos = w;
  else if (oper == 'deck')
  pos = 0;
  var posY = 0;
  var xDir = -1;
  var yDir = -1;
  const lim = 100;
  //get the increase steps X
  if (rectEnd.left > rectStart.left) {
    posXStep = Math.floor((rectEnd.left - rectStart.left - w) / lim);
    xDir = 1;
  } else
    posXStep = Math.floor((rectStart.left - rectEnd.left) / lim);
  //get the increase steps Y
  if (rectEnd.top > rectStart.top) {
    posYStep = Math.floor((rectEnd.top - rectStart.top) / lim);
    yDir = 1;
  } else
    posYStep = Math.floor((rectStart.top - rectEnd.top) / lim);
  // if (oper == 'pick' && (dest.id == 'player2Div' || dest.id == 'player3Div' || dest.id == 'player5Div')) {
  //   posYStep = 1;
  //   posY = -50;
  // } else if (oper == 'drawOver') {
  //   posXStep *= 2;
  //   posYStep = 1;
  // }
  if (oper == 'deck')
    posXStep = 0;
  else if (oper == 'drawOver')
    posXStep = 0;

  function frame() {
    if (c == lim) {
      //end at 100 steps
      clearInterval(id);
      if (oper == "discard")
        discardAfter(card, dest);
      else if (oper == 'pick')
        pickAfter(card, dest);
      else if (oper == "deck")
        deckAfter(card, dest);
      else if (oper == "drawOver")
        drawOverAfter(card);
    } else {
      pos += (posXStep * xDir);
      posY += (posYStep * yDir);
      card.style.left = pos + "px";
      card.style.top = posY + "px";
      c++;
    }
  }
}
//Move Cards Ends

//Player Moves Pick, Discard Draw, DrawOver Lonclick
function discard(cardId, discardId) {
  var discardDiv = document.getElementById(discardId);
  if (cardId == 'INCARD' && IN_CARD != -1) {
    var childs = document.getElementById('cardsDiv').getElementsByTagName('button');
    var card = childs[IN_CARD];
  } else {
    var card = document.getElementById(cardId);
    if (typeof card === "undefined" || card == null) {
      return false;
    }
    card.style.display = 'block';
    card.src = '/static/img/cards/d' + card.name + ".png";
  }
  if (typeof card === "undefined" || card == null) {
    return false;
  }
  moveCard(card, discardDiv, 'discard');
}

function discardAfter(card, discardDiv) {
  var rnd = Math.ceil(Math.random() * 4);
  var classRotate = 'rotateimg10';
  if (rnd == 1)
    classRotate = 'rotateimg20';
  if (rnd == 2)
    classRotate = 'rotateimg30';
  if (rnd == 3)
    classRotate = 'rotateimg40';
  discardDiv.innerHTML += '<img src="/static/img/cards/d' + card.name + '.png" class="card-discard ' + classRotate + '">';
  try {
    document.getElementById(card.parentElement.id).removeChild(card);
  } catch (e) {}
  CARDS = CARDS.replace(card.name + ",", "");
  handCards();
}

function pick(discardId, dest) {
  var childs = document.getElementById(discardId).getElementsByTagName('img');
  var card = childs[childs.length - 1];
  if (typeof card === "undefined" || card == null) {
    return false;
  }
  card.style.height = '100px';
  card.classList.remove('rotateimg10');
  card.classList.remove('rotateimg20');
  card.classList.remove('rotateimg30');
  card.classList.remove('rotateimg40');
  if (dest == 'cardsDiv') {
    var childs = document.getElementById(dest).getElementsByTagName('button');
    discardDiv = childs[childs.length - 1];
  } else
    discardDiv = document.getElementById(dest);
  moveCard(card, discardDiv, 'pick');
}

function pickAfter(card, cardsObj) {
  try {
    document.getElementById(card.parentElement.id).removeChild(card);
  } catch (e) {}
  if (cardsObj.id == 'player2Div' || cardsObj.id == 'player3Div' || cardsObj.id == 'player4Div' || cardsObj.id == 'player5Div')
    return;
  var rnd = Math.ceil(Math.random() * 4);
  var cardsObj = document.getElementById('cardsDiv');
  if (IN_CARD_SIDE == 1) {
    var aux = cardsObj.innerHTML;
    cardsObj.innerHTML = '<button type="button" class="card" name="' + card.name + '" id="card' + card.name + rnd + '" onclick="raiseCard(this);"><img src="/static/img/cards/d' + card.name + '.png"></button>' + aux;
  } else
    cardsObj.innerHTML += '<button type="button" class="card" name="' + card.name + '" id="card' + card.name + rnd + '" onclick="raiseCard(this);"><img src="/static/img/cards/d' + card.name + '.png"></button>';
  CARDS += card.name + ",";
  handCards();
}

function deck(cardName, dest) {
  var deckDiv = document.getElementById('deckDiv');
  var cardsObj = document.getElementById(dest);
  var cc = 'red_back';
  if (dest == 'cardsDiv')
    cc = 'd' + cardName;
  deckDiv.innerHTML += '<img id="deck-card" src="/static/img/cards/' + cc + '.png" height="60" class="card">';
  var card = document.getElementById('deck-card');
  card.name = cardName;
  moveCard(card, cardsObj, 'deck');
}

function deckAfter(card, cardsObj) {
  try {
    document.getElementById(card.parentElement.id).removeChild(card);
  } catch (e) {}
  if (cardsObj.id != 'cardsDiv')
    return;
  var rnd = Math.ceil(Math.random() * 100000);
  if (IN_CARD_SIDE == 1) {
    var aux = cardsObj.innerHTML;
    cardsObj.innerHTML = '<button type="button" class="card" name="' + card.name + '" id="card' + card.name + rnd + '" onclick="raiseCard(this);"><img src="/static/img/cards/d' + card.name + '.png"></button>' + aux;
  } else
    cardsObj.innerHTML += '<button type="button" class="card" name="' + card.name + '" id="card' + card.name + rnd + '" onclick="raiseCard(this);"><img src="/static/img/cards/d' + card.name + '.png"></button>';
  if (cardsObj.id == 'cardsDiv') {
    CARDS += card.name + ",";
    handCards();
  }
}

function drawOver(cardName) {
  var childs = document.getElementById('cardsDiv').getElementsByTagName('button');
  var card = childs[IN_CARD];
  var cardDiv = document.getElementById('cardsDiv');
  if (typeof card === "undefined" || card == null) {
    return false;
  }
  moveCard(card, document.getElementById('deckDiv'), 'drawOver');
}

function drawOverAfter(card, cardsObj) {
  try {
    cardsObj.removeChild(card);
  } catch (e) {}
  CARDS = CARDS.replace(card.name + ",", "")
  handCards();
}

function setLongClicks() {
  var pressTimer;
  $("#discard1BTN").mouseup(function() {
    clearTimeout(pressTimer);
    // Clear timeout
    return false;
  }).mousedown(function() {
    // Set timeout
    pressTimer = window.setTimeout(function() {
      LONG = true;
      showPreview("discard1BTN");
    }, 500);
    LONG = false;
    return false;
  });
  $("#discard2BTN").mouseup(function() {
    clearTimeout(pressTimer);
    // Clear timeout
    return false;
  }).mousedown(function() {
    // Set timeout
    pressTimer = window.setTimeout(function() {
      LONG = true;
      showPreview("discard2BTN");
    }, 500);
    LONG = false;
    return false;
  });
  $("#discard3BTN").mouseup(function() {
    clearTimeout(pressTimer);
    // Clear timeout
    return false;
  }).mousedown(function() {
    // Set timeout
    pressTimer = window.setTimeout(function() {
      LONG = true;
      showPreview("discard3BTN");
    }, 500);
    LONG = false;
    return false;
  });
  $("#discard4BTN").mouseup(function() {
    clearTimeout(pressTimer);
    // Clear timeout
    return false;
  }).mousedown(function() {
    // Set timeout
    pressTimer = window.setTimeout(function() {
      LONG = true;
      showPreview("discard4BTN");
    }, 500);
    LONG = false;
    return false;
  });
  $("#discard5BTN").mouseup(function() {
    clearTimeout(pressTimer);
    // Clear timeout
    return false;
  }).mousedown(function() {
    // Set timeout
    pressTimer = window.setTimeout(function() {
      LONG = true;
      showPreview("discard5BTN");
    }, 500);
    LONG = false;
    return false;
  });
  $("#draw1Div").mouseup(function() {
    clearTimeout(pressTimer);
    // Clear timeout
    return false;
  }).mousedown(function() {
    // Set timeout
    pressTimer = window.setTimeout(function() {
      LONG = true;
      showPreview("draw1Div", 'button');
    }, 500);
    LONG = false;
    return false;
  });
  $("#draw2Div").mouseup(function() {
    clearTimeout(pressTimer);
    // Clear timeout
    return false;
  }).mousedown(function() {
    // Set timeout
    pressTimer = window.setTimeout(function() {
      LONG = true;
      showPreview("draw2Div", 'button');
    }, 500);
    LONG = false;
    return false;
  });
  $("#draw3Div").mouseup(function() {
    clearTimeout(pressTimer);
    // Clear timeout
    return false;
  }).mousedown(function() {
    // Set timeout
    pressTimer = window.setTimeout(function() {
      LONG = true;
      showPreview("draw3Div", 'button');
    }, 500);
    LONG = false;
    return false;
  });
  $("#draw4Div").mouseup(function() {
    clearTimeout(pressTimer);
    // Clear timeout
    return false;
  }).mousedown(function() {
    // Set timeout
    pressTimer = window.setTimeout(function() {
      LONG = true;
      showPreview("draw4Div", 'button');
    }, 500);
    LONG = false;
    return false;
  });
  $("#draw5Div").mouseup(function() {
    clearTimeout(pressTimer);
    // Clear timeout
    return false;
  }).mousedown(function() {
    // Set timeout
    pressTimer = window.setTimeout(function() {
      LONG = true;
      showPreview("draw5Div", 'button');
    }, 500);
    LONG = false;
    return false;
  });

}
//Player Moves Ends

//Display Cards
function handCards() {
  var cardsObj = document.getElementById('cardsDiv');
  var cardsList = CARDS.split(",");
  var startPos = 150;
  cardsObj.innerHTML = '';
  for (var i = 0; i < cardsList.length; i++) {
    if (cardsList[i] == '')
      continue;
    var rnd = Math.ceil(Math.random() * 100000);
    cardsObj.innerHTML += '<button type="button" class="card" name="' + cardsList[i] + '" id="card' + cardsList[i] + rnd + '" style="left: ' + startPos + 'px;" onclick="raiseCard(this);"><img src="/static/img/cards/d' + cardsList[i] + '.png"></button>';
    startPos += 40;
  }
}

function setDiscard(cardsList1, discardDiv) {
  var cardsObj = document.getElementById(discardDiv);
  var cardsList = cardsList1.split(",");
  var i = 0;
  if (cardsList1.length == '') {
    cardsObj.innerHTML = '';
    return;
  }
  var tmpDiscard = '';
  for (; i < cardsList.length; i++) {
    if (cardsList[i] == '') continue;
    var rnd = Math.ceil(Math.random() * 5);
    var classRotate = '';
    if (rnd == 1)
      classRotate = 'rotateimg10';
    else if (rnd == 2)
      classRotate = 'rotateimg20';
    else if (rnd == 3)
      classRotate = 'rotateimg30';
    else if (rnd == 4)
      classRotate = 'rotateimg40';
    tmpDiscard += '<img src="/static/img/cards/d' + cardsList[i] + '.png" name="' + cardsList[i] + '" class="card-discard ' + classRotate + '">';
  }
  //check if discard changed
  if (tmpDiscard.replace(/rotateimg10/g, '').replace(/rotateimg20/g, '').replace(/rotateimg30/g, '').replace(/rotateimg40/g, '') != cardsObj.innerHTML.replace(/rotateimg10/g, '').replace(/rotateimg20/g, '').replace(/rotateimg30/g, '').replace(/rotateimg40/g, ''))
    cardsObj.innerHTML = tmpDiscard;
}

function drawCards(cardsList1, discardDiv) {
  var cardsObj = document.getElementById(discardDiv);
  var games = cardsList1.split("|");
  var startPos = 0;
  var tmpDraw = '';
  var pos = 0;
  for (g = 0; g < games.length; g++) {
    var cardsList = games[g].split(",");
    for (var i = 0; i < cardsList.length; i++) {
      if (cardsList[i] == '')
        continue;
      var jokerPos = 0;
      if (i >= cardsList.length - 2) jokerPos = 1;
      tmpDraw += '<button type="button" class="card" name="' + cardsList[i] + '" style="left: ' + startPos + 'px;" onclick="callDrawOver(\'' + discardDiv + '\', ' + pos + ', ' + jokerPos + ');"><img src="/static/img/cards/d' + cardsList[i] + '.png"></button>';
      startPos += 20;
    }
    startPos += 40;
    pos++;
  }
  if (tmpDraw != cardsObj.innerHTML)
    cardsObj.innerHTML = tmpDraw;
}

function drawPreCards(cardsList1, discardDiv) {
  var cardsObj = document.getElementById(discardDiv);
  var cardsList = cardsList1.split(",");
  var startPos = 20;
  //cardsObj.innerHTML = '';
  for (var i = 0; i < cardsList.length; i++) {
    if (cardsList[i] == '')
      continue;
    cardsObj.innerHTML += '<button type="button" class="card-pre" name="' + cardsList[i] + '" style="left: ' + startPos + 'px;"><img src="/static/img/cards/d' + cardsList[i] + '.png"></button>';
    startPos += 10;
  }
}

function showPreview(discardDiv, type = 'img') {
  var previewObj = document.getElementById('preview-div');
  var childs = document.getElementById(discardDiv).getElementsByTagName(type);
  var startPos = 50;
  previewObj.innerHTML = '';
  for (var i = 0; i < childs.length; i++) {
    if (type == 'button')
      pos = childs[i].style.left;
    else
      pos = startPos + 'px';
    previewObj.innerHTML += '<img src="/static/img/cards/d' + childs[i].name + '.png"class="card-prev" style="left: ' + pos + '">';
    startPos += 30;
  }
  previewObj.style.display = 'block';
}
//Display Cards Ends

// Menu Buttons
function sortCards(color = false) {
  var cardsObj = document.getElementById('cardsDiv');
  var childs = cardsObj.getElementsByTagName('button');
  var cardList = [];
  for (var i = 0; i < childs.length; i++) {
    cardList.push(fixSort(childs[i].name, true, color));
  }
  cardList.sort();
  cardList1 = '';
  var startPos = 150;
  cardsObj.innerHTML = '';
  CARDS = '';
  for (var i = 0; i < cardList.length; i++) {
    cardList1 = fixSort(cardList[i], false, color);
    var rnd = Math.ceil(Math.random() * 100000);
    cardsObj.innerHTML += '<button type="button" class="card" name="' + cardList1 + '" id="card' + cardList1 + rnd + '" style="left: ' + startPos + 'px;" onclick="raiseCard(this);"><img src="/static/img/cards/d' + cardList1 + '.png"></button>';
    startPos += 40;
    CARDS += cardList1 + ',';
  }
  if (color)
    showNotify("Sorted by colors");
  else
    showNotify("Sorted by numbers");
}

function fixSort(card, start, color) {
  if (start || (!start && !color)) {
    var nn = card.substring(0, 1);
    var cc = card.substring(1, 2);
  } else {
    var nn = card.substring(1, 2);
    var cc = card.substring(0, 1);
  }
  if (start) {
    if (nn == "a")
      nn = "y";
    if (nn == "k")
      nn = "r";
    if (nn == "0")
      nn = "h";
    if (nn == "x")
      nn = "z";
  } else {
    if (nn == "y")
      nn = "a";
    if (nn == "r")
      nn = "k";
    if (nn == "h")
      nn = "0";
    if (nn == "z")
      nn = "x";
  }
  if (color && start && cc == 'd') {
    cc = 'b';
  } else if (color && cc == 'b') {
    cc = 'd';
  }
  //if sorting by color put colors letter first, or restore back
  if (color && start)
    return cc + nn;
  else
    return nn + cc;
}

function inSide() {
  if (IN_CARD_SIDE == 1) {
    IN_CARD_SIDE = 0;
    showNotify("In Cards placed at end");
  } else {
    IN_CARD_SIDE = 1;
    showNotify("In Cards placed at beggining");
  }
}

function gameSummary(winner = '', winAux) {
  if (document.getElementById('game-summary-div').style.display == 'block') return;
  var standings = '<div class="row col-sm-12"><h4 class="col-sm-2">#</h4>';
  var playersTotal = [0, 0, 0, 0, 0];
  for (var i = 0; i < PLAYERSNAMES.length; i++)
    if (PLAYERSNAMES[i] != '')
      standings += '<h4 class="col-sm-2">' + PLAYERSNAMES[i] + '</h4>';
  standings += '</div>';
  var set = SET;
  for (var i = 0; i < set; i++) {
    var color = 'red';
    if (FULLDRAW.substring(i, i + 1) == '1')
      color = 'blue';
    standings += '<div class="row col-sm-12"><h4 class="col-sm-2">' + (i + 1) + '</h4>';
    for (var j = 0; j < PLAYERSSTANDINGS[i].length; j++) {
      if (PLAYERSSTANDINGS[i][j] != -1) {
        var colorW = '';
        if (PLAYERSSTANDINGS[i][j] == 0)
          colorW = color;
        standings += '<h4 class="col-sm-2"><font color="' + colorW + '">' + PLAYERSSTANDINGS[i][j] + '</font></h4>';
        playersTotal[j] += parseInt(PLAYERSSTANDINGS[i][j]);
      }
    }
    standings += '</div>';
  }
  standings += '<div class="row col-sm-12"><h4 class="col-sm-2">TOTAL</h4>';
  for (var i = 0; i < PLAYERS.length; i++)
    if (PLAYERS[i] != '')
      standings += '<h4 class="col-sm-2">' + playersTotal[i] + '</h4>';
  standings += '</div>';
  document.getElementById('summaryBody').innerHTML = standings;
  if (winner != '') {
    document.getElementById('summaryTitle').innerHTML = winner;
    if (winAux) {
      if (winner == 'Congrats, You Won this Set')
        callFlow(PLAYERSNAMES[0] + '||--||' + 8 + '||--||');
      else
        callFlow(winner.replace('Sorry, ', "").replace(' Won this Set', '') + '||--||' + 8 + '||--||');
    }
  }
  var ww = 0;
  var min = 10000000;
  if (set == 6) {
    for (var i = 0; i < PLAYERS.length; i++) {
      if (PLAYERS[i] == '') continue;
      if (playersTotal[i] < min) {
        ww = i;
        min = playersTotal[i];
      }
    }
    if (ww == 0 && STARTED == 2)
      document.getElementById('summaryTitle').innerHTML = 'Congrats, YOU WON THE GAME!!!!!!!!!';
    else if(STARTED == 2)
      document.getElementById('summaryTitle').innerHTML = 'Sorry, ' + PLAYERSNAMES[ww] + ' Won the Game!';
    if (winAux) {
      if (ww == 0)
        callFlow(PLAYERSNAMES[0] + '||--||' + 9 + '||--||');
      else
        callFlow(PLAYERSNAMES[ww] + '||--||' + 9 + '||--||');
    }
  }
  document.getElementById('game-summary-div').style.display = 'block';
}

function setInfo() {
  var info = '<h2>This is Game %%GAME%%<h2><h4>You need to draw %%GAMES%%</h4><h4>This Game %%FULLDRAW%% fulldraw</h4>';
  if (SET == 1)
    info = info.replace('%%GAME%%', 'First').replace("%%GAMES%%", "One Straight and One Three of a kind");
  else if (SET == 2)
    info = info.replace('%%GAME%%', 'Second').replace("%%GAMES%%", "Three Three of a kind");
  else if (SET == 3)
    info = info.replace('%%GAME%%', 'Thrid').replace("%%GAMES%%", "One Straight and Two Three of a kind");
  else if (SET == 4)
    info = info.replace('%%GAME%%', 'Fourth').replace("%%GAMES%%", "Two Straight");
  else if (SET == 5)
    info = info.replace('%%GAME%%', 'Fifth').replace("%%GAMES%%", "Two Straight and One Three of a kind");
  else if (SET == 6)
    info = info.replace('%%GAME%%', 'Sixth').replace("%%GAMES%%", "Three Straight");
  if (FULLDRAW.substring(SET - 1, SET) == '1')
    info = info.replace('%%FULLDRAW%%', 'IS');
  else
    info = info.replace('%%FULLDRAW%%', 'is NOT');
  var obj = document.getElementById("set-info-div");
  obj.innerHTML = info;
  obj.style.display = 'block';
}

function showMessages() {
  var objMsg = document.getElementById('messages-div');
  if (objMsg.style.display == 'block')
    objMsg.style.display = 'none';
  else
    objMsg.style.display = 'block';
  objMsg.scrollTop = objMsg.scrollHeight;
}
// Menu Buttons Ends

//Variables
var SET = 0;
var INI = '';
var EMAIL = '';
var USERID = 0;
var GAMEID = 0;
var MYTURN = false;
var STARTED = 0;
var PLAYER = [];
var PLAYERSNAMES = [];
var PLAYERSSTANDINGS = [
  [-1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1]
];
var NUMPLAYERS = 0;
var CARDS = '';
var FETCHING = 0;
var LASTID = 0;
var LASTIDF = 0;
var IN_CARD = -1;
var IN_CARD_NAME = '';
var MULTI_RAISE = 0;
var MOVE_STATUS = 1;
var DRAWGAME = '';
var DRAW = '';
var TMP_CARD = '';
var FULLDRAW = '000000';
var NEWDRAW = false;
var IN_CARD_SIDE = 0;
var LONG = false;
var MESSAGES = [];
var MESS_LASTD = 0;
var RECORDING = false;
var TITLE = '';
var audio = new Audio();

function setVars(userId, email, gameId) {
  EMAIL = email;
  USERID = userId;
  GAMEID = gameId;
}

//Update Remote Data
function fetchData() {
  FETCHING++;
  if (FETCHING > 4) FETCHING = 0;
  if (FETCHING > 1) return;
  var data = 'usernameUser=' + EMAIL + '&oper=bundleData&version=web&gameId=' + GAMEID + '&lastId=' + LASTID + '&lastIdF=' + LASTIDF + '&set=' + SET;
  callUrl(data, 1);
  return STARTED;
}

function callUrl(data, oper) {
  var url = 'https://rummi.theozserver.com/API/app/fetch/';
  if (window.XMLHttpRequest) {
    // code for IE7+, Firefox, Chrome, Opera, Safari
    var xmlhttp = new XMLHttpRequest();
  } else {
    // code for IE6, IE5
    var xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
  }
  xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
      urlResponse(xmlhttp.responseText, oper);
      FETCHING = 0;
    }
  };
  xmlhttp.open("POST", url, true);
  xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xmlhttp.setRequestHeader("X-CSRFToken", document.getElementsByName('csrfmiddlewaretoken')[0].value);
  xmlhttp.send(data);
  return false;
}

//Remote Data Response
function urlResponse(data, oper) {
  var res = data.split("|");
  // background update
  if (oper == 1 && data.substring(0, 2) != '--')
    updateInfo(data);
  // pick from deck
  else if (oper == 2 && res.length == 2) {
    TMP_CARD = res[1].toLowerCase();
    deck(res[1].toLowerCase(), 'cardsDiv');
    IN_CARD = -1;
    IN_CARD_NAME = '';
    callFlow(PLAYERSNAMES[0] + '||--||' + 3 + '||--||');
    // discard
  } else if (oper == 3 && res.length == 2) {
    TMP_CARD = IN_CARD_NAME;
    discard('INCARD', 'discard2BTN', 'cardsDiv');
    callFlow(PLAYERSNAMES[0] + '||--||' + 5 + '||--||' + IN_CARD_NAME.toUpperCase());
    IN_CARD = -1;
    IN_CARD_NAME = '';
    // pick from discard
  } else if (oper == 4 && res.length == 2) {
    TMP_CARD = res[1].toLowerCase();
    pick('discard1BTN', 'cardsDiv');
    callFlow(PLAYERSNAMES[0] + '||--||' + 4 + '||--||' + IN_CARD_NAME.toUpperCase());
    IN_CARD = -1;
    IN_CARD_NAME = '';
    // draw game
  } else if (oper == 5 && res.length == 2) {
    drawCards(DRAW.toLowerCase(), 'draw1Div');
    IN_CARD = -1;
    IN_CARD_NAME = '';
    var cardsList = DRAW.replace("|", "").toLowerCase().split(",");
    for (var i = 0; i < cardsList.length; i++) {
      if (cardsList[i] == "")
        continue;
      CARDS = CARDS.replace(cardsList[i] + ",", "")
    }
    cancelDraw(document.getElementById('mainBTN'));
    handCards();
    callFlow(PLAYERSNAMES[0] + '||--||' + 7 + '||--||');
    // draw Over card
  } else if (oper == 6 && res.length == 2) {
    drawOver(IN_CARD_NAME);
    callFlow(PLAYERSNAMES[0] + '||--||' + 6 + '||--||' + IN_CARD_NAME.toUpperCase());
    IN_CARD = -1;
    IN_CARD_NAME = '';
  } else if (oper == 7 && res.length == 2) {
    handCards();
    callFlow(PLAYERSNAMES[0] + '||--||' + 2 + '||--||');
  } else if (oper == 9 && res.length == 2) // deal Cards
    callFlow(PLAYERSNAMES[0] + '||--||' + 1 + '||--||');
  else if (oper != 8)
    showNotify(data);
}

//Game Info
function updateInfo(dataAux) {
  var dataAux = dataAux.split("\n");
  var data = [];
  var opc = 0;
  var valNewSet = SET;
  var winner = '';
  for (var i = 0; i < dataAux.length; i++) {
    if (dataAux[i] == '')
      continue;
    data[i] = JSON.parse(dataAux[i]);
    if (i == 0) {
      //get current set
      SET = data[0].current_set;
      MOVE_STATUS = data[0].moveStatus;
      initualMisc(data[0]);
      // set main info from game
      if (INI == '' || STARTED == 0) {
        PLAYERS = data[0].playersPos.split(",");
        PLAYERSNAMES = data[0].names.split(",");
        startPlayers(data[0]);
        startDiscards(data[0]);
        FULLDRAW = data[0].fullDraw;
        TITLE = data[0].name;
      }
      //update discards
      updDiscards(data[0]);
      //check turn
      if (PLAYERS[data[0].currentPlayerPos] == USERID)
        MYTURN = true;
      else
        MYTURN = false;
      //game started?
      STARTED = data[0].started;
      gameStatus(data[0]);
    } else {
      //set record type, 0 set info, 1, meesage, 2, flow
      if (data[i].messages == '1') {
        opc = 1;
        continue;
      } else if (data[i].flow == '1') {
        opc = 2;
        continue;
      }
      if (opc == 0) { //game set info
        //process at each update
        if (SET == data[i].set_set) {
          //update cards if current player
          if (USERID == data[i].set_userId_id && INI != '')
            updCards(data[i].set_current_cards.toLowerCase());
          //don't update if new draw, set just ended
          if (!NEWDRAW) {
            //check draws
            updDraw(data[i].set_drawn, data[i].set_userId_id);
          }

        }
        //check if set ended
        if (!NEWDRAW && ((SET - 1) == data[i].set_set || data[i].set_set == 6) && data[i].set_current_cards.length < 2 && INI != '') {
          if (USERID == data[i].set_userId_id)
            winner = 'Congrats, You Won this Set';
          else {
            for (var pi = 0; pi < PLAYERS.length; pi++)
              if (PLAYERS[pi] == data[i].set_userId_id) {
                winner = 'Sorry, ' + PLAYERSNAMES[pi] + ' Won this Set';
                break;
              }
          }
          NEWDRAW = true;
          INI = '';
        }
        //set player cards count
        setPlayerCardsCount(data[i].set_userId_id, data[i].set_current_cards);
        // process only the first time
        //set summary info
        PLAYERSSTANDINGS[data[i].set_set - 1][PLAYERS.indexOf(data[i].set_userId_id)] = data[i].set_points;
        if (INI != '')
          continue;
        //if current user
        if (USERID == data[i].set_userId_id && SET == data[i].set_set) {
          CARDS = data[i].set_current_cards.toLowerCase();
          handCards();
        }
      } else if (opc == 1) { //messages
        LASTID = parseInt(data[i].id) + 1;
        if (INI == '')
          MESSAGES.push(data[i]);
        else
          addMessage(data[i]);
      } else if (opc == 2) { // flow messages
        LASTIDF = parseInt(data[i].id) + 1;
        if (INI == '')
          MESSAGES.push(data[i]);
        else
          addFlowMessage(data[i]);
      }
    }
  }
  var winAux = false;
  if (data[0].userId_id == USERID) winAux = true;
  if (winner != '') gameSummary(winner, winAux);
  if (INI == '' && MESS_LASTD == 0)
    putMessages();
  INI = 'OFF';
}

function gameStatus(data) {
  var mainInfo = document.getElementById('mainInfo');
  var btn = document.getElementById('mainBTN');
  btn.innerHTML = '';
  btn.style.display = 'none';
  document.title = 'Rummi | ' + TITLE;
  mainInfo.style.backgroundColor = "gray";
  if (STARTED == '2') //game Ended
    mainInfo.innerHTML = 'Game Ended<br />';
  else if (MYTURN) {
    mainInfo.classList.add("blink");
    mainInfo.style.backgroundColor = "#c73232";
    mainInfo.innerHTML = "It's Your turn!!!";
    document.title += ' ****';
    if (STARTED == '0') { //Game not started
      mainInfo.innerHTML = 'Waiting for Players...<br />Game Code: ' + data.code;
      btn.innerHTML = 'Start Game';
    } else if (data.current_stack == '') { //game Started, user is dealing
      mainInfo.innerHTML += '<br>Deal cards!';
      btn.innerHTML = 'Deal Cards';
    } else if (data.moveStatus == '1') // user turn to pick card
      mainInfo.innerHTML += '<br>Pick a card!';
    else if (MULTI_RAISE == 1)
      btn.innerHTML = 'Cancel';
    else if (document.getElementById('draw1Div').innerHTML == '') { //user turn to discard, not Drawn
      mainInfo.innerHTML += '<br>Discard a card or Draw!';
      btn.innerHTML = 'Draw';
    } else //user turn to discard, already Drawn
      mainInfo.innerHTML += '<br>Discard a card or DrawOver!';
  } else { //Not user Turn
    mainInfo.classList.remove("blink");
    if (STARTED == '1' && data.current_stack == '')
      mainInfo.innerHTML = "Wating for " + PLAYERSNAMES[data.currentPlayerPos] + "<br /> to deal cards";
    else if (STARTED == '1')
      mainInfo.innerHTML = "Wating for  " + PLAYERSNAMES[data.currentPlayerPos] + "<br /> to move";
    else if (STARTED == '0')
      mainInfo.innerHTML = 'Waiting for Players...<br />Game Code: ' + data.code;
  }
  if (btn.innerHTML != '')
    btn.style.display = 'block';
  document.getElementById('shareBTN').style.display = 'none';
  if (STARTED == '0')
    document.getElementById('shareBTN').style.display = 'block';
}

function updCards(data) {
  if (data.split(",").sort().toString() != CARDS.split(",").sort().toString()) {
    // check if just discarded
    if ((data + TMP_CARD + ",").split(",").sort().toString() != CARDS.split(",").sort().toString()) {
      // check if just pick
      if (data.split(",").sort().toString() != (CARDS + TMP_CARD + ",").split(",").sort().toString()) {
        CARDS = data;
        handCards();
        if (CARDS != '' && NEWDRAW) {
          document.getElementById('draw1Div').innerHTML = '';
          document.getElementById('draw2Div').innerHTML = '';
          document.getElementById('draw3Div').innerHTML = '';
          document.getElementById('draw4Div').innerHTML = '';
          document.getElementById('draw5Div').innerHTML = '';
          NEWDRAW = false;
        }
      }
    }
  }
}

function updDiscards(gameData) {
  var discards = gameData.current_discarded.split("|");
  var pos = 0;
  var lastP = 0;
  for (var i = 0; i <= 4; i++) {
    if (PLAYERS[i] == '') continue;
    lastP++;
    pos = i + 2;
    if (i == 4 || lastP == NUMPLAYERS) pos = 1;
    setDiscard(discards[i].toLowerCase(), 'discard' + pos + 'BTN');
  }
}

function updDraw(cards, userId, force = false) {
  if (cards == '' && !force) return;
  if (USERID == userId)
    document.getElementById('mainBTN').style.display = 'none';
  drawCards(cards.toLowerCase(), 'draw' + (PLAYERS.indexOf(userId) + 1) + 'Div');
}

function setPlayerCardsCount(userId, cards) {
  var cardsCount = cards.split(",").length - 1;
  var i = PLAYERS.indexOf(userId);
  document.getElementById('player' + (i + 1) + 'Name').innerHTML = PLAYERSNAMES[i] + "(" + cardsCount + ")";
}

//Game Info Ends

//Player Clicks
function callStartGame() {
  var data = 'usernameUser=' + EMAIL + '&oper=startGame&version=web&gameId=' + GAMEID;
  callUrl(data, 9);
}

function callDeck() {
  var data = 'usernameUser=' + EMAIL + '&oper=pickCard&stack=1&version=web&gameId=' + GAMEID;
  callUrl(data, 2);
}

function callDiscard() {
  if (LONG) return false;
  var data = 'usernameUser=' + EMAIL + '&oper=discardCard&version=web&gameId=' + GAMEID + '&out=' + IN_CARD_NAME.toUpperCase();
  callUrl(data, 3);
}

function callPick() {
  if (LONG) return false;
  var data = 'usernameUser=' + EMAIL + '&oper=pickCard&discard=1&version=web&gameId=' + GAMEID;
  callUrl(data, 4);
}

function callDraw() {
  var data = 'usernameUser=' + EMAIL + '&oper=draw&&version=web&gameId=' + GAMEID + '&drawCards=' + DRAW;
  callUrl(data, 5);
}

function callDrawOver(drawDiv, drawPos, jokerPos) {
  if (LONG) return false;
  var data = 'usernameUser=' + EMAIL + '&oper=drawOver&&version=web&gameId=' + GAMEID + '&drawPos=' + drawPos + '&pos=' + jokerPos + '&in=' + IN_CARD_NAME.toUpperCase() + '&drawUserId=' + (PLAYERS[drawDiv.replace("draw", "").replace("Div", "") - 1]);
  callUrl(data, 6);
}

function callDeal() {
  var data = 'usernameUser=' + EMAIL + '&oper=dealCards&&version=web&gameId=' + GAMEID;
  callUrl(data, 7);
}

function callMsg(msg) {
  var data = 'usernameUser=' + EMAIL + '&oper=addMessage&&version=web&gameId=' + GAMEID + '&msg=' + msg;
  callUrl(data, 8);
}

function callFlow(msg) {
  var data = 'usernameUser=' + EMAIL + '&oper=addToFlow&version=web&gameId=' + GAMEID + '&msg=' + msg;
  callUrl(data, 8);
}

function mainButton() {
  var btn = document.getElementById('mainBTN');
  if (btn.innerHTML == 'Start Game')
    callStartGame();
  else if (btn.innerHTML == 'Draw')
    iniDraw(btn);
  else if (btn.innerHTML == 'Cancel')
    cancelDraw(btn);
  else if (btn.innerHTML == 'Deal Cards')
    callDeal(btn);
}

function iniDraw(btn) {
  MULTI_RAISE = 1;
  btn.innerHTML = 'Cancel';
  document.getElementById('draw-div').style.display = 'block';
}

function cancelDraw(btn) {
  MULTI_RAISE = 0;
  DRAW = '';
  DRAWGAME = '';
  btn.innerHTML = 'Draw';
  document.getElementById('addDrawBTN').innerHTML = 'Add Game';
  document.getElementById('draw-div').style.display = 'none';
  document.getElementById('drawPreDiv1').innerHTML = '';
  document.getElementById('drawPreDiv2').innerHTML = '';
  document.getElementById('drawPreDiv3').innerHTML = '';
  var childs = document.getElementById('cardsDiv').getElementsByTagName('button');
  for (var i = 0; i < childs.length; i++) {
    childs[i].style.top = '0px';
  }
}

function addDraw() {
  var btn = document.getElementById('addDrawBTN');
  if (btn.innerHTML == 'Add Game') {
    DRAW += DRAWGAME.toUpperCase() + '|';
    var games = DRAW.split("|").length - 1;
    document.getElementById('drawPreDiv' + games).innerHTML = '';
    drawPreCards(DRAWGAME, 'drawPreDiv' + games);
    DRAWGAME = '';
    if ((SET == 1 || SET == 4) && games == 2)
      btn.innerHTML = 'Confirm Draw';
    else if (games > 2)
      btn.innerHTML = 'Confirm Draw';
  } else {
    DRAW = DRAW.substring(0, DRAW.length - 1)
    callDraw();
  }
}
//Player Clicks Ends

//Start game setup
function startPlayers(gameData) {
  var playersExt = gameData.extensions.split(",");
  for (var i = 0; i <= 4; i++) { //set user info
    if (PLAYERS[i] != '') {
      NUMPLAYERS++;
      document.getElementById('player' + (i + 1) + 'Name').innerHTML = PLAYERSNAMES[i];
      if (playersExt[i] != '') {
        document.getElementById('player' + (i + 1) + 'BTN').innerHTML = '<img src="/static/playerAvatars/' + PLAYERS[i] + playersExt[i] + '" class="avatar"/>';
      } else
        document.getElementById('player' + (i + 1) + 'BTN').innerHTML = '<img src="/static/img/player.png" class="avatar"/>';
    } else { // Hide unused user
      document.getElementById('player' + (i + 1) + 'Div').style.display = 'none';
    }
  }
}

function startDiscards(gameData) {
  var discards = gameData.current_discarded.split("|");
  var pos = 0;
  for (var i = 1; i < 4; i++) //set user info
    if (PLAYERS[i] == '') // Hide unused discard
      document.getElementById('discard' + (i + 2) + 'BTN').style.display = 'none';
  if (PLAYERS[4] == '' && PLAYERS[3] == '' && PLAYERS[2] == '') {
    document.getElementById('discard3BTN').style.display = 'none';
    document.getElementById('discard4BTN').style.display = 'none';
    document.getElementById('discard5BTN').style.display = 'none';
  }
  if (PLAYERS[4] == '' && PLAYERS[3] == '') {
    document.getElementById('discard4BTN').style.display = 'none';
    document.getElementById('discard5BTN').style.display = 'none';
  }
  if (PLAYERS[4] == '') document.getElementById('discard5BTN').style.display = 'none';
}

function initualMisc(gameData) {
  var set = 'Fisrt';
  if (SET == 2) set = 'Second';
  if (SET == 3) set = 'Third';
  if (SET == 4) set = 'Fourth';
  if (SET == 5) set = 'Fith';
  if (SET == 6) set = 'Sixth';
  if (gameData.fullDraw.substring(SET - 1, SET) == '1')
    set += '**';
  document.getElementById('gameSetInfo').innerHTML = set;
}

//tools
function getDateF() {
  var d = new Date();
  var date = d.getFullYear() + "-";
  if (d.getMonth() < 10)
    date += "0" + (d.getMonth() + 1);
  else
    date += (d.getMonth() + 1);
  date += "-";
  if (d.getDate() < 10)
    date += "0" + d.getDate();
  else
    date += d.getHours();
  date += " ";
  if (d.getHours() < 10)
    date += "0" + d.getHours();
  else
    date += d.getMinutes();
  date += ":";
  if (d.getMinutes() < 10)
    date += "0" + d.getMinutes();
  else
    date += d.getSeconds();
  if (d.getSeconds() < 10)
    date += "0" + d.getSeconds();
  else
    date += d.getSeconds();
  return date;
}

function getCardName(card) {
  var color = '';
  if (card == "XX") return "Joker";
  if (card.substring(1, 2) == 'S') color = 'Spades';
  else if (card.substring(1, 2) == 'H') color = 'Hearts';
  else if (card.substring(1, 2) == 'D') color = 'Diamonds';
  else if (card.substring(1, 2) == 'C') color = 'Clubs';
  if (card.substring(0, 1) == '0') return "10 of " + color;
  else return card.substring(0, 1) + ' of ' + color;
}

function showNotify(msg, type = 'info') {
  $.notify({
    message: msg
  }, {
    // settings
    position: null,
    type: type,
    delay: 3000,
    placement: {
      from: "top",
      align: "center"
    }
  });
}

function blinker() {
  $('.blink').fadeOut(1500);
  $('.blink').fadeIn(1500);
}
setInterval(blinker, 3000);
