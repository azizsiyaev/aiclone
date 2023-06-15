from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
import torch
import os
from speechbrain.pretrained import EncoderClassifier
import librosa
import soundfile as sf


def create_speaker_embedding(audio, speaker_model):
    with torch.no_grad():
        speaker_embeddings = speaker_model.encode_batch(torch.tensor(audio))
        speaker_embeddings = torch.nn.functional.normalize(speaker_embeddings, dim=2)
        speaker_embeddings = speaker_embeddings.squeeze().cpu().numpy()
    return speaker_embeddings


def main():
    # https://colab.research.google.com/drive/1i7I5pzBcU3WDFarDnzweIj4-sVVoIUFJ#scrollTo=NpXOJAZIs2-n
    spk_model_name = 'speechbrain/spkrec-xvect-voxceleb'
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    speaker_model = EncoderClassifier.from_hparams(
        source=spk_model_name,
        run_opts={'device': device},
        savedir=os.path.join('/tmp', spk_model_name)
    )
    model_checkpoint = 'microsoft/speecht5_tts'
    model_gan_checkpoint = 'microsoft/speecht5_hifigan'
    processor = SpeechT5Processor.from_pretrained(model_checkpoint)
    tokenizer = processor.tokenizer
    model = SpeechT5ForTextToSpeech.from_pretrained(model_checkpoint)
    vocoder = SpeechT5HifiGan.from_pretrained(model_gan_checkpoint)

    target_text = 'In our experience it can be difficult to get good results out of this model ' \
                  'The results can be rather noisy and sometimes what the model outputs doesnt ' \
                  'even sound like speech at all A lot of this appears to be related to the speaker embeddings'

    file_path = 'audio_data/2.wav'
    audio, sr = librosa.load(file_path, sr=None)
    speaker_embeddings = create_speaker_embedding(audio, speaker_model)

    input = processor(
        text=target_text,
        audio_target=audio,
        sampling_rate=16_000,
        return_attention_mask=False,
        return_tensors='pt'
    )
    # input['speaker_embeddings'] = speaker_embeddings
    speaker_embeddings = torch.tensor(speaker_embeddings).unsqueeze(0)
    spectrogram = model.generate_speech(input['input_ids'], speaker_embeddings)
    with torch.no_grad():
        speech = vocoder(spectrogram)

    sf.write('test.wav', speech.numpy(), samplerate=16_000)


if __name__ == '__main__':
    main()