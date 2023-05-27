from .config import Config
from mss import mss
from pynput import keyboard
from typing import Any, Callable
import asyncio
import discord
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

class ScreenshotHotkeyListener:
    def __init__(self, client: discord.Client, channel: discord.TextChannel, config: Config):
        self.client = client
        self.channel = channel
        self.hotkey = config.hotkey
        self.mss = None
        self.listener = None

    def on_start(self):
        # mss must be initialized from the same thread where it will be used
        print(f'Initializing mss on "{threading.current_thread().name}"')
        self.mss = mss()

    def on_activate(self):
        filepath = f'screenshots/screenshot_{time.time_ns()}.png'
        print(f'Hotkey activated! Saving "{filepath}" from "{threading.current_thread().name}"')
        self.mss.shot(output=filepath)
        # For some reeason this runs the coroutine a lot sooner than loop.create_task
        asyncio.run_coroutine_threadsafe(send_screenshot(self.channel, filepath), self.client.loop)

    def start(self):
        print(f'Starting listener from "{threading.current_thread().name}"')
        self.listener = ListenerWithOnStart({self.hotkey: self.on_activate}, self.on_start)
        self.listener.start()
    
    def stop(self):
        self.listener.stop()