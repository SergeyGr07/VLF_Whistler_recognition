from scipy.io import loadmat
import numpy as np
import os
from wavelet_analysis import dec_wavelet
from scipy.signal import butter, filtfilt


def butter_lowpass_filter(data, cutoff_freq, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff_freq / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y


def process_all_files(input_folder, output_folder_dec, output_folder_cwt):
    if not os.path.exists(output_folder_dec) and not os.path.exists(output_folder_cwt):
        os.makedirs(output_folder_dec)
        os.makedirs(output_folder_cwt)

    for root, dirs, files in os.walk(input_folder):
        path = root.split(os.sep)
        print((len(path) - 1) * '---', os.path.basename(root))
        for filename in files:
            print(len(path) * '---', filename)
            file_path = os.path.join(root, filename)
            # Загрузка данных из файла .mat

            mat_data = loadmat(file_path)
            # print(mat_data)

            # Получаем данные
            data_array = mat_data['data']
            # print(len(data_array))

            # Преобразовываем данные в одномерный массив
            signal = data_array.flatten()
            print(f"Signal before: {len(signal)}")
            # Параметры для построения спектрограммы
            fs = float(mat_data['Fs'].item())  # Частота дискретизации
            print(fs)
            # Устанавливаем параметры для фильтрации
            # fs = 100000  # Пример частоты дискретизации в Гц (может быть другой в вашем случае)
            # cutoff_freq = 25000  # Частота среза в Гц

            # Применяем фильтр
            # signal = butter_lowpass_filter(signal, cutoff_freq, fs)

            # freqs = np.fft.fftfreq(len(signal), 1 / fs)
            # print(freqs)
            # # Находим индекс частоты 25 кГц
            # index_25khz = np.argmax(freqs >= 25e3)

            # # Отсекаем часть сигнала, соответствующую частотам выше 25 кГц
            # signal = signal[:index_25khz]
            # print(f"Signal after: {signal}")
            segment_length = 2 * fs  # длина одного отрезка в отсчётах
            num_segments = 90  # количество отрезков

            segments = []
            for i in range(num_segments):
                start_index = int(i * segment_length)
                end_index = int((i + 1) * segment_length)
                segment = signal[start_index:end_index]
                segments.append(segment)
            print(f"Segments: {len(segments)}")
            whistlers_folder = "whistler"
            for i, segment_signal in enumerate(segments):
                dec_wavelet(segment_signal, f"{filename}_{i}", fs, output_folder_dec, whistlers_folder)

            # nperseg = int(fs * 5)  # Длина каждого сегмента (5 секунд)
            # noverlap = nperseg // 2  # Перекрытие между сегментами
            # num_segments = (len(signal) - nperseg) // (nperseg - noverlap) + 1
            # print(num_segments)
            # signal = signal[:nperseg]
            # # print(type(signal), type(filename), type(fs), type(output_folder))

            # for i in range(num_segments):
            #     start = i * (nperseg - noverlap)
            #     end = min(start + nperseg, len(signal))  # Убедитесь, что end не превышает общую длину сигнала
            #     segment_signal = signal[start:end]

            #     if len(segment_signal) == 0:  # Проверка на пустой сегмент
            #         continue

            #     # Вызов функции для обработки текущего сегмента
            #     dec_wavelet(segment_signal, f"{filename}{i}", fs, output_folder_dec, whistlers_folder)
            # dec_wavelet(signal, filename, fs, output_folder_dec, whistlers_folder)

            # cwt_wavelet(signal, filename, fs, output_folder_cwt)


process_all_files("vlf_data/PalmerStation/2007_01_01", "whistler_sounds_dec", "whistler_sounds_cwt")
# 2013_01_01