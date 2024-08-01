import uasyncio
from device import graphics
import peripherals.graphics.colors as colors


FROG_SIZE = 5
START_Y_POS = 120
JUMP_DURATION = 0.5

class Position:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def is_valid(self):
        return 0 <= self.x and self.x < 128 and 0 <= self.y and self.y < 128

    def get_tuple(self):
        return(self.x, self.y)

    def advance(self):
        self.y = self.y - 1


position = Position(-1, -1)

def draw_frog(stretch = 0):
    if not position.is_valid():
        raise Exception(f"Invalid frog position {position}")

    pos = position.get_tuple()
    size = FROG_SIZE + stretch
    graphics.fill_circle(pos, size + 3, colors.BLACK)
    graphics.fill_circle(pos, size, colors.RED)
    graphics.fill_circle(pos, size - 1, colors.GREEN)

def reset_frog(x):
    global position
    position = Position(x, START_Y_POS)
    draw_frog()

async def jump():
    global position
    for frame in range(8):
        position.advance()
        stretch = min(frame, 7 - frame)
        draw_frog(stretch)
        await uasyncio.sleep(JUMP_DURATION/8)

async def animation():
    await uasyncio.sleep(2)
    await jump()
    await uasyncio.sleep(0.8)
    await jump()
    await uasyncio.sleep(1.3)
    await jump()
    await uasyncio.sleep(0.2)
    await jump()
    await uasyncio.sleep(0)
    await jump()
    await uasyncio.sleep(1)
    await jump()
    await uasyncio.sleep(1)


reset_frog(40)
draw_frog()
uasyncio.run(animation())

