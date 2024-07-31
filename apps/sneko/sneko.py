import device
import peripherals.graphics.colors as colors
from apps.sneko.map import Map
from apps.sneko.snake import Snake
from apps.sneko.map import MapContent
from peripherals.audio.notes import *
from peripherals.audio.music import *
import uasyncio # type: ignore


initial_time_step = 0.150
time_decrease = 0.005
min_time_step = 0.050

starting_segments = [(6,7), (7,7), (8,7), (9,7)]


class Sneko:
    async def setup(self):
        self.map = Map()
        self.snake = Snake(self, starting_segments)
        self.score = 0
        self.time_step = initial_time_step

        await uasyncio.sleep(initial_time_step)
        for i in range(4):
            uasyncio.create_task(device.audio.play_tone(A5, 0.1))
            self.map.write(starting_segments[i], i)
            await uasyncio.sleep(initial_time_step)
        for i in range(8):
            uasyncio.create_task(device.audio.play_tone(A1, 0.07))
            self.map.write((4 + i,8), MapContent.WALL)
            await uasyncio.sleep(0.1)
        await uasyncio.sleep(initial_time_step)
        uasyncio.create_task(device.audio.play_tone(A5, 0.14))
        self.map.drop_eggplant()
        await uasyncio.sleep(initial_time_step)

    async def death(self, nextHead):
        await self.snake.die(nextHead)
        await uasyncio.sleep(1)
        deathSound = uasyncio.create_task(device.audio.play_score(death_tune, 0.05))
        await device.graphics.draw_bmp_coroutine('/apps/sneko/res/deathscreen.bmp', (0, 0))
        await deathSound # type: ignore

        await uasyncio.sleep(1)
        device.graphics.clear_screen()
        await uasyncio.sleep(0.5)
        
        device.graphics.write_text((40, 64), "Score: " + str(self.score), colors.WHITE)
        highscore_music = uasyncio.create_task(device.audio.play_score(we_are_number_one, 0.01))
        await device.joystick.wait_for_button()
        highscore_music.cancel() # type: ignore
        device.audio.silence()
        device.graphics.clear_screen()
        await uasyncio.sleep(0.5)

    async def run_game(self):
        while True:
            await self.setup()
            while True:
                await uasyncio.sleep(self.time_step)
                head = self.snake.step()
                if head is not None:
                    map_next_head = self.map.read(head)
                    if map_next_head == MapContent.EMPTY or head == self.snake.segments[0]:
                        self.snake.retract_tail()
                        self.snake.advance_head(head)
                    elif map_next_head == MapContent.EGGPLANT:
                        self.snake.advance_head(head)
                        eat_score = [(A2, 0.2), (A3, 0.2), (A4, 0.2)]
                        uasyncio.create_task(device.audio.play_score(eat_score, 0.01, 0.7))
                        self.map.drop_eggplant()
                        self.time_step = max(self.time_step - time_decrease, min_time_step)
                        self.score += 1
                    else:
                        await self.death(head)
                        break

