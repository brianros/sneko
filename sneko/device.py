from utils.ST7735 import TFT
from machine import SPI, Pin
from utils.drawer import BMPDrawer
from utils.buzzer import Buzzer
from utils.joystick import Joystick


class Device:
    def __init__(self):
        self.joystick = Joystick(pin_x=26, pin_y=27, pin_button=0, deadzone=2000)
        self.buzzer = Buzzer(pin_number=1, defaultVolume=0.5)
        self.spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11), miso=None)
        self.drawer = BMPDrawer(self.spi, dc=16, cs=17, rst=18)
        self.tft = TFT(self.spi, 16, 17, 18)
        self.tft.initr()
        self.tft.rgb(True)

