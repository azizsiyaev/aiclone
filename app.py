from flask import Flask, request, render_template, send_file, make_response
import tts_rtvc
import tts_bark
import librosa
import torchaudio
import soundfile as sf
import time

app = Flask(__name__)
request_file = 'uploads/request.wav'
response_file = 'uploads/response.wav'


def save_bytes(audio_bytes, name):
    with open(name, 'wb') as f:
        f.write(audio_bytes)


def process_request_audio(request):
    audio_source = request.form['source']
    audio_id = 'recorded-audio' if audio_source == 'mic' else 'input-audio'
    audio_bytes = request.files[audio_id].read()
    save_bytes(audio_bytes, request_file)


def generate_audio(text, model_type):
    audio, generated_audio, sr = None, None, None
    if model_type == 'bark':
        audio, sr = torchaudio.load(request_file)
        generated_audio, sr = tts_bark.clone_voice(text, audio, sr)
    elif model_type == 'rtvc':
        audio, sr = librosa.load(request_file, sr=None)
        target_sr = 16_000
        audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
        sr = target_sr
        generated_audio = tts_rtvc.clone_voice(text, audio, sr=target_sr)
    sf.write(file=response_file, data=generated_audio, samplerate=sr)


@app.route('/clone_voice/', methods=['POST'])
def clone_voice():
    start_time = time.time()

    text = request.form['input-text']
    model_type = request.form['model-type']

    process_request_audio(request)
    generate_audio(text, model_type)

    response = make_response(send_file(response_file, mimetype='audio/wav', as_attachment=True))
    response.headers['time'] = str(time.time() - start_time)
    return response


@app.route('/voice_cloning/', methods=['GET', 'POST'])
def voice_cloning():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000, debug=False)
