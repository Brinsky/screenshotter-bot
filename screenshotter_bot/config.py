from dataclasses import dataclass
import json

@dataclass
class Config:
    token: str
    channel: int
    hotkey: str
    monitor: int
    screenshot_width_percent: float
    screenshot_height_percent: float

def load_config(filepath: str) -> Config:
    config_json = json.load(open(filepath))
    config = Config(
        token=config_json['token'],
        channel=config_json['channel'],
        hotkey=config_json['hotkey'],
        monitor=config_json['monitor'],
        screenshot_width_percent=config_json['screenshot_width_percent'],
        screenshot_height_percent=config_json['screenshot_height_percent'])
    if config.monitor < 1:
        raise ValueError('monitor must be a positive integer')
    if config.screenshot_width_percent <= 0 or config.screenshot_width_percent > 1:
        raise ValueError('screenshot_width_percent must be in the range (0, 1]')
    if config.screenshot_height_percent <= 0 or config.screenshot_height_percent > 1:
        raise ValueError('screenshot_height_percent must be in the range (0, 1]')
    return config