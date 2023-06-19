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

var mediaRecorder;
var recordedChunks = [];
var audioSource;

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function(stream) {
            recordedChunks = [];
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            recordButton.disabled = true;
            stopButton.disabled = false;

            mediaRecorder.addEventListener('dataavailable', function(event) {
                recordedChunks.push(event.data);
            });
        })
        .catch(function(error) {
            console.error('Error accessing microphone:', error);
        });
}

function stopRecording() {
    mediaRecorder.stop();
    mediaRecorder.addEventListener('stop', function() {
        recordButton.disabled = false;
        stopButton.disabled = true;

        var recordedAudioBlob = new Blob(recordedChunks, { type: 'audio/wav' });
        const url = window.URL.createObjectURL(recordedAudioBlob);
        referenceAudioSource.src = url;
        referenceAudio.load();

        inputAudioFile.src = url;
        audioSource = 'mic';
    });

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

    loading.style.display = 'block';

    // outputAudio.load()
    e.preventDefault();

    var recordedAudioBlob = new Blob(recordedChunks, { type: 'audio/wav' });
    const formData = new FormData(form);
    formData.append('recorded-audio', recordedAudioBlob, 'recording.wav');
    formData.append('source', audioSource)
    // http://127.0.0.1:9000/clone_voice/
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