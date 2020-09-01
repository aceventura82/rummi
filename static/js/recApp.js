var gumStream; 						//stream from getUserMedia()
var recorder; 						//WebAudioRecorder object
var input; 							//MediaStreamAudioSourceNode  we'll be recording
var encodingType; 					//holds selected encoding for resulting audio (file)
var encodeAfterRecord = true;       // when to encode

// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext; //new audio context to help us record

function recPressed() {
  const recBtn = document.getElementById('recBTN');
  var objAudio = document.getElementById('audios-img');
  if (!RECORDING) { // start recording
    document.getElementById('recBTN').innerHTML = '<i class="fa fa-stop" aria-hidden="true"></i>';
    RECORDING = true;
    startRecording();
    objAudio.src = '/static/img/recording.gif';
    objAudio.style.display = 'block';
  } else { // stop recording
    document.getElementById('recBTN').innerHTML = '<i class="fa fa-microphone" aria-hidden="true"></i>';
    RECORDING = false;
    objAudio.style.display = 'none';
    stopRecording();
  }
}

function startRecording() {

	/*
		Simple constraints object, for more advanced features see
		https://addpipe.com/blog/audio-constraints-getusermedia/
	*/

    var constraints = { audio: true, video:false }

    /*
    	We're using the standard promise based getUserMedia()
    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
	*/

	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		console.log("getUserMedia() success, stream created, initializing WebAudioRecorder...");

		/*
			create an audio context after getUserMedia is called
			sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
			the sampleRate defaults to the one set in your OS for your playback device

		*/
		audioContext = new AudioContext();

		//assign to gumStream for later use
		gumStream = stream;

		/* use the stream */
		input = audioContext.createMediaStreamSource(stream);

		//stop the input from playing back through the speakers
		//input.connect(audioContext.destination)

		recorder = new WebAudioRecorder(input, {
		  workerDir: "/static/js/", // must end with slash
		  encoding: "wav",
		  numChannels:2, //2 is the default, mp3 encoding supports only 2
		  onEncoderLoading: function(recorder, encoding) {
		    // show "loading encoder..." display
		    console.log("Loading "+encoding+" encoder...");
		  },
		  onEncoderLoaded: function(recorder, encoding) {
		    // hide "loading encoder..." display
		    console.log(encoding+" encoder loaded");
		  }
		});

		recorder.onComplete = function(recorder, blob) {
			console.log("Encoding complete");
			createDownloadLink(blob,recorder.encoding);
		}

		recorder.setOptions({
		  timeLimit:120,
		  encodeAfterRecord:encodeAfterRecord,
	      ogg: {quality: 0.5},
	      mp3: {bitRate: 160}
	    });

		//start the recording process
		recorder.startRecording();

		 console.log("Recording started");

	}).catch(function(err) {

	});

}

function stopRecording() {
	//stop microphone access
	gumStream.getAudioTracks()[0].stop();
	//tell the recorder to finish the recording (stop recording + encode the recorded audio)
	recorder.finishRecording();
}

function cancelRec() {
  if (RECORDING) {
    RECORDING = false;
    //tell the recorder to stop the recording
    rec.stop(); //stop microphone access
    gumStream.getAudioTracks()[0].stop();
    document.getElementById('recBTN').innerHTML = '<i class="fa fa-microphone" aria-hidden="true"></i>';
  }
  audio.pause();
  audio.currentTime = 0;
  document.getElementById('audios-img').style.display = 'none';
}

function createDownloadLink(blob) {
  //upload link
  var xhr = new XMLHttpRequest();
  xhr.onload = function(e) {
    if (this.readyState === 4) {}
  };
  var fd = new FormData();
  fd.append("usernameUser", EMAIL);
  fd.append("oper", 'addAudio');
  fd.append("version", 'web');
  fd.append("gameId", GAMEID);
  fd.append("msg", '::AUDIO::' + USERID + '::');
  fd.append("file", USERID + '_' + GAMEID);
  fd.append("audio", blob, USERID + '_' + GAMEID + '.wav');
  xhr.open("POST", "https://rummi.theozserver.com/API/app/fetch/", true);
  xhr.send(fd);
  xhr.onreadystatechange = function() {
    if (xhr.readyState == 4 && xhr.status == 200) {
      sendData("audio");
      console.log("Send");
    }
  };
}
