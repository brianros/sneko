from utils.ST7735 import TFT
from res.sysfont import sysfont
from machine import SPI, Pin, ADC
from utils.drawer import BMPDrawer
from utils.joystick import Joystick
from map import Map
import time
import math
import random
import uasyncio



class Game:
    def __init__(self, device):
        self.device = device
        self.map = Map()

        self.score = 0

        self.snake = [(6,7), (7,7), (8,7), (9,7)]
        self.nextLetter = 0
        self.snakeDir = 0
        self.lastSnakeDir = 4

        self.timeStep = 150
        self.timeDecrease = 5

        self.joystickUpdater = uasyncio.create_task(self.updateJoystickCoroutine())
    
    async def waitStep(self):
        return uasyncio.sleep(self.timeStep)
    
    async def updateJoystickCoroutine(self):
        while True:
            await uasyncio.sleep(0.01)
            x, y, b = self.device.joystick.read_joystick()
            dir = self.snakeDir
            if abs(x) > abs(y):
                dir = 4 if x > 0 else 2
            if abs(y) > abs(x):
                dir = 1 if y > 0 else 3
            if (dir - self.lastSnakeDir) % 4 != 2:
                self.snakeDir = dir
                if x !=0 or y !=0:
                    self.device.buzzer.play_new_direction_sound()
    
    def calculateNextHead(self, head):
        (x, y) = head
        if self.snakeDir == 1:
            y += 1
        elif self.snakeDir == 2:
            x -= 1
        elif self.snakeDir == 3:
            y -= 1
        elif self.snakeDir == 4:
            x += 1
        x = x % 16
        y = y % 16
        return (x,y)

    def advanceHeadOnly(self, nextHead):
        self.snake.append(nextHead)
        self.map.write(nextHead, self.nextLetter)
        self.nextLetter = (self.nextLetter + 1) % 4

    async def death(self, nextHead):
        self.joystickUpdater.cancel()
        self.map.write(nextHead, 7)
        await uasyncio.sleep(0.3)
        bloodSound = uasyncio.create_task(self.device.buzzer.play_blood_sound(0.03))
        (x, y) = nextHead
        for i in range(8):
            radio = i//2 + random.randint(3, 7)
            posX = 8 * x + 3.5 + random.randint(-5 - i, 5 + i)
            posY = 8 * y + 3.5 + random.randint(-5 - i, 5 + i)
            self.device.tft.fillcircle((posX, posY), radio, TFT.RED)
            await uasyncio.sleep(0.03)
        await bloodSound
        await uasyncio.sleep(1)
        deathSound = uasyncio.create_task(self.device.buzzer.play_death_tune())
        self.device.drawer.draw_bmp('/sneko/res/deathscreen.bmp', (0, 0))
        await deathSound
        await uasyncio.sleep(1)

    def retractTail(self):
        oldTail = self.snake.pop(0)
        self.map.write(oldTail, 6)

    async def intro(self):
        self.map.clearAll()
        await self.waitStep()
        for i in range(4):
            self.device.buzzer.chirp()
            self.map.write((6 + i, 7), i)
            await self.waitStep()
        for i in range(8):
            self.device.buzzer.chorp()
            self.map.write((4 + i,8), 4)
            await uasyncio.sleep(0.1)
        await self.waitStep()
        self.device.buzzer.chorp()
        self.map.dropEggplant()
        await self.waitStep()

    async def runGame(self):
        await self.intro()
        while True:
            head = self.snake[-1]
            nextHead = self.calculateNextHead(head)
            self.lastSnakeDir = self.snakeDir
            if head != nextHead:
                mapNextHead = self.map.read(nextHead)
                if mapNextHead == 6:
                    self.retractTail()
                    self.advanceHeadOnly(nextHead)
                elif mapNextHead == 5:
                    self.advanceHeadOnly(nextHead)
                    self.device.buzzer.play_eat_sound()
                    self.map.dropEggplant()
                    self.timeStep -= self.timeDecrease
                    self.score += 1
                else:
                    if nextHead == self.snake[0]:
                        self.retractTail()
                        self.advanceHeadOnly(nextHead)
                    else:
                        self.retractTail()
                        await self.death(nextHead)
                        break

