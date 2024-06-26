import device.graphics.graphics
from device.graphics.ST7735 import TFT
import random


letters = ['S', 'E', 'K', 'O']
eggplantPath = '/games/sneko/res/eggplant.bmp'

class Content:
    S = 0
    E = 1
    K = 2
    O = 3
    Eggplant = 4
    Wall = 5
    Empty = 6
    Blood = 7

def by8(XY):
    (x, y) = XY
    return (8 * x, 8 * y)

class Map:
    def __init__(self, graphics):
        self.graphics = graphics
        self.grid = [[Content.Empty for _ in range(16)] for _ in range(16)]
        self.graphics.clear_screen()
    
    def read(self, XY):
        return self.grid[XY[0]][XY[1]]  

    def write(self, XY, content):
        (x, y) = XY
        self.grid[x][y] = content
        if content < 4:
            self.graphics.write_text(by8(XY), letters[content])
        elif content == Content.Eggplant:
            self.graphics.draw_bmp(eggplantPath, by8(XY))
        elif content == Content.Wall:
            self.graphics.fill_rect(by8(XY), (8, 8), TFT.WHITE)
        elif content == Content.Empty:
            self.graphics.fill_rect(by8(XY), (8, 8), TFT.BLACK)
        elif content == Content.Blood:
            self.graphics.fill_rect(by8(XY), (8, 8), TFT.RED)

    def dropEggplant(self):
        while True:
            XY = (random.randint(0, 15), random.randint(0, 15))
            if self.read(XY) == Content.Empty:
                self.write(XY, Content.Eggplant)
                break

