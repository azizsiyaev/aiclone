from bark.generation import load_codec_model, generate_text_semantic
from encodec.utils import convert_audio
import torchaudio
import torch
import numpy as np
import soundfile as sf

from hubert.hubert_manager import HuBERTManager
hubert_manager = HuBERTManager()
# hubert_manager.make_sure_hubert_installed()
# hubert_manager.make_sure_tokenizer_installed()

device = 'cpu' # or 'cpu'
model = load_codec_model(use_gpu=True if device == 'cuda' else False)

from hubert.pre_kmeans_hubert import CustomHubert
from hubert.customtokenizer import CustomTokenizer


hubert_model = CustomHubert(checkpoint_path='data/models/hubert/hubert.pt').to(device)
tokenizer = CustomTokenizer.load_from_checkpoint('data/models/hubert/tokenizer.pth').to(device)

from bark.api import generate_audio
from bark.generation import SAMPLE_RATE, preload_models

preload_models(
        text_use_gpu=True,
        text_use_small=True,
        coarse_use_gpu=True,
        coarse_use_small=True,
        fine_use_gpu=True,
        fine_use_small=True,
        codec_use_gpu=True,
        force_reload=True,
        path="models"
    )


def clone_voice(text, audio, sr):
    audio = convert_audio(audio, sr, model.sample_rate, model.channels)
    audio = audio.to(device)

    semantic_vectors = hubert_model.forward(audio, input_sample_hz=model.sample_rate)
    semantic_tokens = tokenizer.get_token(semantic_vectors)

    with torch.no_grad():
        encoded_frames = model.encode(audio.unsqueeze(0))
    codes = torch.cat([encoded[0] for encoded in encoded_frames], dim=-1).squeeze()

    codes = codes.cpu().numpy()
    semantic_tokens = semantic_tokens.cpu().numpy()

    voice_name = 'temp_output'
    output_path = 'bark/assets/prompts/' + voice_name + '.npz'
    np.savez(output_path, fine_prompt=codes, coarse_prompt=codes[:2, :], semantic_prompt=semantic_tokens)
    audio_array = generate_audio(text, history_prompt=voice_name, text_temp=0.7, waveform_temp=0.7)
    return audio_array, SAMPLE_RATE


def main():
    # https://github.com/serp-ai/bark-with-voice-clone/blob/main/generate.ipynb
    # Load and pre-process the audio waveform
    pass


if __name__ == '__main__':
    main()