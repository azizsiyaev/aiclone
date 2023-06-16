const form = document.getElementById('form');
const outputAudio = document.getElementById('output-audio');
const outputAudioSource = document.getElementById('output-audio-source');

form.addEventListener('submit', generate);

async function generate(e){
    e.preventDefault();
    const formData = new FormData(form);

    let response = await fetch("http://165.246.43.139:9000/clone_voice/", {
        method: "POST",
        body: formData
    })

    // var blob = new Blob([response.data], { type: 'audio/wav' })
    // var url = window.URL.createObjectURL(blob)
    //
    // outputAudioSource.src = url;
    // outputAudio.load()
    // outputAudio.play()
    let blob = await response.blob()
    console.log(response)

    // let file = new File([response.data], "temp.wav", {type:'audio/wav'})
    // console.log(URL.createObjectURL(file))
    // outputAudioSource.src = URL.createObjectURL(file)
    // outputAudioSource.src = 'http://165.246.43.139:9000/' + json.url
    // outputAudio.load()
    // outputAudio.play()
    // outputAudioSource.src = URL.createObjectURL(blob);
    // outputAudio.load()
    // outputAudio.play()
}