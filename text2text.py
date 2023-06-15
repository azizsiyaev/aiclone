from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch


def translate(model, tokenizer, sentence):
    inputs = tokenizer(sentence, return_tensors='pt', padding=True)
    with torch.no_grad():
        predictions = model.generate(inputs.input_ids, max_length=100)
    prediction = tokenizer.batch_decode(predictions, skip_special_tokens=True)[0]

    return prediction


def main():
    tokenizer = T5Tokenizer.from_pretrained('t5-small')
    model = T5ForConditionalGeneration.from_pretrained('t5-small', return_dict=True)


if __name__ == '__main__':
    main()