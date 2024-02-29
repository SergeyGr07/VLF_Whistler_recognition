import os
import numpy as np
import matplotlib.pyplot as plt
import librosa


# def plot_spectrogram(data, sampling_rate, title='Спектрограмма'):
#     plt.figure(figsize=(10, 6))
#     plt.specgram(data, Fs=sampling_rate, cmap='')
#     plt.title(title)
#     plt.xlabel('Время (сек)')
#     plt.ylabel('Частота (Гц)')
#     plt.colorbar(label='Амплитуда')
#     plt.show()
def plot_spectrogram(y, sr, title='Спектрограмма'):
    plt.figure(figsize=(10, 6))
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y.astype(float))), ref=np.max)
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='linear')
    # freqs = librosa.core.fft_frequencies(sr=sr)

    # Изменение диапазона построения на графике от 0 до половины частоты дискретизации
    # D = D[(freqs >= 0) & (freqs <= sr / 2)]

    # librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
    plt.title(title)
    plt.colorbar(format='%+2.0f dB')
    # plt.savefig(f'{title.replace(" ", "_")}.png')
    # plt.close()
    plt.show()


def plot_waveform(y, sr, voltage_range, title='Осциллограмма'):
    plt.figure(figsize=(10, 4))

    # Преобразование в формат с плавающей точкой
    y_float = y.astype(float)

    # Создание временной шкалы
    # time = np.arange(0, len(y_float)) / sr
    # Разрядность АЦП
    adc_bits = 14

    # Максимальное значение АЦП
    max_adc_value = 2 ** adc_bits - 1

    # Коэффициент пересчета в вольты
    voltage_conversion = voltage_range / max_adc_value

    # Создание временной шкалы
    time = np.arange(0, len(y_float)) / sr

    # Пересчет значений в вольты
    y_volts = y_float * voltage_conversion

    plt.plot(time, y_volts, color='b')   # Можете выбрать другой цвет, например, 'r' для красного
    plt.title(title)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    # plt.savefig(f'{title.replace(" ", "_")}.png')
    # plt.close()
    plt.show()


def read_binary_file(file_path):
    with open(file_path, 'rb') as file:
        binary_data = np.fromfile(file, dtype=np.int16)
        print(len(binary_data))
    return binary_data


def process_files_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".bin"):
            file_path = os.path.join(directory, filename)

            # Чтение бинарного файла
            binary_data = read_binary_file(file_path)

            # Частота дискретизации (может потребоваться настройка в зависимости от ваших данных)
            sampling_rate = 100000
            duration = librosa.get_duration(y=binary_data, sr=sampling_rate)

            print(f'Длительность файла: {duration} секунд')
            # Построение спектрограммы и осциллограммы
            voltage_range = 2.5
            # plot_waveform(binary_data, sampling_rate, voltage_range, title=f'Осциллограмма для {filename}')

            plot_spectrogram(binary_data, sampling_rate, title=f'Спектрограмма для {filename}')


# Путь к папке с бинарными файлами
folder_path = "September 2019"

# Обработка всех файлов в папке
process_files_in_directory(folder_path)
