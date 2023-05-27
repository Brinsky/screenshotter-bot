from screenshotter_bot import load_config, ScreenshotterBotClient
from pathlib import Path

config = load_config('data/config.json')
Path('screenshots').mkdir(exist_ok=True)
client = ScreenshotterBotClient(config)
client.run(config.token)