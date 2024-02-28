import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram


def read_settings_file(file_path):
    settings = {}
    with open(file_path, 'r') as file:
        for line in file:
            # print(line)
            if ':' in line:
                key, value = line.strip().split(':', 1)  # Используем максимально одно разделение
                settings[key.strip()] = value.strip()
    return settings


def main():
    print()
    # Путь к папке с файлами
    broadband_folder = 'September 2019'
    # print(broadband_folder)
    # Поиск всех файлов с данными
    data_files = [file for file in os.listdir(broadband_folder) if file.endswith('.bin')]
    # print(data_files)
    # Перебор всех файлов с данными
    for i, data_file in enumerate(data_files):
        print(f"data_file: {data_file}{i}")
        # Получение пути к файлу с настройками
        sets_file = os.path.join(broadband_folder, data_file.replace('Data', 'Sets'))

        # Извлечение даты и времени из имени файла
        file_name_parts = os.path.splitext(data_file)[0].split('_')
        date_time_utc = file_name_parts[-2] + ' ' + file_name_parts[-1]
        
        # Чтение файла с настройками
        settings = read_settings_file(sets_file)
        print(f"Настройки из файла {sets_file}: {settings}")
        # Чтение файла с данными
        data_file_path = os.path.join(broadband_folder, data_file)
        with open(data_file_path, 'rb') as f:
            data = np.fromfile(f, dtype=np.int16)
        print(f"DATA BEFORE:{data[:10]}")
        data = data.astype(np.float32)  # Преобразуйте данные в тип float32 перед масштабированием
        data = data * (10.0 / 2**14) - 5.0
        print(f"DATA AFTER:{data[:10]}")
        fs = 200000

        # Расчет длительности файла данных
        sampling_rate = int(settings.get('Clock', fs))  # Получаем частоту дискретизации из настроек, если она там есть
        duration_seconds = len(data) / sampling_rate

        segment_length = 2 * fs  # длина одного отрезка в отсчётах
        num_segments = 30  # количество отрезков

        segments = []
        for i in range(num_segments):
            start_index = int(i * segment_length)
            end_index = int((i + 1) * segment_length)
            segment = data[start_index:end_index]
            segments.append(segment)
        print(f"Segments: {len(segments)}")

        for i, segment_signal in enumerate(segments):
            plt.figure(figsize=(10, 4))
            # plt.specgram(segment_signal, Fs=sampling_rate, NFFT=1024 // 2, cmap='jet')
            f, t, Sxx = spectrogram(segment_signal, fs, nfft=4096)
            Sxx = Sxx * 100000
            print(20 * np.log10(Sxx))
            f = f[:len(f) // 10]
            # plt.pcolormesh(t, f, 20 * np.log10(Sxx[:len(f), :]), shading='auto', cmap='jet')
            plt.pcolormesh(t, np.fft.fftfreq(len(segment_signal), 1/fs)[:len(segment_signal)//2], 20 * np.log10(Sxx[:len(segment_signal)//2]), shading='auto', cmap='jet')
            # plt.pcolormesh(t, np.fft.fftfreq(len(f))[:len(f) // 2], 10 * np.log10(Sxx[:len(f) // 2, :]), shading='auto', cmap='jet')
            plt.title('Спектрограмма')
            plt.xlabel('Время (сек)')
            plt.ylabel('Частота (Гц)')
            plt.colorbar().set_label('Интенсивность')
            # plt.axis('off')
            plt.show()
            # plt.savefig(f"for_cv/not_whistler/{data_file}{i}.png")
            plt.close('all')
        # if data_file.split('_')[1] == 'Data':
        #     # Вывод информации о файле
        #     print(f"Дата и время UTC: {date_time_utc}")
            # print(f"Настройки из файла {sets_file}: {settings}")
        #     # print(f"Количество отсчетов: {len(data)}")
        #     # print("Пример данных:", data[:10])
        #     print(f"Длительность файла данных: {duration_seconds:.2f} секунд")
        #     print()

        #     # # Вывод спектрограммы
        #     plt.figure(figsize=(10, 4))
        #     plt.specgram(data, Fs=sampling_rate, NFFT=1024, cmap='jet')
        #     plt.title('Спектрограмма')
        #     plt.xlabel('Время (сек)')
        #     plt.ylabel('Частота (Гц)')
        #     plt.colorbar().set_label('Интенсивность')
        #     # plt.axis('off')
        #     plt.show()

        #     # Вывод частотно-амплитудного спектра
        #     plt.figure(figsize=(10, 4))
        #     frequencies, amplitudes = np.fft.fftfreq(len(data), 1 / sampling_rate), np.abs(np.fft.fft(data))
        #     plt.plot(frequencies[:len(frequencies) // 2], amplitudes[:len(amplitudes) // 2])
        #     plt.title('Частотно-амплитудный спектр')
        #     plt.xlabel('Частота (Гц)')
        #     plt.ylabel('Амплитуда')
        #     # plt.axis('off')
        #     plt.show()

        #     print()


if __name__ == "__main__":
    main()
