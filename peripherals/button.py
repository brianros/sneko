from . import Peripheral
from machine import Pin
import uasyncio

class Button(Peripheral):
	def __init__(self, pin):
		super().__init__()
		self._pin = Pin(pin, Pin.IN, Pin.PULL_UP)
	
	def read(self):
		return not self._pin.value()

	def debug(self):
		print(f"Button: {self.read()}")

	async def wait_for_button(self):
		while True:
			if (self.read()):
				break
			await uasyncio.sleep(0.05)

