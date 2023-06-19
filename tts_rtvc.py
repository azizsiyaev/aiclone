from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder import inference as vocoder
import librosa
import numpy as np
import soundfile as sf


encoder.load_model('pretrained_models/encoder.pt')
synthesizer = Synthesizer('pretrained_models/synthesizer.pt', verbose=False)
vocoder.load_model('pretrained_models/vocoder.pt')


def clone_voice(text, audio, sr):
    embedding = encoder.embed_utterance(encoder.preprocess_wav(audio, sr))
    specs = synthesizer.synthesize_spectrograms([text], [embedding])
    generated_wav = vocoder.infer_waveform(specs[0])
    generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")
    return generated_wav


def main():
    text = "Hi people check this out this man Rida is doing something fun"
    audio_path = 'audio_data/2.wav'
    audio, sr = librosa.load(audio_path, sr=None)

    generated_audio = clone_voice(text, audio, sr)
    sf.write('test3.wav', generated_audio, samplerate=16_000)


if __name__ == '__main__':
    main()