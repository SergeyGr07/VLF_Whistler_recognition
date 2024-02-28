from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import os
import pywt


def dec_wavelet(signal: np.ndarray, filename: str, fs: float, output_folder: str, whistlers_folder: str):
    f, t, Sxx = spectrogram(signal, fs)
    f = f[:len(f) // 5]
    # print(f"length: {len(f)}")
    # print(f"Frequency: {f[:len(f)]}")
    # print(t)
    # print(len(t))
    print(filename)
    # Вейвлет-преобразование
    coeffs = pywt.wavedec(signal, 'coif5', level=10)

    features = []
    for coef in coeffs:
        features.extend([np.mean(coef), np.std(coef)])
    sum_features = (sum(features))
    # sum_amplitudes = np.sum(amplitudes_array, axis=0)
    # # print('wavelets features: ', coeffs)
    # print(f"sum_amplitudes: {sum_amplitudes}")
    print(f"sum: {sum_features}", '\n')

    # if sum_features > -11000 and sum_features < 11000:
        # Построение спектрограммы
    plt.figure(figsize=(10, 4))
    plt.pcolormesh(t, f, 10 * np.log10(Sxx[:len(f), :]), shading='auto', cmap='jet')
        # plt.ylabel('Frequency [Hz]')
    # plt.xlabel('Time [sec]')
    #     # plt.title(f'Spectrogram of Whistler: {filename}, Features={sum_features}')
    plt.colorbar(label='Power/Frequency [dB/Hz]')
    # plt.axis('off')
    plt.show()
    # plt.savefig(f"new_whistler_dataset/{whistlers_folder}/{filename}.png")
    # plt.savefig(f"dataset_for_five_sec/whistler/{filename}.png")
    plt.close('all')
    #     # Сохранение данных в аудиофайл формата WAV
    #     # wav_filename = os.path.splitext(filename)[0] + ".wav"
    #     # print(wav_filename)
    #     # wavfile.write(f"whistler_data/{filename}.wav", int(fs), signal.astype(np.int16))
    # else:
    #     # Построение спектрограммы
    #     plt.figure(figsize=(10, 4))
    #     plt.pcolormesh(t, f, 10 * np.log10(Sxx[:len(f), :]), shading='auto', cmap='jet')
    #     plt.ylabel('Frequency [Hz]')
    #     # plt.xlabel('Time [sec]')
    #     # plt.title(f'Spectrogram of not whistler: {filename}, Features={sum_features}')
    #     plt.colorbar(label='Power/Frequency [dB/Hz]')
    #     # plt.axis('off')
    #     plt.show()
        # plt.savefig(f"not_whistler/{filename}.png")
        # plt.close('all')
        # wav_filename = os.path.splitext(filename)[0] + ".wav"
        # print(wav_filename)
        # wavfile.write(f"not_whistler_data/{filename}.wav", int(fs), signal.astype(np.int16))


def cwt_wavelet(signal: np.ndarray, filename: str, fs: float, output_folder: str):
    f, t, Sxx = spectrogram(signal, fs)
    # Вейвлет-преобразование
    # Выберите вейвлет (например, 'morl' или 'haar')
    wavelet = 'morl'

    # Примените CWT к сигналу
    coeffs, freqs = pywt.cwt(signal, np.arange(1, 128), wavelet)

    # Получите амплитуду CWT
    # amplitude = np.abs(coeffs)

    features = []
    for coef in coeffs:
        features.extend([np.mean(coef), np.std(coef)])
    sum_features = (sum(features))

    print(f"sum: {sum_features}", '\n')

    # plt.figure(figsize=(10, 6))
    # plt.imshow(amplitude, extent=[0, len(signal), freqs[-1], freqs[0]], cmap='viridis', aspect='auto')
    # plt.colorbar(label='Amplitude')
    # plt.title(f'Continuous Wavelet Transform {filename}')
    # plt.xlabel('Sample Index')
    # plt.ylabel('Frequency (Hz)')
    # plt.show()

    if sum_features > 10000 and sum_features < 35000:
        # Построение спектрограммы
        plt.figure(figsize=(10, 4))
        plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='auto', cmap='jet')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.title(f'Whistler spectrogram of {filename}, Features={sum_features}')
        plt.colorbar(label='Power/Frequency [dB/Hz]')
        # plt.show()
        plt.savefig(f"whistler_specs(cwt)/{filename}.png")

    #     # Сохранение данных в аудиофайл формата WAV
        wav_filename = os.path.splitext(filename)[0] + ".wav"
    #     # print(wav_filename)
        wavfile.write(f"{output_folder}/{wav_filename}", int(fs), signal.astype(np.int16))
    else:
        # Построение спектрограммы
        plt.figure(figsize=(10, 4))
        plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='auto', cmap='jet')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.title(f'Not whistler spectrogram of {filename}, Features={sum_features}')
        plt.colorbar(label='Power/Frequency [dB/Hz]')
        # plt.show()
        plt.savefig(f"not_whistlers_specs(cwt)/{filename}.png")
