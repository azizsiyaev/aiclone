from flask import Flask, request, render_template, send_file, make_response
from flask import jsonify
import numpy as np
import tts
# import stt
# import translate
import librosa
import soundfile as sf

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
    text = request.form['input-text']
    audio_source = request.form['source']

    if audio_source == 'mic':
        audio_bytes = request.files['recorded-audio'].read()
    elif audio_source == 'file':
        audio_bytes = request.files['input-audio'].read()
    else:
        return 'File not found'

    save_bytes(audio_bytes, request_file)
    audio, sr = librosa.load(request_file, sr=None)
    print('Received Audio: ', audio.shape, sr)

    generated_audio = tts.clone_voice(text, audio, sr)
    sf.write(file=response_file, data=generated_audio, samplerate=sr)

    return send_file(response_file, mimetype='audio/wav', as_attachment=True)


@app.route('/voice_cloning/', methods=['GET', 'POST'])
def voice_cloning():
    return render_template('index.html')


@app.route('/full_pipeline/', methods=['GET', 'POST'])
def full_pipeline():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000, debug=True)
