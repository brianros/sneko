from machine import ADC, Pin # type: ignore


class Joystick:
    def __init__(self, pin_x, pin_y, pin_button, deadzone=2000):
        self.axi = [ADC(Pin(pin_x)), ADC(Pin(pin_y))]
        self.button = Pin(pin_button, Pin.IN, Pin.PULL_UP)
        self.deadzone = deadzone

    def read_axis(self, index):
        value = self.axi[index].read_u16()
        if value < 32768 - self.deadzone:
            return -(value - (32768 - self.deadzone))/(32768 - self.deadzone)
        elif value > 32768 + self.deadzone:
            return -(value - (32768 + self.deadzone))/(32768 - self.deadzone)
        else:
            return 0

    def read_joystick(self):
        x_status = self.read_axis(0)
        y_status = self.read_axis(1)
        button_status = not self.button.value()
        return x_status, y_status, button_status

    def debug_joystick(self):
        print("Joystick data:")
        x, y, b = self.read_joystick()
        print(x)
        print(y)
        print(b)

