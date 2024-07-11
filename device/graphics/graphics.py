import uasyncio # type: ignore
from machine import SPI, Pin # type: ignore
from device.graphics.ST7735 import TFT, TFTColor
from device.graphics.sysfont import sysfont


class Graphics:
    def __init__(self):
        self.spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(14), mosi=Pin(15), miso=None)
        self.tft = TFT(self.spi, 16, 17, 18)
        self.tft.initr()
        self.tft.rgb(False)
        self.clear_screen()

    def clear_screen(self):
        self.tft.fill(TFT.BLACK)
    
    def fill_rect(self, pos, size, color):
        self.tft.fillrect(pos, size, color)
    
    def fill_circle(self, pos, radius, color):
        self.tft.fillcircle(pos, radius, color)

    def write_text(self, pos, text, color = TFT.WHITE, size = 1, nowrap = False):
        self.tft.text(pos, text, color, sysfont, size, nowrap)

    def draw_bmp(self, filename, position):
        uasyncio.create_task(self.draw_bmp_coroutine(filename, position, 10000000, 0))

    async def draw_bmp_coroutine(self, filename, position, chunk_pixels = 100, chunk_pause = 0):
        pixel_count = 0
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
                    # print("Image size:", width, "x", height)
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

                            pixel_count = pixel_count + 1
                            if pixel_count % chunk_pixels == 0:
                                await uasyncio.sleep(chunk_pause)
        f.close()

