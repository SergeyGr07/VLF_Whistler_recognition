import cv2
import numpy as np
import os
from pathlib import Path


def compare_images(img1, img2):
    # Сравнение двух изображений
    return cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)


def classify_image(input_image, templates_folder):
    # Загрузка входного изображения
    input_img = cv2.imread(input_image, cv2.IMREAD_GRAYSCALE)

    max_score = -1
    classification = None

    # Получение списка поддиректорий
    subfolders = [f.path for f in os.scandir(templates_folder) if f.is_dir()]

    # Сравнение входного изображения с каждым шаблоном в каждой поддиректории
    for subfolder in subfolders:
        templates = os.listdir(subfolder)
        for template in templates:
            template_img = cv2.imread(os.path.join(subfolder, template), cv2.IMREAD_GRAYSCALE)
            score = compare_images(input_img, template_img)

            # Если это совпадение лучше, чем предыдущее лучшее совпадение, то обновляем классификацию
            if np.max(score) > max_score:
                max_score = np.max(score)
                classification = os.path.basename(subfolder)  # Используем имя поддиректории в качестве классификации

    return classification


# def main():
#     dataset_dir = Path("input/predict")

#     # Вывести содержимое папки dataset
#     for file in dataset_dir.iterdir():
#         print(f"---{file}")
#         if file.is_file() and file.suffix.lower() == ".png":  # Проверяем, что файл - изображение формата PNG
#             filename = str(file)
#             print(classify_image(filename, 'templates_folder'))


# if __name__ == "__main__":
#     main()

print(classify_image('input/predict/PA090101044500_003.mat_21.png', 'templates_folder'))
