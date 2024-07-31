from device.graphics.ST7735 import TFT
from device.graphics.graphics import Graphics
from device.buzzer import Buzzer
from device.joystick import Joystick


peripherals = []

class Peripheral:
    def __init__(self):
        if type(self) is Peripheral:
            raise TypeError("Peripheral cannot be instantiated directly")

        peripherals.append(self)
    
    def reset(self):
        pass


class Device:
    def __init__(self):
        self.joystick = Joystick(pin_x=26, pin_y=27, pin_button=0, deadzone=2000)
        self.buzzer = Buzzer(pin_number=1)
        self.graphics = Graphics()
    
    def reset(self):
        pass

