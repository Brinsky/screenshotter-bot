# screenshotter-bot
A simple application that captures screenshots when a hotkey is pressed and uploads them to a Discord channel.

## Setup

Building the application requires a [Poetry](https://python-poetry.org/) installation.

From within the `screenshotter-bot` directory, run the following commands:

### To install

```
poetry install
```

### To configure

Copy `data/config-sample.json` to `data/config.json` and populate the relevant fields (bot token, channel ID, etc.) with the appropriate values. The meanings of each field are as follows:

- `token`: The secret token for your configured Discord bot, as a string
- `channel`: The ID of the channel in which screenshots should be posted, as an integer
- `hotkey`: The key combination that should trigger screenshot capture and upload, as a string. See [this](https://github.com/moses-palmer/pynput/blob/078491edf7025033c22a364ee76fb9e79db65fcc/lib/pynput/keyboard/__init__.py#L120-L125) documentation.
- `monitor`: The index of the monitor from which screenshots should be taken, starting from 0, as an integer
- `screenshot_width_percent`: The percentage of the monitor width to capture in the screenshot, centered at the midpoint of the monitor, as a float. Must be greater than 0 and less than or equal to 1.
- `screenshot_height_percent`: The percentage of the monitor height to capture in the screenshot, centered at the midpoint of the monitor, as a float. Must be greater than 0 and less than or equal to 1.

### To run

```
poetry run python bot.py
```