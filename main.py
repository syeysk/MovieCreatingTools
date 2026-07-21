from pathlib import Path

from tools.img2video import img_to_mp4, make_vertical
from utils import IterData

OUT_DIR = Path(__file__).parent / 'out'

options = {'out_dir': OUT_DIR}

path_images_gen = IterData(r'A:\Изображения\Личное\Растения\tapo_night')
images_gen = IterData.init_from_gen(
    make_vertical(path_image, background='red', options=options) for path_image in path_images_gen.iter_pathes()
)
img_to_mp4(images_gen, '123456', 0.5, options=options)
