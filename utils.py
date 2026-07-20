from os import walk
from pathlib import Path


def walker(*any_pathes):
    for any_path in any_pathes:
        any_path = Path(any_path)
        if not any_path.exists():
            print(f'Путь не существует: {any_path}')
            continue

        if any_path.is_dir():
            for directory, _, filenames in walk(any_path):
                for filename in filenames:
                    yield Path(directory) / filename
        else:
            yield any_path

