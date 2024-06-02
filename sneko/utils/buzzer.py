# buzzer.py
from machine import Pin, PWM
import utime
import uasyncio


class Buzzer:
    def __init__(self, pin_number, defaultVolume = 1):
        self.pin = Pin(pin_number)
        self.pwm = PWM(self.pin)
        self.pwm.duty_u16(0)
        self.defaultVolume = defaultVolume

    async def play_tone(self, frequency, duration, volume = None):
        if volume is None:
            volume = self.defaultVolume
        self.pwm.freq(frequency)
        self.pwm.duty_u16(math.floor(volume * 65535))
        await uasyncio.sleep(duration)
        self.pwm.duty_u16(0)

    async def play_score(self, score, silenceLength, volume = None):
        for note in score:
            await self.play_tone(*note, volume)
            await uasyncio.sleep(silenceLength)

    def play_new_direction_sound(self):
        uasyncio.create_task(self.play_tone(frequency = E3, duration = 0.02, volume = 0.3))

    def play_eat_sound(self):
        score = [(A2, 0.2), (A3, 0.2), (A4, 0.2)]
        silence = 0.001
        volume = 0.3
        uasyncio.create_task(self.play_score(score, silence, volume))

    async def play_blood_sound(self, duration):
        score = [(A2, duration), (B2, duration), (C3, duration), (D3, duration), (E3, duration), (F3, duration), (G3, duration), (A3, duration)]
        await self.play_score(score, 0)

    async def play_death_tune(self):
        score = [(A3, 0.625), (A3, 0.500), (A3, 0.175), (A3, 0.625), (C3, 0.500), (B3, 0.125), (B3, 0.500), (A3, 0.125), (A3, 0.500), (C3, 0.125), (A3, 0.625)]
        await self.play_score(score, 0.05)

    def chirp(self):
        uasyncio.create_task(self.play_tone(A5, 0.1))

    def chorp(self):
        uasyncio.create_task(self.play_tone(A1, 0.07))


# Define frequency values for notes
A1 = 55
G2 = 98
A2 = 110
B2 = 123
C3 = 131
D3 = 147
E3 = 165
F3 = 175
G3 = 196
A3 = 220
B3 = 247
A4 = 440
A5 = 880

