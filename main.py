from tools.img2video import img_to_mp4, make_vertical
from utils import walker


path_images_gen = walker(r'A:\Изображения\Личное\Растения\tapo_night')
img_to_mp4(list(path_images_gen)[:-1], '123456', 0.5)
