from peripherals import reset_all
from peripherals.graphics.ST7735_controller import ST7735_Controller
from peripherals.audio.buzzer import Buzzer
from peripherals.joystick import Joystick
from peripherals.rotary_encoder import RotaryEncoder
import config


def reset():
    reset_all()

joystick = Joystick(**config.joystick)
audio = Buzzer(**config.buzzer)
display = ST7735_Controller(**config.display)
wheel = RotaryEncoder(**config.rotary_encoder)

