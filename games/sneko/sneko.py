from device.graphics.ST7735 import TFT
from games.sneko.map import Map
from games.sneko.snake import Snake
import time
import math
import random
import uasyncio


time_decrease = 5
min_time_step = 50
starting_segments = [(6,7), (7,7), (8,7), (9,7)]


class Sneko:
    def __init__(self, device):
        self.device = device
        self.map = Map(device.graphics)
        self.snake = Snake(device, self, starting_segments)
        self.score = 0
        self.time_step = 150
    
    async def setup(self):
        await uasyncio.sleep(self.time_step)
        for i in range(4):
            self.device.buzzer.chirp()
            self.map.write(starting_segments[i], i)
            await uasyncio.sleep(self.time_step)
        for i in range(8):
            self.device.buzzer.chorp()
            self.map.write((4 + i,8), 4)
            await uasyncio.sleep(0.1)
        await uasyncio.sleep(self.time_step)
        self.device.buzzer.chorp()
        self.map.dropEggplant()
        await uasyncio.sleep(self.time_step)

    async def death(self, nextHead):
        await self.snake.die(nextHead)
        await uasyncio.sleep(1)
        deathSound = uasyncio.create_task(self.device.buzzer.play_death_tune())
        self.device.drawer.draw_bmp('/sneko/res/deathscreen.bmp', (0, 0))
        await deathSound
        await uasyncio.sleep(1)

    async def runGame(self):
        await self.setup()
        while True:
            old_head, next_head = self.snake.step()
            if old_head != next_head:
                map_next_head = self.map.read(next_head)
                if map_next_head == 6:
                    self.snake.retract_tail()
                    self.snake.advance_head(next_head)
                elif map_next_head == 5:
                    self.snake.advance_head(next_head)
                    self.device.buzzer.play_eat_sound()
                    self.map.dropEggplant()
                    self.time_step = max(self.time_step - time_decrease, min_time_step)
                    self.score += 1
                else:
                    if next_head == self.snake[0]:
                        self.snake.retract_tail()
                        self.snake.advance_head(next_head)
                    else:
                        await self.death(next_head)
                        break

