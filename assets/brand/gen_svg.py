import re
import sys
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

import os

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.dirname(HERE)

FONT = f'{HERE}/fonts/Manrope.ttf'
MARK_SVG = sys.argv[1] if len(sys.argv) > 1 else f'{HERE}/mark-trace.svg'

NAME = 'Integra Moda'

M = 512
MARK_SCALE = 0.78
PAD = int(M * 0.10)
GAP = int(M * 0.16)
SIZE_NAME = int(M * 0.44)
TRACK_NAME = M * 0.44 * -0.015

RED = '#FB0D1C'


def instance_coords(style):
    f = TTFont(FONT)
    names = f['name']
    for inst in f['fvar'].instances:
        if names.getDebugName(inst.subfamilyNameID) == style:
            return dict(inst.coordinates)
    raise SystemExit(f'instance {style} not found')


class Face:
    def __init__(self, style):
        self.coords = instance_coords(style)
        self.tt = instantiateVariableFont(TTFont(FONT), self.coords, updateFontNames=False)
        self.upem = self.tt['head'].unitsPerEm
        self.glyphset = self.tt.getGlyphSet()
        blob = hb.Blob.from_file_path(FONT)
        face = hb.Face(blob)
        self.hb = hb.Font(face)
        self.hb.scale = (self.upem, self.upem)
        self.hb.set_variations(self.coords)

    def cap_height(self, size):
        return self.tt['glyf']['H'].yMax * size / self.upem

    def shape(self, text):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf)
        return buf.glyph_infos, buf.glyph_positions

    def run(self, text, size, track, x, y, fill):
        s = size / self.upem
        infos, poss = self.shape(text)
        out = []
        for info, pos in zip(infos, poss):
            gname = self.tt.getGlyphName(info.codepoint)
            pen = SVGPathPen(self.glyphset)
            self.glyphset[gname].draw(pen)
            d = pen.getCommands()
            if d:
                gx = x + pos.x_offset * s
                gy = y - pos.y_offset * s
                color = fill(info.cluster) if callable(fill) else fill
                out.append(
                    f'<path transform="translate({gx:.3f} {gy:.3f}) scale({s:.6f} {-s:.6f})" '
                    f'fill="{color}" d="{d}"/>'
                )
            x += pos.x_advance * s + track
        return out, x

    def width(self, text, size, track):
        _, poss = self.shape(text)
        s = size / self.upem
        return sum(p.x_advance * s for p in poss) + track * (len(poss) - 1)


def mark_group(tx, ty, target):
    src = open(MARK_SVG).read()
    vb = float(re.search(r'viewBox="0 0 ([\d.]+)', src).group(1))
    transform = re.search(r'<g transform="([^"]+)"', src).group(1)
    paths = re.findall(r'<path d="([^"]+)"', src)
    k = target / vb
    inner = ''.join(f'<path fill="{RED}" d="{d}"/>' for d in paths)
    return (f'<g transform="translate({tx} {ty}) scale({k:.6f}) {transform}">{inner}</g>')


def build(out, name_color, with_text=True):
    bold = Face('Bold')

    if not with_text:
        w = h = M
        body = mark_group(0, 0, M)
    else:
        text_w = bold.width(NAME, SIZE_NAME, TRACK_NAME)
        w = int(PAD + M + GAP + text_w + PAD)
        h = M + 2 * PAD
        cap_n = bold.cap_height(SIZE_NAME)
        tx = PAD + M + GAP
        base_n = PAD + M / 2 + cap_n / 2

        highlight = NAME.index('Moda')

        mark = M * MARK_SCALE
        body = mark_group(PAD + (M - mark) / 2, PAD + (M - mark) / 2, mark)
        body += ''.join(bold.run(
            NAME, SIZE_NAME, TRACK_NAME, tx, base_n,
            lambda c: RED if c >= highlight else name_color)[0])

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
           f'width="{w}" height="{h}" fill="none">{body}</svg>')
    open(out, 'w').write(svg)
    print(out, w, h, len(svg), 'bytes')


if __name__ == '__main__':
    build(f'{ASSETS}/logo-simbolo.svg', None, with_text=False)
    build(f'{ASSETS}/logo-horizontal.svg', '#000000')
    build(f'{ASSETS}/logo-horizontal-dark.svg', '#FFFFFF')
