import uasyncio
from games.sneko.sneko import Sneko


async def main():
    await Sneko(device).run_game()

try:
    print("Main loop initiated")
    main_loop = main()
    uasyncio.run(main_loop)
except KeyboardInterrupt:
    # Here go debug methods
    # Here go termination methods
    main_loop.close()
    print("Main loop terminated")
    device.reset()

