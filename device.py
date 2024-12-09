from peripherals import *
import config


def reset():
    reset_all()

joystick = Joystick(**config.joystick)
audio = Buzzer(**config.buzzer)
display = ST7735_Controller(**config.display)
wheel = RotaryEncoder(**config.rotary_encoder)

