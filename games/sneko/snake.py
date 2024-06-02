from device.graphics.ST7735 import TFT
import uasyncio
import random


class Snake:
    def __init__(self, device, sneko, starting_segments):
        self.device = device
        self.sneko = sneko

        self.segments = starting_segments
        self.nextLetter = 0

        self.snakeDir = 0
        self.lastSnakeDir = 4
        
        self.joystickUpdater = uasyncio.create_task(self.updateJoystickCoroutine())
    
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

    def step(self):
        old_head = self.segments[-1]
        
        (x, y) = old_head
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
        next_head = (x,y)
    
        self.lastSnakeDir = self.snakeDir
        return (old_head, next_head)

    def retract_tail(self):
        oldTail = self.segments.pop(0)
        self.sneko.map.write(oldTail, 6)

    def advance_head(self, next_head):
        self.segments.append(next_head)
        self.map.write(next_head, self.nextLetter)
        self.nextLetter = (self.nextLetter + 1) % 4

    async def die(self, nextHead):
        self.joystickUpdater.cancel()
        
        self.retract_tail()
        self.sneko.map.write(nextHead, 7)
        await uasyncio.sleep(0.3)

        bloodSound = uasyncio.create_task(self.device.buzzer.play_blood_sound(0.4))
        (x, y) = nextHead
        for i in range(8):
            radius = i//2 + random.randint(3, 7)
            posX = 8 * x + 3.5 + random.randint(-5 - i, 5 + i)
            posY = 8 * y + 3.5 + random.randint(-5 - i, 5 + i)
            self.device.graphics.fill_circle((posX, posY), radius, TFT.RED)
            await uasyncio.sleep(0.03)
        await bloodSound

