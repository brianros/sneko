import uasyncio
import device
import apps

async def main():
    await apps.loader()

try:
    print("Main loop initiated")
    main_loop = main()
    uasyncio.run(main_loop)
except KeyboardInterrupt:
    # Here go debug methods
    # Here go pre-termination methods
    main_loop.close()
finally:
    # Here go termination methods
    print("Main loop terminated")
    device.reset()

