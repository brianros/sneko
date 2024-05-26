# bmp_drawer.py
from ST7735 import TFT, TFTColor

def draw_bmp(tft, bmp_file, position=(0, 0)):
    with open(bmp_file, 'rb') as f:
        if f.read(2) == b'BM':  # header
            f.seek(10)
            offset = int.from_bytes(f.read(4), 'little')
            hdrsize = int.from_bytes(f.read(4), 'little')
            width = int.from_bytes(f.read(4), 'little')
            height = int.from_bytes(f.read(4), 'little')
            if int.from_bytes(f.read(2), 'little') == 1:  # planes must be 1
                depth = int.from_bytes(f.read(2), 'little')
                if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:  # uncompressed
                    rowsize = (width * 3 + 3) & ~3
                    if height < 0:
                        height = -height
                        flip = False
                    else:
                        flip = True
                    w, h = width, height
                    if w > 128: w = 128
                    if h > 128: h = 128
                    tft._setwindowloc(position, (position[0] + w - 1, position[1] + h - 1))
                    for row in range(h):
                        pos = offset + (height - 1 - row) * rowsize if flip else offset + row * rowsize
                        f.seek(pos)
                        for col in range(w):
                            bgr = f.read(3)
                            tft._pushcolor(TFTColor(bgr[2], bgr[1], bgr[0]))
