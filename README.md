# telegr

Simple script to send text messages to a Telegram bot from the command line.

Requires Python 3.5+, tested on Ubuntu 20.04 and Windows 10.

Messages above 4096 length are split into multiple messages.

## Limitations

This script is very basic and does not support any formatting, like Markdown or HTML.

Message splitting is very rudamentary, does not take into account and sentence structures or newlines, etc.

It supports only one recipient/chat at each run, although you could specify multiple recipients (on successive executions) via config files (parameter `-c / --config`, see below).

## Installation

Copy [`telegr.cfg`](telegr.cfg) to `.telegr.cfg` in your user home directory and modify `BOT_TOKEN` and `CHAT_ID` to add your credentials. If you run this for cronjob notifications, remember to copy the config to other user directories as well (i.e. `/root`).

Copy [`telegr.py`](telegr.py) to your distro's bin directory and make it executable:

```
cp telegr.py /usr/local/bin/telegr
chmod +x /usr/local/bin/telegr
```

## Configuration

```
# token acquired from Telegram BotFather
BOT_TOKEN = "<bot token, read from config>"
# chat ID between designated user and bot, acquire via /getUpdates endpoint
CHAT_ID = "<chat id, read from config>"
# max. length for a message (4096 = Telegram API limit)
MAX_LENGTH = 4096
# max. amount of messages to send in series, if message was split
MAX_MSG_COUNT = 2
```

## Usage

Pipe anything as stdin into the script:

```
echo hello | telegr
```

Usage of `-v / --verbose`:

```
echo hello | telegr -v
```

Usage of `-c / --config` to specify a different config file location:

```
echo using another config file | telegr -c telegr2.cfg
```

## License

MIT
