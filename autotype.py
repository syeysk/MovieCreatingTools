# about keyboard module: https://habr.com/ru/articles/579942/


'''
text = """from PIL import Image
import earthpy.spatial as es
import numpy


image_array = numpy.array(\x7fImage.open(\x7f'\x7ftest_image.tif'))
ndvi_array = es.normalized_diff(\x7f
image_array[:, :, 3], image_array[:, :, 2],
\b)
Image.fromarray(\x7fndvi_array).save(\x7f'\x7foutput.tif')
"""
with open('text_to_type.txt', 'w', encoding="utf-8") as f:
    f.write(text)
exit()
'''


import time
import argparse

import keyboard


parser = argparse.ArgumentParser(
    prog='autotyper',
    description='Type any text',
)
parser.add_argument('input_path')
parser.add_argument('-w', '--wait-before-typing', help='example: 1, 0.5 (secs)', default=5, type=float)
parser.add_argument('-d', '--delay', help='example: 1, 0.5 (secs)', default=0.1, type=float)
args = parser.parse_args()

time.sleep(args.wait_before_typing)

with open(args.input_path, encoding='utf-8') as input_file:
    input_text = input_file.read()
    #input_text = input_text.replace('\n', '\x1b\n').replace('.', '.\x1b')
    for s in input_text:
        if (s == '\x7f'):
            keyboard.send('del')
        else:
            keyboard.write(s)

        time.sleep(args.delay)
        keyboard.send('esc')
