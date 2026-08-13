import subprocess
from uuid import uuid4
from pathlib import Path

from config import INKSCAPE_PATH


def check_inkscape_version(major, minor):
    try:
        result = subprocess.run([INKSCAPE_PATH, '--version'], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as error:
        print('error:', error.stderr)
    else:
        result_str = result.stdout.split()
        if result_str and result_str[0] == 'Inkscape':
            version_parts = result_str[1].split('.')
            return int(version_parts[0]) >= major and int(version_parts[1]) >= minor


def export_svg(svg_path: Path, pages='all', options=dict()):
    if not check_inkscape_version(1, 3):
        print('Требуутся Inkscape версии >= 1.3')
        return
        
    out_dir = options['out_dir'] / uuid4().hex
    if not out_dir.exists():
        out_dir.mkdir()

    try:
        result = subprocess.run(
            [INKSCAPE_PATH, '--export-type=png', f'--export-page={pages}', '-o', str(out_dir / 'output.png'), str(svg_path)],
            check=True,
            capture_output=True,
            text=True,
        )
        print(result.stdout)
    except subprocess.CalledProcessError as error:
        print('error:', error.stderr)

    return out_dir
