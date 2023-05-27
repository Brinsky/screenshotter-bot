from dataclasses import dataclass
import json

@dataclass
class Config:
    token: str
    channel: int
    hotkey: str

def load_config(filepath: str):
    config_json = json.load(open(filepath))
    return Config(
        token=config_json['token'],
        channel=config_json['channel'],
        hotkey=config_json['hotkey'])