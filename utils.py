from os import walk
from pathlib import Path
from typing import Any, Generator

from PIL import Image


class IterData:
    def __init__(self, *data):
        self.data: list[str | Path | Any] = list(data)
    
    @classmethod
    def init_from_gen(_class, gen):
        obj = _class()
        obj.data = gen
        return obj

    def iter_pathes(self) -> Generator[Path | Any, None, None]:
        for item in self.data:
            if isinstance(item, str):
                item = Path(item)

            if not isinstance(item, Path):
                yield item
                continue

            if not item.exists():
                print(f'Путь не существует: {item}')
                continue

            if item.is_dir():
                for directory, _, filenames in walk(item):
                    for filename in filenames:
                        yield Path(directory) / filename
            else:
                yield item

    def iter_images(self, mode: str) -> Generator[Image.Image, None, None]:
        for path_image in self.iter_pathes():
            if isinstance(path_image, Path):
                yield Image.open(str(path_image), mode)
            elif isinstance(path_image, Image.Image):
                yield path_image
            else:
                print('Неверный формат объекта:', type(path_image))

    def append(self, item):
        self.data.append(item)
