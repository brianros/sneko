from utils.ST7735 import TFT
from res.sysfont import sysfont
import random


def by8(XY):
    (x, y) = XY
    return (8 * x, 8 * y)


class Map:
    def __init__(self, tft):
        self.tft = tft
        self.grid = [[6 for _ in range(16)] for _ in range(16)]
      
    def read(self, XY):
        return self.grid[XY[0]][XY[1]]  

    def clearAll(self):
        self.tft.fill(TFT.BLACK)

    def drawBlack(self, XY):
        self.tft.fillrect(by8(XY), (8, 8), TFT.BLACK)

    def drawLetter(self, XY, letter):
        self.drawBlack(XY)
        self.tft.text(by8(XY), letter, TFT.WHITE, sysfont, 1)

    def write(self, XY, content):
        self.grid[XY[0]][XY[1]] = content
        if content == 0:
            self.drawLetter(XY, "S")
        elif content == 1:
            self.drawLetter(XY, "E")
        elif content == 2:
            self.drawLetter(XY, "K")
        elif content == 3:
            self.drawLetter(XY, "O")
        elif content == 4: # Wall
            self.tft.fillrect(by8(XY), (8, 8), TFT.WHITE)
        elif content == 5: # Eggplant
            (x, y) = XY
            self.device.drawer.draw_bmp('/sneko/res/eggplant.bmp', (8 * x - 4, 8 * y - 4))
        elif content == 6: # Empty
            self.drawBlack(XY)
        elif content == 7: # Blood
            self.tft.fillrect(by8(XY), (8, 8), TFT.RED)

    def dropEggplant(self):
        while True:
            x = random.randint(0, 15)
            y = random.randint(0, 15)
            if self.grid[x][y] == 6:
                self.write((x, y), 5)
                break

