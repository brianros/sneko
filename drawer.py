
class BMPDrawer:
    def __init__(self, spi, dc, cs, rst):
        self.tft = TFT(spi, dc, cs, rst)
        self.tft.initr()
        self.tft.rgb(True)
        self.tft.fill(TFT.BLACK)
    
    def draw_bmp(self, filename, position=(0,0)):
        x, y = position
        f = open(filename, 'rb')
        if f.read(2) == b'BM':  # header
            f.read(8)  # file size(4), creator bytes(4)
            offset = int.from_bytes(f.read(4), 'little')
            hdrsize = int.from_bytes(f.read(4), 'little')
            width = int.from_bytes(f.read(4), 'little')
            height = int.from_bytes(f.read(4), 'little')
            if int.from_bytes(f.read(2), 'little') == 1:  # planes must be 1
                depth = int.from_bytes(f.read(2), 'little')
                if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:  # uncompressed
                    print("Image size:", width, "x", height)
                    rowsize = (width * 3 + 3) & ~3
                    if height < 0:
                        height = -height
                        flip = False
                    else:
                        flip = True
                    w, h = width, height
                    if w > 128: w = 128
                    if h > 128: h = 128
                    self.tft._setwindowloc((x, y), (x + w - 1, y + h - 1))
                    for row in range(h):
                        if flip:
                            pos = offset + (height - 1 - row) * rowsize
                        else:
                            pos = offset + row * rowsize
                        if f.tell() != pos:
                            f.seek(pos)
                        for col in range(w):
                            bgr = f.read(3)
                            self.tft._pushcolor(TFTColor(bgr[2], bgr[1], bgr[0]))
        f.close()
