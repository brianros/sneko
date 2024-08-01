import device
import uasyncio
import random
from apps.app import App


class Frogger(App):
    async def jump(self):
        device.graphics.clear_screen()
        uasyncio.create_task(device.audio.play_tone(200, 0.3))
        pos = (random.randint(8, 80), random.randint(8, 100))
        device.graphics.write_text(pos, "Parkour!")
        await uasyncio.sleep(1)

    async def run(self):
        await super().run()
        await self.jump()
        await self.jump()
        await self.jump()
        await self.jump()

