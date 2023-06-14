import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor


def transcribe(audio, model, processor, device):
    input_values = processor(
        audio,
        sampling_rate=16_000,
        return_tensors='pt'
    ).input_values.to(device)

    with torch.no_grad():
        logits = model(input_values).logits

    pred_ids = torch.argmax(logits, dim=-1)
    transcript = processor.batch_decode(pred_ids)[0]
    return transcript


def get_stt_model_processor_v1(model_checkpoint='jonatasgrosman/wav2vec2-large-xlsr-53-russian'):
    processor = Wav2Vec2Processor.from_pretrained(model_checkpoint)
    model = Wav2Vec2ForCTC.from_pretrained(model_checkpoint)
    return model, processor


def main():
    # device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
    device = torch.device('cpu')

    model, processor = get_stt_model_processor_v1()

    file_path = 'audio_data/2.wav'
    audio, sr = librosa.load(file_path, sr=None)

    prediction = transcribe(audio, model, processor, device)

    print('Predicted Transcript: ', prediction)

#     https://huggingface.co/facebook/mms-1b-fl102 check this out


if __name__ == '__main__':
    main()