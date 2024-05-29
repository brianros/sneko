from device.graphics.ST7735 import TFT
from device.res.sysfont import sysfont
from games.sneko.sneko import Sneko
from device.device import Device
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
        sneko = Sneko(device)
        await sneko.runGame()
        device.tft.fill(TFT.BLACK)
        device.tft.text((60, 64), "Score: " + str(sneko.score), TFT.WHITE, sysfont, 1)
        await waitForResetButton(device)


uasyncio.run(main())

