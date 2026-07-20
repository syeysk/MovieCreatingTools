import cv2
import numpy as np
from PIL import Image


def img_to_mp4(path_images_gen, vid_name: str, duration: int, transformer=None, **kwargs):
    """
    :param path_images_gen: генератор путей к изображению
    :param vid_name: имя результирующего видео mp4
    :param duration: длительность одной картинки в секундах
    """
    f_rate = 30.0
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_scr = None
    for path_image in path_images_gen:
        img = Image.open(str(path_image))      
        if transformer:
            img = transformer(img)

        if out_scr is None:
            out_scr = cv2.VideoWriter(f"{vid_name}.mp4", fourcc, f_rate, (img.width, img.height))

        for _ in range(0, int(duration * f_rate)):
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out_scr.write(frame)


def make_vertical(img, out_w=1080, out_h=1920, **kwargs):
    # Vertical (9:16) (1080x1920 pixels) (540x960 pixels)
    transformed_h = int(img.height * out_w / img.width)
    img = img.resize((out_w, transformed_h))
    new_img = Image.new(img.mode, (out_w, out_h), 'blue')
    new_img.paste(img, (0, (out_h - transformed_h) // 2))
    return new_img
