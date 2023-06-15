from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch


def translate(model, tokenizer, sentence):
    inputs = tokenizer(sentence, return_tensors='pt', padding=True)
    with torch.no_grad():
        predictions = model.generate(inputs.input_ids)[0]
    prediction = tokenizer.decode(predictions, skip_special_tokens=True)
    return prediction


def main():
    model_checkpoint = 'Helsinki-NLP/opus-mt-ru-en'
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)

    input_text = 'и так давайте приступим к самым озам питона вообще как работае наш файл вот мы ' \
                 'создали синержи точка пай здесь мы будем писать весь код он выполняется как некая ' \
                 'последовательность заклинаний вот вы в хогварде например там сказали овада кидавра ' \
                 'потммз люмо  эм нз и вот сначало выполниться овада кидавра потом же люмо соответстенно ' \
                 'сначало выполняеться первая страка потом потом т-е и так д..е за маленьким '\
                 'исключением о котором мы поговорим потом хорошо давайте приступим к изучению первого ' \
                 'нашего заклинания чтобы в схватке с волондомортом мы хочёт могли противопоставить ' \
                 'оно называется принт собстенно это заклинание берёт и выводит то что мы ему сказали в ' \
                 'круглых кобочках например если мы скажему вывести пять то как нестранно он унас это сделает ' \
                 'да все отлично вывел пять'

    prediction = translate(model, tokenizer, sentence=input_text)
    print('Predicted Transcript: ', prediction)


if __name__ == '__main__':
    main()