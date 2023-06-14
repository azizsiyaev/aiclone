import librosa
import os
import soundfile as sf
from tqdm import tqdm


def load_resample(path, dest_sr=16_000):
    audio_data, sr = librosa.load(path, sr=None)
    resampled_audio_data = librosa.resample(audio_data, orig_sr=sr, target_sr=dest_sr)
    return resampled_audio_data


def resample_files_in_folder(src_folder_path, dest_folder_path, dest_sr=16_000):
    for file in tqdm(os.listdir(src_folder_path)):
        src_file_path = os.path.join(src_folder_path, file)
        dest_file_path = os.path.join(dest_folder_path, file)

        try:
            resampled_audio_data = load_resample(src_file_path, dest_sr=dest_sr)
            sf.write(file=dest_file_path, data=resampled_audio_data, samplerate=dest_sr)
        except:
            print('Could not resample file: ', src_file_path)


def main():
    # src_folder_path = 'test-task-audios'
    # dest_folder_path = 'audio_data'
    # resample_files_in_folder(src_folder_path, dest_folder_path, dest_sr=16_000)
    pass


if __name__ == '__main__':
    main()




