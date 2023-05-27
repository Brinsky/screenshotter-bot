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

Copy `data/config-sample.json` to `data/config.json` and populate the relevant fields (bot token, channel ID, etc.) with the appropriate values.

### To run

```
poetry run python bot.py
```