from device.graphics.ST7735 import TFT
from games.sneko.sneko import Sneko
from device.device import Device
import uasyncio # type: ignore


async def main():
    device = Device()

    sneko = Sneko(device)
    await sneko.run_game()


uasyncio.run(main())

