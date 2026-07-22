from pathlib import Path

from tools.img2video import img_to_mp4, make_vertical
from tools.make_subtitles import t2subtitles
from tools.extern_inkscape import export_svg
from utils import IterData

OUT_DIR = Path(__file__).parent / 'out'
if not OUT_DIR.exists():
    OUT_DIR.mkdir()

options = {'out_dir': OUT_DIR}

# path_images_gen = IterData(r'A:\Изображения\Личное\Растения\tapo_night')
# images_gen = IterData.init_from_gen(
#     make_vertical(path_image, background='red', options=options) for path_image in path_images_gen.iter_pathes()
# )
# img_to_mp4(images_gen, '123456', 0.5, options=options)

text_file_path = 'A:\\Проекты\\_видео_syeysk\\008-django-generic-foreign-key\\text_to_subtitles.txt'
with open(text_file_path, 'r', encoding='utf-8') as text_file:
    svg_path = t2subtitles(text_file, options=options)
    export_svg(svg_path, options=options)
