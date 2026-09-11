import os
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = f'{HERE}/mark-source-alpha.png'
OUT = f'{HERE}/mark-trace.svg'

RADIUS = int(sys.argv[1]) if len(sys.argv) > 1 else 5
UPSCALE = 4


def main():
    tmp = f'{HERE}/.tmp'
    os.makedirs(tmp, exist_ok=True)

    dilated = f'{tmp}/alpha-dilated.png'
    subprocess.run(['magick', SOURCE, '-morphology', 'Dilate', f'Disk:{RADIUS}', dilated],
                   check=True)

    img = Image.open(dilated).convert('L')
    bbox = img.point(lambda p: 255 if p > 8 else 0).getbbox()
    img = img.crop(bbox)
    w, h = img.size
    side = max(w, h)
    square = Image.new('L', (side, side), 0)
    square.paste(img, ((side - w) // 2, (side - h) // 2))
    squared = f'{tmp}/alpha-squared.png'
    square.save(squared)

    pbm = f'{tmp}/mark.pbm'
    subprocess.run(['magick', squared, '-resize', f'{UPSCALE * 100}%',
                    '-threshold', '50%', '-negate', pbm], check=True)
    subprocess.run(['potrace', '-s', '--flat', '-a', '1.0', '-O', '0.2', '-t', '4',
                    '-o', OUT, pbm], check=True)

    for f in os.listdir(tmp):
        os.remove(f'{tmp}/{f}')
    os.rmdir(tmp)

    print(f'{OUT} - dilatação Disk:{RADIUS}, bbox {bbox}, canvas {side}x{side}')


if __name__ == '__main__':
    main()
