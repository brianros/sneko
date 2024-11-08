import uasyncio
import device
import peripherals.graphics.colors as colors
from peripherals.audio.music import startup_tune
from apps.sneko.sneko import Sneko
from apps.frogger.frogger import Frogger


apps = [Sneko, Frogger]

async def run_menu():

    selected_app = 0

    def draw_app_list():
        y_base = 48
        device.display.fill_rect((0, y_base), (128, 128 - y_base), colors.BLACK)

        for i, app in enumerate(apps):
            y = y_base + i * 8
            device.display.write_text((22, y), app.__name__)
        
        nonlocal selected_app
        circle_pos = (18, y_base + selected_app * 8 + 4)
        circle_radius = 2
        device.display.fill_circle(circle_pos, circle_radius, colors.WHITE)

    def move_selection(new_dir):
        nonlocal selected_app
        selected_app = (selected_app + new_dir) % len(apps)
        draw_app_list()
    
    async def selection_menu():
        await device.audio.play_score(startup_tune, 0.01)
        device.display.write_text((16, 24), "hey there pretty")
        device.display.write_text((10, 32), "choose your poison")
        draw_app_list()

        old_dir = 0
        while True:
            await uasyncio.sleep(0.1)
            x, y, b = device.joystick.read()
            if b:
                break
            new_dir = -1 if (y > 0.5) else 1 if (y < -0.5) else 0
            if old_dir != new_dir:
                move_selection(new_dir)
                old_dir = new_dir
    
    while True:
        device.display.fill_rect((0,50), (128, 64), colors.BLACK)
        await uasyncio.sleep(2)
        for i in range(4):
            device.display.write_text((60 + 10 * i, 60 + 10 * i), "zzz")
            await device.audio.play_tone(100, 1, 0.3)
            await uasyncio.sleep(0.4)

