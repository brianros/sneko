from device.graphics.ST7735 import TFT
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
        await sneko.run_game()
        device.graphics.clear_screen()
        device.graphics.write_text((60, 64), "Score: " + str(sneko.score), TFT.WHITE)
        highscores_music = uasyncio.create_task(device.buzzer.play_highscores_tune())
        await waitForResetButton(device)
        highscores_music.cancel()


uasyncio.run(main())

