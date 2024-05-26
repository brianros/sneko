# buzzer.py
from machine import Pin, PWM
import utime

class Buzzer:
    def __init__(self, pin_number):
        self.pin = Pin(pin_number)
        self.pwm = PWM(self.pin)
        self.pwm.duty_u16(0)

    def play_tone(self, frequency, duration):
        self.pwm.freq(frequency)
        self.pwm.duty_u16(35000)  # 50% duty cycle for volume
        utime.sleep_ms(duration)
        self.pwm.duty_u16(0)  # turn off the buzzer

    def play_direction_sound(self):
        # Define frequency and duration for direction sound
        frequency = 1000  # Adjust frequency as needed
        duration = 2  # Adjust duration as needed
        self.play_tone(frequency, duration)

    def play_pick_sound(self):
        # Define frequency and duration for pick sound
        frequency = 1500  # Adjust frequency as needed
        duration = 5  # Adjust duration as needed
        self.play_tone(frequency, duration)

    def play_death_tune(self):
        notes = [(A2, 625), (A2, 500), (A2, 175), (A2, 625), (C3, 500), (B2, 125), (B2, 500), (A2, 125), (A2, 500), (C3, 125), (A2, 625)]
        for note in notes:
            self.play_tone(note[0], note[1])
            utime.sleep_ms(50)  # Delay between notes

# Define frequency values for notes
C3 = 131
D3 = 147
E3 = 165
F3 = 175
G3 = 196
A2 = 220
B2 = 247
G2 = 98


