from bark.generation import load_codec_model, generate_text_semantic
from encodec.utils import convert_audio

import torchaudio
import torch
import librosa
import numpy as np
import soundfile as sf

from hubert.hubert_manager import HuBERTManager
hubert_manager = HuBERTManager()
# hubert_manager.make_sure_hubert_installed()
hubert_manager.make_sure_tokenizer_installed()

device = 'cpu' # or 'cpu'
model = load_codec_model(use_gpu=True if device == 'cuda' else False)

from hubert.pre_kmeans_hubert import CustomHubert
from hubert.customtokenizer import CustomTokenizer

# Load the HuBERT model
hubert_model = CustomHubert(checkpoint_path='data/models/hubert/hubert.pt').to(device)

# Load the CustomTokenizer model
tokenizer = CustomTokenizer.load_from_checkpoint('data/models/hubert/tokenizer.pth').to(device)

from bark.api import generate_audio
from transformers import BertTokenizer
from bark.generation import SAMPLE_RATE, preload_models, codec_decode, generate_coarse, generate_fine, generate_text_semantic



def main():
    # https://github.com/serp-ai/bark-with-voice-clone/blob/main/generate.ipynb
    # Load and pre-process the audio waveform
    audio_filepath = 'audio_data/1.wav'  # the audio you want to clone (under 13 seconds)
    wav, sr = torchaudio.load(audio_filepath)
    # wav, sr = librosa.load(audio_filepath)
    wav = convert_audio(wav, sr, model.sample_rate, model.channels)
    wav = wav.to(device)

    semantic_vectors = hubert_model.forward(wav, input_sample_hz=model.sample_rate)
    semantic_tokens = tokenizer.get_token(semantic_vectors)

    with torch.no_grad():
        encoded_frames = model.encode(wav.unsqueeze(0))
    codes = torch.cat([encoded[0] for encoded in encoded_frames], dim=-1).squeeze()  # [n_q, T]

    codes = codes.cpu().numpy()
    # move semantic tokens to cpu
    semantic_tokens = semantic_tokens.cpu().numpy()

    voice_name = 'aziz'  # whatever you want the name of the voice to be
    output_path = 'bark/assets/prompts/' + voice_name + '.npz'
    np.savez(output_path, fine_prompt=codes, coarse_prompt=codes[:2, :], semantic_prompt=semantic_tokens)

    text_prompt = "Hello, my name is Serpy. And, uh — and I like pizza. [laughs]"
    preload_models(
        text_use_gpu=True,
        text_use_small=False,
        coarse_use_gpu=True,
        coarse_use_small=False,
        fine_use_gpu=True,
        fine_use_small=False,
        codec_use_gpu=True,
        force_reload=False,
        path="models"
    )

    audio_array = generate_audio(text_prompt, history_prompt=voice_name, text_temp=0.7, waveform_temp=0.7)
    filepath = "aziz.wav"  # change this to your desired output path
    sf.write(filepath, audio_array, SAMPLE_RATE)


if __name__ == '__main__':
    main()