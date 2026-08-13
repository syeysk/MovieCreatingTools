"""
## Format of `text_to_audio.txt` file

- one line is one audio file (if it's not empty file)
- block between empty lines  is a scene
"""

import argparse
import base64
from pathlib import Path

import requests

from config import YANDEX_CLOUD_SECRET_KEY


def t2audio(text, audio_file_path):
    target = 'https://tts.api.cloud.yandex.net/tts/v3/utteranceSynthesis'
    request_data = {
        'text': text,
        'hints': [
            {'speed': 1.2},
            {'voice': 'filipp'},
        ]
    }
    headers = {
        'Authorization': f'Api-Key {YANDEX_CLOUD_SECRET_KEY}'
    }
    response = requests.post(target, json=request_data, timeout=25, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        chunk_base64 = response_data['result']['audioChunk']['data']
        #start = response_data['result']['audioChunk']['startMs']
        #length = response_data['result']['audioChunk']['lengthMs']
        chunk_bin = base64.b64decode(chunk_base64)
        with open(audio_file_path, 'wb') as audio_file:
            audio_file.write(chunk_bin)

    from http.client import responses
    print('   ', response.status_code, responses[response.status_code]), response.text)


def parse_args():
    parser = argparse.ArgumentParser(
        prog='t2audio',
        description='Convert text to audio',
    )
    parser.add_argument('project', help='path to the project')
    return parser.parse_args()


def gen_text(text_file_path, audio_files_path):
    audio_file_name_template = 'audio-{scene_index:03}-{file_index:03}.wav'
    scene = 1
    audio = 0
    with open(text_file_path, 'r', encoding='utf-8') as text_file:
        for line in text_file:
            line = line.strip()
            if line:
                audio += 1
            else:
                scene += 1
                audio = 0
                continue

            #if len(line) > 250:
            #    print('line has more 250 characters')
            #    break

            audio_file_path = audio_files_path / audio_file_name_template.format(scene_index=scene, file_index=audio)
            print(audio_file_path.name, '\n   ', line)
            if audio_file_path.exists():
                print('    audio already exists\n')
                continue

            yield line, audio_file_path
            print('    ready\n')


if __name__ == '__main__':
    args = parse_args()
    project_path = Path(args.project)
    text_file_path = project_path / 'text_to_audio.txt'
    audio_files_path = project_path / 'исходники'
    for line, audio_file_path in gen_text(text_file_path, audio_files_path):
        t2audio(line, audio_file_path)