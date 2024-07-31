import device.graphics.graphics
from device.graphics.ST7735 import TFT
import random


letters = ['S', 'E', 'K', 'O']
eggplantPath = '/games/sneko/res/eggplant.bmp'

class MapContent:
    S = 0
    E = 1
    K = 2
    O = 3
    EGGPLANT = 4
    WALL = 5
    EMPTY = 6
    BLOOD = 7

def by8(XY):
    (x, y) = XY
    return (8 * x, 8 * y)

class Map:
    def __init__(self, graphics):
        self.graphics = graphics
        self.grid = [[MapContent.EMPTY for _ in range(16)] for _ in range(16)]
        self.graphics.clear_screen()
    
    def read(self, XY):
        return self.grid[XY[0]][XY[1]]  

    def write(self, XY, content):
        (x, y) = XY
        self.grid[x][y] = content
        if content < 4:
            self.graphics.fill_rect(by8(XY), (8, 8), TFT.BLACK)
            self.graphics.write_text(by8(XY), letters[content])
        elif content == MapContent.EGGPLANT:
            self.graphics.draw_bmp(eggplantPath, by8(XY))
        elif content == MapContent.WALL:
            self.graphics.fill_rect(by8(XY), (8, 8), TFT.WHITE)
        elif content == MapContent.EMPTY:
            self.graphics.fill_rect(by8(XY), (8, 8), TFT.BLACK)
        elif content == MapContent.BLOOD:
            self.graphics.fill_rect(by8(XY), (8, 8), TFT.RED)

    def drop_eggplant(self):
        while True:
            XY = (random.randint(0, 15), random.randint(0, 15))
            if self.read(XY) == MapContent.EMPTY:
                self.write(XY, MapContent.EGGPLANT)
                break

