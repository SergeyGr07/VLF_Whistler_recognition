import struct
# import numpy as np


def read_sets_file(file_path):
    with open(file_path, 'rb') as file:
        # Чтение данных из файла
        data = file.read(200)
        # data_bin = np.fromfile(file, dtype=np.int16)
        # print(data_bin)
        buffer_size = 22 if len(data) >= 22 else len(data)

        # Распаковка данных в соответствии с форматом, указанным в документации
        # В примере, я просто вывожу некоторые значения, но вы можете использовать их по своему усмотрению
        adc_n_ch, adc_range, adc_clock, adc_s, adc_mode, adc_clk_source = struct.unpack('BBdIBB', data[:buffer_size])
        # adc_fifo_state, adc_fifo_status, adc_model = struct.unpack(f'{buffer_size_96}sB32s', data[buffer_size_24:(buffer_size_24 + buffer_size_96)])
        # adc_input_mode, adc_real_time_fifo, adc_real_time_usb_packet = struct.unpack('BII', data[buffer_size_96:(buffer_size_96 + buffer_size_129)])
        # adc_id, adc_fs, adc_delay, adc_dt, adc_gen_demod_once = struct.unpack('BdIdd?', data[132:149])
        # gps_com_port, gps_bit_rate, gps_time_set = struct.unpack('128sIB', data[149:280])
        # gps_latitude, gps_longitude = struct.unpack('dd', data[280:296])
        # station_list = struct.unpack('1024s', data[296:1320])[0].decode('utf-8').split('\x00')
        rest_of_data = file.read()

        # Возвращение значений (это просто пример, замените его на свои нужды)
        return {
            'ADC_N_Channels': adc_n_ch,
            'ADC_Range': adc_range,
            'ADC_Clock': adc_clock,
            'ADC_S': adc_s,
            'ADC_Mode': adc_mode,
            'ADC_ClkSource': adc_clk_source,
            'Rest_Of_Data': rest_of_data,
            # 'ADC_InputMode': adc_input_mode,
            # 'ADC_RealTime_FIFO': adc_real_time_fifo,
            # 'ADC_RealTime_USB_Packet': adc_real_time_usb_packet,
            # 'ADC_FIFO_State': adc_fifo_state.decode('utf-8').strip('\x00'),
            # 'ADC_FIFO_Status': bool(adc_fifo_status),
            # 'ADC_Model': adc_model.decode('utf-8').strip('\x00'),
            # 'ADC_ID': adc_id,
            # 'ADC_Fs': adc_fs,
            # 'ADC_Delay': adc_delay,
            # 'ADC_dt': adc_dt,
            # 'ADC_GenDemodOnce': adc_gen_demod_once,
            # 'GPS_COM_Port': gps_com_port.decode('utf-8').strip('\x00'),
            # 'GPS_BitRate': gps_bit_rate,
            # 'GPS_TimeSet': gps_time_set,
            # 'GPS_Latitude': gps_latitude,
            # 'GPS_Longitude': gps_longitude,
            # 'Station_List': station_list
        }


# Пример использования
sets_file_path = 'January 2022/Broadband_Sets_2022.01.01_23.35.00.bin'
sets_data = read_sets_file(sets_file_path)

# Вывод информации (это просто пример, замените его на свои нужды)
for key, value in sets_data.items():
    print(f'{key}: {value}')


# # train the model
# epochs = 20 # количество эпох тренировки
# history = model.fit(
# 	train_ds,
# 	validation_data=val_ds,
# 	epochs=epochs,
# 	callbacks=[early_stopping])

# # visualize training and validation results
# acc = history.history['accuracy']
# val_acc = history.history['val_accuracy']

# loss = history.history['loss']
# val_loss = history.history['val_loss']

# epochs_range = range(epochs)

# plt.figure(figsize=(8, 8))
# plt.subplot(1, 2, 1)
# plt.plot(epochs_range, acc, label='Training Accuracy')
# plt.plot(epochs_range, val_acc, label='Validation Accuracy')
# plt.legend(loc='lower right')
# plt.title('Training and Validation Accuracy')

# plt.subplot(1, 2, 2)
# plt.plot(epochs_range, loss, label='Training Loss')
# plt.plot(epochs_range, val_loss, label='Validation Loss')
# plt.legend(loc='upper right')
# plt.title('Training and Validation Loss')
# plt.show()



# from tensorflow.keras import callbacks
# # create model
# num_classes = len(class_names)
# model = Sequential([
# 	# т.к. у нас версия TF 2.6 локально
# 	layers.experimental.preprocessing.Rescaling(1./255, input_shape=(img_height, img_width, 3)),

# 	# дальше везде одинаково
# 	layers.Conv2D(16, 3, padding='same', activation='relu'),
# 	layers.MaxPooling2D(),

# 	layers.Conv2D(32, 3, padding='same', activation='relu'),
# 	layers.MaxPooling2D(),

# 	layers.Conv2D(64, 3, padding='same', activation='relu'),
# 	layers.MaxPooling2D(),
    
#     layers.Flatten(),
#     layers.Dropout(0.5),  # Добавление Dropout слоя для уменьшения переобучения
#     layers.Dense(128, activation='relu'),
#     layers.Dropout(0.5),  # Добавление еще одного Dropout слоя
#     layers.Dense(num_classes, activation='softmax')
# ])

# # compile the model
# model.compile(
# 	optimizer='adam',
# 	loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
# 	metrics=['accuracy'])

# # print model summary
# model.summary()

# # создание функции ранней остановки
# early_stopping = callbacks.EarlyStopping(
#     min_delta=0.001,  # минимальное изменение ошибки для остановки
#     patience=10,  # сколько эпох ждать перед остановкой
#     restore_best_weights=True,
# )