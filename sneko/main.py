from utils.ST7735 import TFT
from res.sysfont import sysfont
from sneko import Game
from device import Device
import uasyncio


async def waitForResetButton(device):
    while True:
        await uasyncio.sleep(0.01)
        x, y, button = device.joystick.read_joystick()
        if (button):
            break

async def main():
    device = Device()
    while True:
        game = Game(device)
        await game.runGame()
        device.tft.fill(TFT.BLACK)
        device.tft.text((60, 64), "Score: " + str(game.score), TFT.WHITE, sysfont, 1)
        await waitForResetButton(device)


uasyncio.run(main())

