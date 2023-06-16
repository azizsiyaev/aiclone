import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, AutoProcessor

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model_checkpoint = 'facebook/mms-1b-fl102'
processor = AutoProcessor.from_pretrained(model_checkpoint)
model = Wav2Vec2ForCTC.from_pretrained(model_checkpoint)
processor.tokenizer.set_target_lang('rus')
model.load_adapter('rus')
model.to(device)


def transcribe(audio):
    input_values = processor(
        audio,
        sampling_rate=16_000,
        return_tensors='pt'
    ).input_values.to(device)

    with torch.no_grad():
        logits = model(input_values).logits

    pred_ids = torch.argmax(logits, dim=-1)[0]
    transcript = processor.decode(pred_ids)
    return transcript


def another_stt_model_processor(model_checkpoint='jonatasgrosman/wav2vec2-large-xlsr-53-russian'):
    processor = Wav2Vec2Processor.from_pretrained(model_checkpoint)
    model = Wav2Vec2ForCTC.from_pretrained(model_checkpoint)
    return model, processor


def main():
    # device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
    file_path = 'audio_data/2.wav'
    audio, sr = librosa.load(file_path, sr=None)

    prediction = transcribe(audio)

    print('Predicted Transcript: ', prediction)

#   https://huggingface.co/facebook/mms-1b-fl102 check this out


if __name__ == '__main__':
    main()