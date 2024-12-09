from peripherals import *
import config


joystick = Joystick(**config.joystick)
audio = Buzzer(**config.buzzer)
display = ST7735_Controller(**config.display)
wheel = RotaryEncoder(**config.rotary_encoder)

