from flask import Flask, request, render_template, send_file, make_response
from flask import jsonify
import numpy as np
import tts_rtvc
import tts_bark
# import stt
# import translate
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


@app.route('/translate/', methods=['POST'])
def translate():
    rus_text = request.form['text']
    eng_text = translate.translate(rus_text)

    response = {
        'translation': eng_text
    }
    return jsonify(response)


@app.route('/transcribe/', methods=['POST'])
def transcribe():
    audio_bytes = request.files['audio_data'].read()
    audio = np.frombuffer(audio_bytes, dtype=np.float32)

    transcript = stt.transcribe(audio)

    response = {
        'transcript': transcript
    }
    return jsonify(response)


@app.route('/clone_voice/', methods=['POST'])
def clone_voice():
    start_time = time.time()

    text = request.form['input-text']
    audio_source = request.form['source']
    model_type = request.form['model-type']

    if audio_source == 'mic':
        audio_bytes = request.files['recorded-audio'].read()
    elif audio_source == 'file':
        audio_bytes = request.files['input-audio'].read()
    else:
        return 'File not found'

    save_bytes(audio_bytes, request_file)
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
    # response = send_file(response_file, mimetype='audio/wav', as_attachment=True)
    response = make_response(send_file(response_file, mimetype='audio/wav', as_attachment=True))
    response.headers['time'] = str(time.time() - start_time)
    return response


@app.route('/voice_cloning/', methods=['GET', 'POST'])
def voice_cloning():
    return render_template('index.html')


@app.route('/full_pipeline/', methods=['GET', 'POST'])
def full_pipeline():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000, debug=False)
