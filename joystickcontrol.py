from machine import Pin, ADC
import utime

class Joystick:
    def __init__(self, pin_x, pin_y, pin_button, deadzone=2000):
        self.x_axis = ADC(Pin(pin_x))
        self.y_axis = ADC(Pin(pin_y))
        self.button = Pin(pin_button, Pin.IN, Pin.PULL_UP)
        self.deadzone = deadzone

    def read_x(self):
        x_value = self.x_axis.read_u16()
        if x_value < 32768 - self.deadzone:
            return -(x_value - (32768 - self.deadzone))/(32768 - self.deadzone)
        elif x_value > 32768 + self.deadzone:
            return -(x_value - (32768 + self.deadzone))/(32768 - self.deadzone)
        else:
            return 0

    def read_y(self):
        y_value = self.y_axis.read_u16()
        if y_value < 32768 - self.deadzone:
            return (y_value - (32768 - self.deadzone))/(32768 - self.deadzone)
        elif y_value > 32768 + self.deadzone:
            return (y_value - (32768 + self.deadzone))/(32768 - self.deadzone)
        else:
            return 0

    def read_button(self):
        return 0 if self.button.value() else 1

    def read_joystick(self):
        x_status = self.read_x()
        y_status = self.read_y()
        button_status = self.read_button()
        return x_status, y_status, button_status

# Example usage
# if __name__ == "__main__":
#     joystick = Joystick(pin_x=26, pin_y=27, pin_button=0, deadzone=2000)

#     while True:
#         x_status, y_status, button_status = joystick.read_joystick()
#         print(f"X: {x_status}, Y: {y_status}, Button: {button_status}")
#         utime.sleep(0.1)


