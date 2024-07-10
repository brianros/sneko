from device.graphics.ST7735 import TFT
from games.sneko.map import MapContent
import uasyncio # type: ignore
import random


class Snake:
    def __init__(self, device, sneko, starting_segments):
        self.device = device
        self.sneko = sneko

        self.segments = starting_segments
        self.next_letter = 0

        self.last_snake_dir = 0
        self.next_snake_dir = 0
        
        self.joystick_updater = uasyncio.create_task(self.updateJoystickCoroutine())
    
    async def updateJoystickCoroutine(self):
        while True:
            await uasyncio.sleep(0.01)
            x, y, b = self.device.joystick.read_joystick()
            dir = self.next_snake_dir
            if abs(x) > abs(y):
                dir = 4 if x > 0 else 2
            if abs(y) > abs(x):
                dir = 1 if y > 0 else 3
            if (dir - self.last_snake_dir) % 4 != 2:
                self.next_snake_dir = dir
                if x !=0 or y !=0:
                    self.device.buzzer.play_new_direction_sound()

    def step(self):
        oldHead = self.segments[-1]
        
        (x, y) = oldHead
        if self.next_snake_dir == 1:
            y -= 1
        elif self.next_snake_dir == 2:
            x -= 1
        elif self.next_snake_dir == 3:
            y += 1
        elif self.next_snake_dir == 4:
            x += 1
        x = x % 16
        y = y % 16
        new_head = (x,y)
    
        self.last_snake_dir = self.next_snake_dir
        return new_head if oldHead != new_head else None

    def retract_tail(self):
        oldTail = self.segments.pop(0)
        self.sneko.map.write(oldTail, MapContent.EMPTY)

    def advance_head(self, next_head):
        self.segments.append(next_head)
        self.sneko.map.write(next_head, self.next_letter)
        self.next_letter = (self.next_letter + 1) % 4

    async def die(self, next_head):
        self.joystick_updater.cancel()
        
        self.retract_tail()
        self.sneko.map.write(next_head, MapContent.BLOOD)
        await uasyncio.sleep(0.3)

        blood_sound = uasyncio.create_task(self.device.buzzer.play_blood_sound(0.4))
        (x, y) = next_head
        for i in range(8):
            radius = i//2 + random.randint(3, 7)
            pos_x = 8 * x + 3.5 + random.randint(-5 - i, 5 + i)
            pos_y = 8 * y + 3.5 + random.randint(-5 - i, 5 + i)
            self.device.graphics.fill_circle((pos_x, pos_y), radius, TFT.RED)
            await uasyncio.sleep(0.03)
        await blood_sound

