from typing import Any
import discord
from discord.flags import Intents
from . import listener
from .config import Config

class ScreenshotterBotClient(discord.Client):
    def __init__(self, config: Config) -> None:
        self.config = config
        # Minimal intents are needed currently since the bot doesn't respond to Discord events.
        # guild: Needed for get_channel()
        super().__init__(intents=Intents(guilds=True))

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        channel = self.get_channel(self.config.channel)
        if (channel is None):
            raise ValueError(f'Unable to retrieve channel with ID "{self.config.channel}"')
        listener.ScreenshotHotkeyListener(self, channel, self.config).start()

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')