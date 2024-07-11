from machine import Pin, PWM # type: ignore
import math
import uasyncio # type: ignore


def midiNumber2Frec(m):
    return math.floor(440 * 2 ** ((m - 69)/12))

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
        self.pwm.duty_u16(math.floor(volume * 32768))
        await uasyncio.sleep(duration)
        self.pwm.duty_u16(0)

    async def play_score(self, score, silenceLength, volume = None):
        for note in score:
            await self.play_tone(*note, volume)
            await uasyncio.sleep(silenceLength)

    def play_new_direction_sound(self):
        uasyncio.create_task(self.play_tone(frequency = E3, duration = 0.02, volume = 0.7))

    def play_eat_sound(self):
        score = [(A2, 0.2), (A3, 0.2), (A4, 0.2)]
        silence = 0.001
        volume = 0.7
        uasyncio.create_task(self.play_score(score, silence, volume))

    async def play_blood_sound(self, duration):
        baseNote = 45 # A3
        for m in range(baseNote, baseNote + 12):
            await self.play_tone(midiNumber2Frec(m), duration/13)

    async def play_highscores_tune(self):
        await self.play_score(we_are_number_one, 0.01)

    async def play_death_tune(self):
        await self.play_score(death_tune, 0.05)

    def chirp(self):
        uasyncio.create_task(self.play_tone(A5, 0.1))

    def chorp(self):
        uasyncio.create_task(self.play_tone(A1, 0.07))
    
    def silence(self):
        self.pwm.duty_u16(0)


# Note durations
fn = 0.4;
hn = fn/2;
qn = fn/4;

# Note frecuencies
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
F5 = 698;
C6 = 1047;
B5 = 988;
Gs5 = 831;
Cs6 = 1109;
Ds6 = 1245;

death_tune = [
    (A3, 0.625),
    (A3, 0.500),
    (A3, 0.175),
    (A3, 0.625),
    (C3, 0.500),
    (B3, 0.125),
    (B3, 0.500),
    (A3, 0.125),
    (A3, 0.500),
    (C3, 0.125),
    (A3, 0.625)
]

we_are_number_one = [
    (F5, fn + hn),
    (C6, hn),
    (B5, qn),
    (C6, qn),
    (B5, qn),
    (C6, qn),
    (B5, hn),
    (C6, hn),
    (Gs5, fn),
    (F5, fn + hn),
    (F5, hn),
    (Gs5, hn),
    (C6, hn),
    (Cs6, fn),
    (Gs5, fn),
    (Cs6, fn),
    (Ds6, fn),
    (C6, hn),
    (Cs6, hn),
    (C6, hn),
    (Cs6, hn),
    (C6, fn)
]

