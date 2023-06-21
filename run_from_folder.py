from app import generate_audio
import os
from tqdm import tqdm


def main():
    model_type = 'rtvc'

    source_folder_path = 'audios/test-task-audios'
    dest_folder_path = f'audios/{model_type}_results'
    if not os.path.exists(dest_folder_path):
        os.mkdir(dest_folder_path)

    text = 'Does the quick brown fox jump over the lazy dog?'

    for file in tqdm(os.listdir(source_folder_path)):
        audio_file_path = os.path.join(source_folder_path, file)
        generated_audio_file_path = os.path.join(dest_folder_path, file)

        generate_audio(
            text=text,
            model_type=model_type,
            input_file=audio_file_path,
            output_file=generated_audio_file_path
        )


if __name__ == '__main__':
    main()