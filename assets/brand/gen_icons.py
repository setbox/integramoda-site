import base64
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.dirname(HERE)
ROOT = os.path.dirname(ASSETS)
B64 = f'{HERE}/base64'
ICONS = f'{ASSETS}/favicon'

RED = '#FB0D1C'
WHITE = '#FFFFFF'
RADIUS = 0.22


def mark_paths():
    src = open(f'{HERE}/mark-trace.svg').read()
    vb = float(re.search(r'viewBox="0 0 ([\d.]+)', src).group(1))
    transform = re.search(r'<g transform="([^"]+)"', src).group(1)
    paths = re.findall(r'<path d="([^"]+)"', src)
    return vb, transform, paths


def mark_group(size, inset, fill):
    vb, transform, paths = mark_paths()
    m = size * inset
    off = (size - m) / 2
    inner = ''.join(f'<path fill="{fill}" d="{d}"/>' for d in paths)
    return (f'<g transform="translate({off:.3f} {off:.3f}) scale({m / vb:.6f}) '
            f'{transform}">{inner}</g>')


def svg(size, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
            f'width="{size}" height="{size}">{body}</svg>')


def icon_svg(size=1024, inset=0.72, rounded=True):
    r = f' rx="{size * RADIUS:.1f}"' if rounded else ''
    bg = f'<rect width="{size}" height="{size}"{r} fill="{RED}"/>'
    return svg(size, bg + mark_group(size, inset, WHITE))


def symbol_svg(size=512, fill=RED):
    body = mark_group(size, 1.0, fill)
    x, y, w, h = mark_bbox(size)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:.3f} {y:.3f} {w:.3f} {h:.3f}" '
            f'width="{w:.3f}" height="{h:.3f}">{body}</svg>')


def mark_bbox(size):
    probe = f'{HERE}/.tmp/probe.svg'
    png = f'{HERE}/.tmp/probe.png'
    open(probe, 'w').write(svg(size, mark_group(size, 1.0, RED)))
    subprocess.run(['rsvg-convert', '-w', '1024', '-h', '1024', probe, '-o', png], check=True)
    out = subprocess.run(['magick', png, '-trim', '-format', '%w %h %X %Y', 'info:'],
                         check=True, capture_output=True, text=True).stdout.split()
    w, h, x, y = (float(v.replace('+', '')) for v in out)
    k = size / 1024
    return x * k, y * k, w * k, h * k


def write(path, content):
    open(path, 'w').write(content)
    print(os.path.relpath(path, ROOT))


def render(svg_path, out, size, flatten=None):
    cmd = ['rsvg-convert', '-w', str(size), '-h', str(size)]
    if flatten:
        cmd += ['-b', flatten]
    cmd += [svg_path, '-o', out]
    subprocess.run(cmd, check=True)
    print(os.path.relpath(out, ROOT))


def render_width(svg_path, out, width):
    subprocess.run(['rsvg-convert', '-w', str(width), svg_path, '-o', out], check=True)
    print(os.path.relpath(out, ROOT))


def b64(src, out, mime):
    data = base64.b64encode(open(src, 'rb').read()).decode()
    open(out, 'w').write(f'data:{mime};base64,{data}\n')
    print(os.path.relpath(out, ROOT))


def main():
    os.makedirs(B64, exist_ok=True)
    os.makedirs(ICONS, exist_ok=True)
    tmp = f'{HERE}/.tmp'
    os.makedirs(tmp, exist_ok=True)

    subprocess.run(['python3', f'{HERE}/gen_svg.py'], check=True)

    write(f'{ASSETS}/icon.svg', icon_svg())
    write(f'{ASSETS}/logo-simbolo.svg', symbol_svg())
    write(f'{ASSETS}/logo-simbolo-invertido.svg', icon_svg(rounded=False))
    write(f'{ASSETS}/safari-pinned-tab.svg', symbol_svg(fill='#000000'))

    write(f'{tmp}/maskable.svg', icon_svg(inset=0.56, rounded=False))
    write(f'{tmp}/touch.svg', icon_svg(inset=0.68, rounded=False))
    write(f'{tmp}/mstile.svg', icon_svg(inset=0.60, rounded=False))

    render_width(f'{ASSETS}/logo-simbolo.svg', f'{ASSETS}/logo-simbolo.png', 1024)
    render(f'{ASSETS}/logo-simbolo-invertido.svg', f'{ASSETS}/logo-simbolo-invertido.png', 1024)
    render_width(f'{ASSETS}/logo-horizontal.svg', f'{ASSETS}/logo-horizontal.png', 2110)
    render_width(f'{ASSETS}/logo-horizontal-dark.svg', f'{ASSETS}/logo-horizontal-dark.png', 2110)

    for size in (16, 32, 48):
        render(f'{ASSETS}/icon.svg', f'{ICONS}/favicon-{size}x{size}.png', size)
    for size in (192, 512):
        render(f'{ASSETS}/icon.svg', f'{ICONS}/android-chrome-{size}x{size}.png', size)

    render(f'{tmp}/touch.svg', f'{ROOT}/apple-touch-icon.png', 180)
    render(f'{tmp}/maskable.svg', f'{ICONS}/android-chrome-maskable-512x512.png', 512)
    render(f'{tmp}/mstile.svg', f'{ICONS}/mstile-150x150.png', 150)

    subprocess.run(
        ['magick', f'{ICONS}/favicon-16x16.png', f'{ICONS}/favicon-32x32.png',
         f'{ICONS}/favicon-48x48.png', f'{ROOT}/favicon.ico'], check=True)
    print('favicon.ico')

    subprocess.run(['magick', f'{ROOT}/apple-touch-icon.png', '-background', RED,
                    '-alpha', 'remove', '-alpha', 'off',
                    f'{ROOT}/apple-touch-icon.png'], check=True)

    b64(f'{ASSETS}/icon.svg', f'{B64}/icon.svg.txt', 'image/svg+xml')
    b64(f'{ASSETS}/logo-simbolo.svg', f'{B64}/logo-simbolo.svg.txt', 'image/svg+xml')
    b64(f'{ASSETS}/logo-horizontal.svg', f'{B64}/logo-horizontal.svg.txt', 'image/svg+xml')
    b64(f'{ASSETS}/logo-horizontal-dark.svg', f'{B64}/logo-horizontal-dark.svg.txt', 'image/svg+xml')
    b64(f'{ICONS}/favicon-32x32.png', f'{B64}/favicon-32x32.png.txt', 'image/png')
    b64(f'{ASSETS}/logo-horizontal.png', f'{B64}/logo-horizontal.png.txt', 'image/png')

    for f in os.listdir(tmp):
        os.remove(f'{tmp}/{f}')
    os.rmdir(tmp)


if __name__ == '__main__':
    main()
