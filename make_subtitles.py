import argparse
from pathlib import Path

START = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   width="1080"
   height="1920"
   viewBox="0 0 285.74999 508"
   version="1.1"
   id="svg5"
   inkscape:version="1.2.2 (732a01da63, 2022-12-09)"
   sodipodi:docname="{docname}"
   inkscape:export-xdpi="96"
   inkscape:export-ydpi="96"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
'''

END = '</svg>\n'

PAGES_START = '''<sodipodi:namedview
     id="namedview7"
     pagecolor="#000000"
     bordercolor="#666666"
     borderopacity="0"
     inkscape:showpageshadow="2"
     inkscape:pageopacity="0"
     inkscape:pagecheckerboard="0"
     inkscape:deskcolor="#d1d1d1"
     inkscape:document-units="mm"
     showgrid="false"
     inkscape:zoom="0.11313708"
     inkscape:cx="0"
     inkscape:cy="0"
     inkscape:window-width="1920"
     inkscape:window-height="1001"
     inkscape:window-x="3191"
     inkscape:window-y="121"
     inkscape:window-maximized="1"
     inkscape:current-layer="layer1"
     showguides="true">
'''
PAGES_END = '  </sodipodi:namedview>\n'

PAGE = '''    <inkscape:page
       x="{x}"
       y="{y}"
       width="{width}"
       height="{height}"
       id="page{page_id}"
       inkscape:label="{scene_index:03}-{file_index:03}"
       inkscape:export-filename=".\subtitle-{scene_index:03}-{file_index:03}.png"
       inkscape:export-xdpi="96"
       inkscape:export-ydpi="96" />
'''

DEFS_START = '''<defs
     id="defs2">
'''

DEFS_END = '  </defs>\n'

RECT  = '''    <rect
       x="0"
       y="0"
       width="{width}"
       height="{height}"
       id="rect{rect_id}" />
'''

GROUP_START = '''  <g
     inkscape:label="Слой 1"
     inkscape:groupmode="layer"
     id="layer1"
     style="display:inline">
'''
#     transform="translate(1112.693,88.932614)">

GROUP_END = '  </g>\n'

#       transform="matrix(0.26458333,0,0,0.26458333,-1133.3671,-75.575264)"
TEXT_START = '''    <text
       xml:space="preserve"
       id="text{text_id}"
       transform="translate({x}, {y})"
       style="font-size:20px;line-height:1.25;font-family:sans-serif;text-align:center;white-space:pre;shape-inside:url(#{shape_inside_id});display:inline"
       x="0"
       y="0">'''

TEXT_END = '</text>\n'

TSPAN_START = '''<tspan
         x="0"
         y="0"
         id="tspan{tspan_id}">'''

TSPAN_START_HIGHLIGHT = '''<tspan
           style="font-weight:500;font-family:'Neo Sans Pro';-inkscape-font-specification:'Neo Sans Pro Medium';fill:#858dff;"
           id="tspan{tspan_id}">'''

TSPAN_START_USUAL = '''<tspan
           style="font-weight:500;font-family:'Neo Sans Pro';-inkscape-font-specification:'Neo Sans Pro Medium';fill:#ffffff;"
           id="tspan{tspan_id}">'''

TSPAN_END = '</tspan>'


def parse_args():
    parser = argparse.ArgumentParser(
        prog='make_subtitles',
        description='Make subtitles from text',
    )
    parser.add_argument('project', help='path to the project')
    return parser.parse_args()


class SVG:
    def __init__(self, page_width, page_height, docname):
        self.docname = docname
        self.page_width = page_width
        self.page_height = page_height
        self.pages = []
        self.texts = []
        self.rects = []
        self.page_id = iter(range(1, 1000))
        self.text_id = iter(range(1, 1000))
        self.tspan_id = iter(range(1, 2000))
        self.rect_id = iter(range(1, 1000))
    
    def add_page(self, x, y, scene, word_index):
        page = PAGE.format(
            height=self.page_height,
            width=self.page_width,
            x=x,
            y=y,
            page_id=next(self.page_id),
            scene_index=scene,
            file_index=word_index,
        )
        self.pages.append(page)
    
    def build_text(self, x, y, words, word_index_highlight):
        shape_inside_id = next(self.rect_id)
        self.rects.append(
            RECT.format(
                rect_id=shape_inside_id,
                height=self.page_height / 4,
                width=self.page_width,
            )
        )

        text_start = TEXT_START.format(
            text_id=next(self.text_id),
            shape_inside_id=f'rect{shape_inside_id}',
            x=x,
            y=y,
        )
        self.texts.append(text_start)

        for word_index, word in enumerate(words):
            if word_index == word_index_highlight:
                self.texts.append(TSPAN_START_HIGHLIGHT.format(tspan_id=next(self.tspan_id)))
            else:
                self.texts.append(TSPAN_START_USUAL.format(tspan_id=next(self.tspan_id)))

            self.texts.append(f'{word} ')
            self.texts.append(f'{TSPAN_END}')

        self.texts.append(f'{TEXT_END}\n')
    
    def write(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as svg_file:
            svg_file.write(START.format(docname=self.docname))
            svg_file.write(PAGES_START)
            svg_file.write('\n'.join(self.pages))
            svg_file.write(PAGES_END)
            svg_file.write(DEFS_START)
            svg_file.write(''.join(self.rects))
            svg_file.write(DEFS_END)
            svg_file.write(GROUP_START)
            svg_file.write(''.join(self.texts))
            svg_file.write(GROUP_END)
            svg_file.write(END)


def t2subtitles(text_file, subtitles_file_path):
    scene = 1
    y = 0
    x = 0
    scene_word_index = 1
    svg = SVG(page_width, page_height, subtitles_file_path.name)
    for line in text_file:
        line = line.strip()
        if not line:
            scene += 1
            y += page_height
            x = 0
            scene_word_index = 1
            continue

        words = line.split()
        for word_index, word in enumerate(words):
            svg.add_page(x, y, scene, scene_word_index)
            svg.build_text(x, y + (page_height - 200), words, word_index)
            x += page_width
            scene_word_index += 1


    svg.write(subtitles_file_path)


if __name__ == '__main__':
    page_height = 508
    page_width = 285.75

    args = parse_args()
    project_path = Path(args.project)
    text_file_path = project_path / 'text_to_subtitles.txt'
    subtitles_file_path = project_path / 'исходники' / 'subtitles.svg'
    with open(text_file_path, 'r', encoding='utf-8') as text_file:
        t2subtitles(text_file, subtitles_file_path)
