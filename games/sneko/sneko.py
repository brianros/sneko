from device.graphics.ST7735 import TFT
from games.sneko.map import Map
from games.sneko.snake import Snake
from games.sneko.map import MapContent
import uasyncio # type: ignore


time_decrease = 5
min_time_step = 50
starting_segments = [(6,7), (7,7), (8,7), (9,7)]


class Sneko:
    def __init__(self, device):
        self.device = device
        self.map = Map(device.graphics)
        self.snake = Snake(device, self, starting_segments)
        self.score = 0
        self.time_step = 0.150
    
    async def setup(self):
        await uasyncio.sleep(self.time_step)
        for i in range(4):
            self.device.buzzer.chirp()
            self.map.write(starting_segments[i], i)
            await uasyncio.sleep(self.time_step)
        for i in range(8):
            self.device.buzzer.chorp()
            self.map.write((4 + i,8), MapContent.WALL)
            await uasyncio.sleep(0.1)
        await uasyncio.sleep(self.time_step)
        self.device.buzzer.chorp()
        self.map.drop_eggplant()
        await uasyncio.sleep(self.time_step)

    async def death(self, nextHead):
        await self.snake.die(nextHead)
        await uasyncio.sleep(1)
        deathSound = uasyncio.create_task(self.device.buzzer.play_death_tune())
        self.device.drawer.draw_bmp('/games/sneko/res/deathscreen.bmp', (0, 0))
        await deathSound
        await uasyncio.sleep(1)

    async def run_game(self):
        await self.setup()
        while True:
            head = self.snake.step()
            if head is not None:
                map_next_head = self.map.read(head)
                if map_next_head == MapContent.EMPTY or head == self.snake[0]:
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

