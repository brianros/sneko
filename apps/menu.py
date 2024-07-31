import uasyncio
import device
import peripherals.graphics.colors as colors
from peripherals.audio.music import startup_tune
from apps.sneko.sneko import Sneko


async def run():
    device.graphics.write_text((16, 32), "hey there pretty")
    await device.audio.play_score(startup_tune, 0.01)
    animation_task = uasyncio.create_task(sleepy_wait_animation())
    await device.joystick.wait_for_button()
    animation_task.cancel() # type: ignore
    uasyncio.run(Sneko().run_game())


async def sleepy_wait_animation():
    while True:
        device.graphics.fill_rect((0,50), (128, 64), colors.BLACK)
        await uasyncio.sleep(2)
        for i in range(4):
            device.graphics.write_text((60 + 10 * i, 60 + 10 * i), "zzz")
            await device.audio.play_tone(100, 1, 0.3)
            await uasyncio.sleep(0.4)

