from .config import Config
from PIL import Image
from pynput import keyboard
from typing import Any, Callable
import asyncio
import discord
import dxcam
import threading
import time

class ListenerWithOnStart(keyboard.GlobalHotKeys):
    def __init__(self, hotkeys: dict[str, Callable[[], None]], on_start: Callable[[], None], *args: Any, **kwargs: Any) -> None:
        self.on_start = on_start
        super().__init__(hotkeys, *args, **kwargs)
    
    def run(self) -> None:
        print(f'Triggering Listener on_start() from "{threading.current_thread().name}"')
        self.on_start()
        super().run()

async def send_screenshot(channel: discord.TextChannel, filepath: str):
    print(f'Opening screenshot from "{threading.current_thread().name}"')
    await channel.send(file=discord.File(filepath))

def get_region(monitor_region: tuple[int, int, int, int], percentages: tuple[int, int]) -> tuple[int, int, int, int]:
        # Region format: (left, top, right, bottom)

        # Probably overkill, but no guarantee that left and top are always 0
        mon_width =  monitor_region[2] - monitor_region[0]
        mon_height = monitor_region[3] - monitor_region[1]
        mon_center_x = int((monitor_region[0] + monitor_region[2]) / 2)
        mon_center_y = int((monitor_region[1] + monitor_region[3]) / 2)

        width_percent = percentages[0]
        height_percent = percentages[1]

        image_width = int(mon_width * width_percent)
        image_height = int(mon_height * height_percent)

        left = mon_center_x - int(image_width / 2)
        top = mon_center_y - int(image_height / 2)

        return (left, top, left + image_width, top + image_height)

def grab_deflake(camera: dxcam.DXCamera, region: tuple[int, int, int, int]) -> Image:
    # DXCamera.grab() will return None if there isn't a "new" frame available
    frame = camera.grab(region)
    if frame is None:
        print(f'First grab() failed - waiting and grabbing again')
        # Unfortunate hack - wait >1/60th of a second and try again :/
        time.sleep(0.02)
        frame = camera.grab(region)
    
    if frame is None:
        print(f'Second grab() failed')
        return None
    return Image.fromarray(frame)

class ScreenshotHotkeyListener:
    def __init__(self, client: discord.Client, channel: discord.TextChannel, config: Config):
        self.client = client
        self.channel = channel
        self.hotkey = config.hotkey
        self.monitor = config.monitor
        self.region_percentages = (config.screenshot_width_percent, config.screenshot_height_percent)
        self.camera = None
        self.listener = None

    def on_start(self):
        print(f'Initializing DXCamera on "{threading.current_thread().name}"')
        self.camera = dxcam.create(output_idx=self.monitor)

    def on_activate(self):
        filepath = f'screenshots/screenshot_{time.time_ns()}.png'
        print(f'Hotkey activated! Saving "{filepath}" from "{threading.current_thread().name}"')

        region = get_region(self.camera.region, self.region_percentages)
        print(f'Calculated screenshot region of {region}')

        image = grab_deflake(self.camera, region)
        if image is not None:
            image.save(filepath, 'PNG')
            # For some reeason this runs the coroutine a lot sooner than loop.create_task
            asyncio.run_coroutine_threadsafe(send_screenshot(self.channel, filepath), self.client.loop)

    def start(self):
        print(f'Starting listener from "{threading.current_thread().name}"')
        self.listener = ListenerWithOnStart({self.hotkey: self.on_activate}, self.on_start)
        self.listener.start()
    
    def stop(self):
        self.listener.stop()