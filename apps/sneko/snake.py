import peripherals.graphics.colors as colors
from apps.sneko.map import MapContent
import device
from peripherals.audio.notes import midiNumber2Frec, E3
import uasyncio # type: ignore
import random


async def play_blood_sound(duration):
    baseNote = 45 # A3
    for m in range(baseNote, baseNote + 12):
        await device.audio.play_tone(midiNumber2Frec(m), duration/13)

class Snake:
    def __init__(self, sneko, starting_segments):
        self.sneko = sneko

        self.segments = starting_segments.copy()
        self.next_letter = 0

        self.last_snake_dir = 0
        self.next_snake_dir = 0
        
        self.joystick_updater = uasyncio.create_task(self.updateJoystickCoroutine())
    
    async def updateJoystickCoroutine(self):
        while True:
            await uasyncio.sleep(0.01)
            x, y, b = device.joystick.read()
            dir = self.next_snake_dir
            if abs(x) > abs(y):
                dir = 4 if x > 0 else 2
            if abs(y) > abs(x):
                dir = 1 if y > 0 else 3
            if (dir - self.last_snake_dir) % 4 != 2:
                if self.next_snake_dir != dir:
                    self.next_snake_dir = dir
                    uasyncio.create_task(device.audio.play_tone(frequency = E3, duration = 0.02, volume = 0.7))

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
        self.joystick_updater.cancel() # type: ignore
        
        self.retract_tail()
        self.sneko.map.write(next_head, MapContent.BLOOD)
        await uasyncio.sleep(0.3)

        blood_sound = uasyncio.create_task(play_blood_sound(0.4))
        (x, y) = next_head
        for i in range(8):
            radius = i//2 + random.randint(3, 7)
            pos_x = 8 * x + 3.5 + random.randint(-5 - i, 5 + i)
            pos_y = 8 * y + 3.5 + random.randint(-5 - i, 5 + i)
            device.graphics.fill_circle((pos_x, pos_y), radius, colors.RED)
            await uasyncio.sleep(0.03)
        await blood_sound # type: ignore




