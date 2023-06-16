const form = document.getElementById('form');
const outputAudio = document.getElementById('output-audio');
const outputAudioSource = document.getElementById('output-audio-source');

form.addEventListener('submit', generate);

async function generate(e){
    e.preventDefault();
    const formData = new FormData(form);

    // for (const entry of formData.entries()) {
    //     console.log(entry)
    // }

    let response = await fetch("/http://165.246.43.139:9000/predict/", {
        body: formData
    })

    // make a request

    // let file = File([])
    outputAudioSource.src = URL.createObjectURL(file)
    outputAudio.load()
    outputAudio.play()
}