const form = document.getElementById('form');
const referenceAudio = document.getElementById('reference-audio');
const referenceAudioSource = document.getElementById('reference-audio-source');
const outputAudio = document.getElementById('output-audio');
const outputAudioSource = document.getElementById('output-audio-source');
const inputAudioFile = document.getElementById('input-audio');
const loading = document.getElementById('loading');
const recordButton = document.getElementById('recordButton');
const stopButton = document.getElementById('stopButton');
const timeText = document.getElementById('generation-time');

inputAudioFile.addEventListener('change', changeAudioSource);
form.addEventListener('submit', generate);
recordButton.addEventListener('click', startRecording);
stopButton.addEventListener('click', stopRecording);

var audioSource;

URL = window.URL || window.webkitURL;
var gumStream;
var rec;
var input;
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext;
var blobToSend;


function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true, video: false})
        .then(function(stream) {

            audioContext = new AudioContext();
		    gumStream = stream;
		    input = audioContext.createMediaStreamSource(stream);

    		rec = new Recorder(input, { numChannels: 1 })
	    	rec.record()
            console.log("Recording started");
            recordButton.disabled = true;
            stopButton.disabled = false;

        })
        .catch(function(error) {
            console.error('Error accessing microphone:', error);
        });
}

function stopRecording() {
    recordButton.disabled = false;
    stopButton.disabled = true;

    rec.stop();
	gumStream.getAudioTracks()[0].stop();
	rec.exportWAV(createDownloadLink);

    console.log("Recording stopped");
}

function createDownloadLink(blob) {

	let url = URL.createObjectURL(blob);
	referenceAudio.controls = true;
	referenceAudioSource.src = url;
    referenceAudio.load();
    inputAudioFile.src = url;
    audioSource = 'mic';

    blobToSend = blob;

}

function changeAudioSource(e){
    let file = event.target.files[0];
    let inputAudioURL;
    inputAudioURL = URL.createObjectURL(file);
    referenceAudioSource.src = inputAudioURL;
    referenceAudio.load();
    audioSource = 'file';
}

async function generate(e){
    console.log("Voice Generate")

    loading.style.display = 'block';

    e.preventDefault();

    const formData = new FormData(form);
    formData.append('source', audioSource)
    if (audioSource === 'mic'){
        formData.append('recorded-audio', blobToSend, 'recording.wav');
    }

    let response = await fetch('/clone_voice/', {
        method: 'POST',
        body: formData

    })
        .then(response => {
            const time = response.headers.get('time')
            timeText.innerHTML = "Generation time (s): " + time;
            return response;
        })
        .then(response => response.blob())
        .then(blob => {
            let url;
            url = URL.createObjectURL(blob);
            outputAudioSource.src = url;
            outputAudio.load();
            loading.style.display = 'none';
        });
}