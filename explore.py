import os
import librosa


def main():
    audios_folder_path = 'audio_data'
    for file in os.listdir(audios_folder_path):
        file_path = os.path.join(audios_folder_path, file)

        audio_data, sr = librosa.load(file_path, sr=None)
        print('File name: ', file, 'Audio shape: ', audio_data.shape, 'SR: ', sr)


if __name__ == '__main__':
    main()