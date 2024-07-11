from device.graphics.ST7735 import TFT
from games.sneko.map import Map
from games.sneko.snake import Snake
from games.sneko.map import MapContent
import uasyncio # type: ignore


initial_time_step = 0.150
time_decrease = 0.005
min_time_step = 0.050

starting_segments = [(6,7), (7,7), (8,7), (9,7)]


class Sneko:
    def __init__(self, device):
        self.device = device

    async def setup(self):
        self.map = Map(self.device.graphics)
        self.snake = Snake(self.device, self, starting_segments)
        self.score = 0
        self.time_step = initial_time_step

        await uasyncio.sleep(initial_time_step)
        for i in range(4):
            self.device.buzzer.chirp()
            self.map.write(starting_segments[i], i)
            await uasyncio.sleep(initial_time_step)
        for i in range(8):
            self.device.buzzer.chorp()
            self.map.write((4 + i,8), MapContent.WALL)
            await uasyncio.sleep(0.1)
        await uasyncio.sleep(initial_time_step)
        self.device.buzzer.chorp()
        self.map.drop_eggplant()
        await uasyncio.sleep(initial_time_step)

    async def death(self, nextHead):
        await self.snake.die(nextHead)
        await uasyncio.sleep(1)
        deathSound = uasyncio.create_task(self.device.buzzer.play_death_tune())
        await self.device.graphics.draw_bmp_coroutine('/games/sneko/res/deathscreen.bmp', (0, 0))
        await deathSound

        await uasyncio.sleep(1)
        self.device.graphics.clear_screen()
        await uasyncio.sleep(0.5)
        
        self.device.graphics.write_text((40, 64), "Score: " + str(self.score), TFT.WHITE)
        highscore_music = uasyncio.create_task(self.device.buzzer.play_highscores_tune())

        while True:
            await uasyncio.sleep(0.01)
            x, y, button = self.device.joystick.read_joystick()
            if (button):
                break
        
        highscore_music.cancel()
        self.device.graphics.clear_screen()
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
                        self.device.buzzer.play_eat_sound()
                        self.map.drop_eggplant()
                        self.time_step = max(self.time_step - time_decrease, min_time_step)
                        self.score += 1
                    else:
                        await self.death(head)
                        break

