from device.graphics.ST7735 import TFT
from device.graphics.graphics import Graphics
from device.buzzer import Buzzer
from device.joystick import Joystick


class Device:
    def __init__(self):
        self.joystick = Joystick(pin_x=26, pin_y=27, pin_button=0, deadzone=2000)
        self.buzzer = Buzzer(pin_number=1)
        self.graphics = Graphics()

