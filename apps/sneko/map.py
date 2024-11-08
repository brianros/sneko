import device
import random
import peripherals.graphics.colors as colors


letters = ['S', 'E', 'K', 'O']
eggplantPath = '/apps/sneko/res/eggplant.bmp'

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
    def __init__(self):
        self.grid = [[MapContent.EMPTY for _ in range(16)] for _ in range(16)]
        device.display.clear_screen()
    
    def read(self, XY):
        return self.grid[XY[0]][XY[1]]  

    def write(self, XY, content):
        (x, y) = XY
        self.grid[x][y] = content
        if content < 4:
            device.display.fill_rect(by8(XY), (8, 8), colors.BLACK)
            device.display.write_text(by8(XY), letters[content])
        elif content == MapContent.EGGPLANT:
            device.display.draw_bmp(eggplantPath, by8(XY))
        elif content == MapContent.WALL:
            device.display.fill_rect(by8(XY), (8, 8), colors.WHITE)
        elif content == MapContent.EMPTY:
            device.display.fill_rect(by8(XY), (8, 8), colors.BLACK)
        elif content == MapContent.BLOOD:
            device.display.fill_rect(by8(XY), (8, 8), colors.RED)

    def drop_eggplant(self):
        while True:
            XY = (random.randint(0, 15), random.randint(0, 15))
            if self.read(XY) == MapContent.EMPTY:
                self.write(XY, MapContent.EGGPLANT)
                break

