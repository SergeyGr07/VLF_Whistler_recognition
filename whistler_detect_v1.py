import pywt
import numpy as np
import scipy.io.wavfile as wav
import librosa
import os
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")


def extract_wavelet_features(audio_file):
    sample_rate, audio_data = wav.read(audio_file)

    coeffs = pywt.wavedec(audio_data, 'db4', level=6)

    # print(f"coeffs: {coeffs}")
    # print(len(coeffs))

    features = []
    for coef in coeffs:
        features.extend([np.mean(coef), np.std(coef)])
    # print('wavelets features: ', features, '\n')

    return features


def extract_spectrogram_features(audio_file):
    audio_data, sample_rate = librosa.load(audio_file)

    spectrogram = librosa.feature.melspectrogram(y=audio_data, sr=sample_rate)
    # print(f'spectrogram: {spectrogram}')

    features = []

    mean_amplitude = np.mean(spectrogram)

    # print(f"mean_amplitude: {mean_amplitude}")
    features.append(mean_amplitude)

    std_amplitude = np.std(spectrogram)
    # print(f'std_amplitude: {std_amplitude}')
    features.append(std_amplitude)
    print('spec features: ', features)
    return features


threshold = 25000

audio_folder = "sounds"

for filename in os.listdir(audio_folder):
    if filename.endswith(".wav"):
        print(filename, '\n')
        audio_file = os.path.join(audio_folder, filename)

        wavelet_features = extract_wavelet_features(audio_file)

        spectrogram_features = extract_spectrogram_features(audio_file)

        combined_features = wavelet_features + spectrogram_features
        print(sum(combined_features))
        if sum(combined_features) > threshold:
            print(f"Файл '{filename}' содержит свистящие атмосферики.\n")

            audio_data, sample_rate = librosa.load(audio_file)
            spectrogram = librosa.feature.melspectrogram(y=audio_data, sr=sample_rate)
            plt.figure(figsize=(10, 4))
            librosa.display.specshow(librosa.power_to_db(spectrogram, ref=np.max), y_axis='mel', x_axis='time')
            plt.colorbar(format='%+2.0f dB')
            plt.title('Mel spectrogram of whistlers')
            plt.tight_layout()
            plt.show()

        else:
            audio_data, sample_rate = librosa.load(audio_file)
            spectrogram = librosa.feature.melspectrogram(y=audio_data, sr=sample_rate)
            plt.figure(figsize=(10, 4))
            librosa.display.specshow(librosa.power_to_db(spectrogram, ref=np.max), y_axis='mel', x_axis='time')
            plt.colorbar(format='%+2.0f dB')
            plt.title('Mel spectrogram of non-whistlers')
            plt.tight_layout()
            plt.show()
            print(f"Файл '{filename}' не содержит свистящих атмосфериков.\n")
