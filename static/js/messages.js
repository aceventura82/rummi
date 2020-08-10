function putMessages() {
  MESSAGES = MESSAGES.sort(function(a, b) {
    var c = new Date(a.date);
    var d = new Date(b.date);
    return c - d;
  });
  var i = 0;
  var interval = setInterval(function() {
    var valMsg = addMsgs(i);
    i += 20;
    if(valMsg == 1)
      clearInterval(interval);
  }, 500);
}

function addMsgs(i) {
  var lim = i + 20;
  if (lim > MESSAGES.length)
    lim = MESSAGES.length;
  for (; i < lim; i++) {
    if (MESS_LASTD != MESSAGES[i].date.substring(0, 10))
      document.getElementById('messages-in-div').innerHTML += '<div class="flow-text text-center"><p><strong>' + MESSAGES[i].date.substring(0, 10) + '</strong></p></div>';
    MESS_LASTD = MESSAGES[i].date.substring(0, 10);
    if (typeof MESSAGES[i].userId_id === 'undefined')
      addFlowMessage(MESSAGES[i], true);
    else
      addMessage(MESSAGES[i], true);
  }
  if (lim == MESSAGES.length) return 1;
  else return 0;
}

function addMessage(dataMsg, ini = false) {
  if (!ini && dataMsg.userId_id == PLAYERS[0]) return;
  var objMsg = document.getElementById('messages-in-div');
  var msg = '<div class="chat-text"><p>' + dataMsg.date.substring(11, 19) + ' <strong>' + PLAYERSNAMES[PLAYERS.indexOf(dataMsg.userId_id)] + ': </strong>';
  if (dataMsg.msg.substring(0, 9) == '::AUDIO::') {
    objMsg.innerHTML += msg + 'Speaking</p>';
    if (ini) return;
    var objAudio = document.getElementById('audios-img');
    objAudio.src = '/static/img/playing_audio.gif';
    objAudio.style.display = 'block';
    audio = new Audio('/static/audios/' + dataMsg.userId_id + '_' + GAMEID + '.wav?' + Math.ceil(Math.random() * 100000000));
    audio.play();
    $(audio).on("loadedmetadata", function() {
      setInterval(function() {
        objAudio.style.display = 'none';
      }, Math.floor(audio.duration) * 1000);
    });
    showNotify(PLAYERSNAMES[PLAYERS.indexOf(dataMsg.userId_id)] + 'Speaking', 'danger');
    return;
  }
  if (!ini)
    showNotify(PLAYERSNAMES[PLAYERS.indexOf(dataMsg.userId_id)] + ':' + decodeURI(dataMsg.msg), 'danger');
  objMsg.innerHTML += msg + decodeURI(dataMsg.msg) + '</p></div>';
  objMsg.scrollTop = objMsg.scrollHeight;
}

function addFlowMessage(dataMsg, ini = false) {
  var objMsg = document.getElementById('messages-in-div');
  var msgData = dataMsg.msg.split("||--||");
  if (msgData.length != 3) {
    return;
  }
  var msg = '<div class="flow-text"><p>' + dataMsg.date.substring(11, 19) + ' <strong>' + msgData[0] + ': </strong>';
  var notif = msg.length;
  if (msgData[1] == 1) msg += 'Game Starts</p>';
  else if (msgData[1] == 2) msg += 'Deal Cards</p>';
  else if (msgData[1] == 3) {
    msg += 'Picked card from Stack</p>';
    // if(INI != '') moveCardFromUsersDiscard("", currentUser, 3)
  } else if (msgData[1] == 4) {
    msg += 'Picked card ' + getCardName(msgData[2]) + ' from discard</p>';
    // if(INI != '') moveCardFromUsersDiscard("", currentUser, 3)
  } else if (msgData[1] == 5) {
    msg += 'Discarded card ' + getCardName(msgData[2]) + '</p>';
    // if(INI != '') moveCardFromUsersDiscard("", currentUser, 3)
  } else if (msgData[1] == 6) {
    msg += 'Draw Over card ' + getCardName(msgData[2]) + '</p>';
    // if(INI != '') moveCardFromUsersDiscard("", currentUser, 3)
  } else if (msgData[1] == 7) msg += 'Drawn Game</p>';
  else if (msgData[1] == 8) msg += 'Won the Set</p>';
  else if (msgData[1] == 9) msg += 'Won the Game</p>';
  else if (msgData[1] == 10) msg += 'Created the Game</p>';
  else if (msgData[1] == 11) msg += 'Joined the Game</p>';
  else msg += dataMsg + '</p>';
  if (!ini) {
    notif = msgData[0] + ':' + msg.substring(notif, msg.length - 4);
    showNotify(notif);
  }
  msg += '</div>';
  objMsg.innerHTML += msg;
  objMsg.scrollTop = objMsg.scrollHeight;
}

function sendMsg() {
  var objMsg = document.getElementById('send-msg');
  $('input[id=send-msg]').on('keydown', function(e) {
    if (e.which == 13 && objMsg != '') {
      e.preventDefault();
      callMsg(encodeURIComponent(objMsg.value));
      var dateNow = getDateF();
      var objInMsg = document.getElementById('messages-in-div');
      if (MESS_LASTD != dateNow.substring(0, 10))
        objInMsg.innerHTML += '<div class="flow-text text-center"><p><strong>' + dateNow.substring(0, 10) + '</strong></p></div>';
      objInMsg.innerHTML += '<div class="chat-text"><p>' + dateNow.substring(11, 19) + ' <strong>' + PLAYERSNAMES[0] + ': </strong>' + objMsg.value + '</p></div>';
      objMsg.value = '';
    }
  });
}
