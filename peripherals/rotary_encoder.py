from . import Peripheral
from machine import Pin


# This rotary encoder ignores the usual switch button
# If present, it should be treated as a regular button on an unrelated pin
# The traditionally called CLK and DT pins will be called X and Y.

# We have the four points in the plane:
# (calling them Quadrants is a manner of speaking)
# Quadrant | (X, Y)
#        0 | (0, 0)
#        1 | (1, 0)
#        2 | (1, 1)
#        3 | (0, 1)
# Quadrant changes are counted
# A click is made of 4 counters
# A turn is made of clicks_per_turn clicks, if set
# Clicks are discretized, while turns are though as a continuum

class RotaryEncoder(Peripheral):
    def __init__(self, pin_x, pin_y, clicks_per_turn):
        self._pin_x = Pin(pin_x, Pin.IN, Pin.PULL_UP)
        self._pin_y = Pin(pin_y, Pin.IN, Pin.PULL_UP)
        self._clicks_per_turn = clicks_per_turn

        # Initial state
        self._quadrant = self._get_quadrant()
        self._counter = 0
        self._unresolved_updates = 0
        
        self._pin_x.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._update)
        self._pin_y.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._update)

    def _get_quadrant(self) -> int:
        x = self._pin_x.value()
        y = self._pin_y.value()
        return 2 * x + x ^ y # X is the second digit, and the first is (X xor Y)

    def get_counter(self) -> int:
        return self._counter

    def get_clicks(self) -> int:
        return self._counter // 4

    def get_turns(self) -> float:
        return self._counter / (4 * self._clicks_per_turn)

    def _update(self, _):
        new_quadrant = self._get_quadrant()
        diff = (new_quadrant - self._quadrant) % 4
        self._quadrant = new_quadrant

        if diff == 0:
            return
        elif diff == 1:
            self._counter += 1
        elif diff == 3:
            self._counter -= 1
        else:
            self._unresolved_updates += 1
    
    def debug(self):
        super().debug()
        print(f"quadrant: {self._get_quadrant()}, X: {self._pin_x.value()}, Y: {self._pin_y.value()}"
            + f", counter: {self.get_counter()}, clicks: {self.get_clicks()}, unresolved: {self._unresolved_updates}"
            + (f", turns: {self.get_turns()}" if self._clicks_per_turn is not None else "")
        )

    def reset(self):
        super().reset()
        self._pin_x.irq(None)
        self._pin_y.irq(None)

