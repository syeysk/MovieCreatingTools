import os
import os.path
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def img_to_mp4(path_images_gen, vid_name: str, duration: int, transformer=None):
    """
    :param path_images_gen: генератор путей к изображению
    :param vid_name: имя результирующего видео mp4
    :param duration: время длительности клипа в секундах
    """
    f_rate = 30.0
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_scr = None

    for path_image in path_images_gen:
        img = Image.open(path_image)        
        if transformer:
            img = transformer(img)

        if out_scr is None:
            out_scr = cv2.VideoWriter(f"{vid_name}.mp4", fourcc, f_rate, (img.width, img.height))

        for im in range(0, int(duration * f_rate)):
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out_scr.write(frame)


def make_vertical(img):
    # Vertical (9:16) (1080x1920 pixels) (540x960 pixels)
    transformed_h = int(img.height * 1080 / img.width)
    img = img.resize((1080, transformed_h))
    new_img = Image.new(img.mode, (1080, 1920), 'blue')
    new_img.paste(img, (0, (1920 - transformed_h) // 2))
    return new_img


def image_walker(any_pathes):
    for any_path in any_pathes:
        any_path = Path(any_path)
        if not any_path.exists():
            print(f'Путь не существует: {any_path}')
            continue

        if any_path.is_dir():
            for directory, _, filenames in os.walk(any_pathes):
                for filename in filenames:
                    yield Path(os.path.join(directory, filename))
        else:
            yield any_path


path_images_gen = image_walker(r'A:\Изображения\Личное\Растения\tapo_day')
img_to_mp4(list(path_images_gen)[:-1], '123456', 0.5)