import device
import uasyncio


class App:
    def __init__(self):
        if type(self) is App:
            raise TypeError("App cannot be instantiated directly")
    
    async def run(self):
        print(f"Running app {self}")
        pass

    def close(self):
        print(f"Terminating app {self}")
        pass

