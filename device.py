from peripherals.peripheral import reset_all
from peripherals.graphics.ST7735_controller import ST7735_Controller
from peripherals.audio.buzzer import Buzzer
from peripherals.joystick import Joystick


def reset():
    print("Resetting device")
    reset_all()

joystick = Joystick(26, 27, 0)
audio = Buzzer(1)
graphics = ST7735_Controller(14, 15, 16, 17, 18)

