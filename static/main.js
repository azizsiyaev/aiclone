const form = document.getElementById('form');
const referenceAudio = document.getElementById('reference-audio');
const referenceAudioSource = document.getElementById('reference-audio-source');
const outputAudio = document.getElementById('output-audio');
const outputAudioSource = document.getElementById('output-audio-source');
const inputAudioFile = document.getElementById('input-audio');
const loading = document.getElementById('loading');

inputAudioFile.addEventListener('change', changeAudioSource);
form.addEventListener('submit', generate);


function changeAudioSource(e){
    var file = event.target.files[0];
    var url = URL.createObjectURL(file);
    console.log(url)
    referenceAudioSource.src = url;
    referenceAudio.load();
}


async function generate(e){

    loading.style.display = 'block';

    e.preventDefault();
    const formData = new FormData(form);

    let response = await fetch("http://127.0.0.1:9000/clone_voice/", {
        method: "POST",
        body: formData
    })
        .then(response => response.blob())
        .then(blob => {
            var url = URL.createObjectURL(blob);
            outputAudioSource.src = url;
            outputAudio.load()
            // outputAudio.play()
            loading.style.display = 'none';
        });
}