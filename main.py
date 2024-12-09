import device
import uasyncio
import apps

async def main():
    await apps.loader()

try:
    main_loop = main()
    uasyncio.run(main_loop)
except KeyboardInterrupt:
    main_loop.close()
finally:
    device.reset_peripherals()

