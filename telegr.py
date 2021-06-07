#!/usr/bin/env python3
import argparse
import configparser
import json
import os
import sys
import urllib.request
import urllib.parse
from pathlib import Path

sys.stdin.reconfigure(encoding='utf-8')

telegram_cfg = configparser.ConfigParser()
cfg_path = os.path.join(Path.home(), ".telegr.cfg")

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", type=str, default=cfg_path, help="Location for the configuration file that stores chat ID and bot token")
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
args = parser.parse_args()

if not os.path.isfile(cfg_path):
	print("A new empty '.telegr.cfg' is being created your home directory:")
	print(cfg_path)
	print("This file is necessary as it stores the bot credentials and chat id.")
	print("Please add the necessary data to that file and run the 'telegr' command again.")

	telegram_cfg["DEFAULT"] = {
		"BOT_TOKEN": "",
		"CHAT_ID": ""
	}
	with open(cfg_path, 'w') as configfile:
		telegram_cfg.write(configfile)

	sys.exit()
else:
	if args.config:
		cfg_path = args.config
	if not os.path.isfile(cfg_path):
		print("The specified configuration file does not exist: {}".format(cfg_path))
		print("Exiting.")
		sys.exit()
	telegram_cfg.read(cfg_path)

# -v     verbose 
VERBOSE = args.verbose
# secret bot token
BOT_TOKEN = telegram_cfg["DEFAULT"]["BOT_TOKEN"]
# chat ID with designated chat partner
CHAT_ID = telegram_cfg["DEFAULT"]["CHAT_ID"]
# API endpoint
TELEGRAM_URL = "https://api.telegram.org/bot{token}/sendMessage".format(token=BOT_TOKEN)
# length per message
MAX_LENGTH = 4096
# amount of messages in a series if split
MAX_MSG_COUNT = 2
MAX_LENGTH_HARD_LIMIT = MAX_MSG_COUNT*MAX_LENGTH

if VERBOSE:
	print("Sending a Telegram message")
	print("Reading config from {}".format(cfg_path))

def send_msg(text):
	message = text
	data = {
		"chat_id": "134232630",
		"text": message,
		"disable_notification": True,
		"disable_web_page_preview": True
	}

	req_data = urllib.parse.urlencode(data).encode()
	req = urllib.request.Request(TELEGRAM_URL, data=req_data)
	try:
		with urllib.request.urlopen(req) as f:
			if VERBOSE:
				print("Message sent")
				print("Telegram API response:")
				print(f.read().decode('utf-8'))
	except urllib.error.HTTPError as e:
		if VERBOSE:
			print("Telegram API responded with an error:")
			print(e.read())
			print(text)
	except:
		if VERBOSE:
			print("An unknown error occured")
			print(text)

stdin_read = sys.stdin.read(MAX_LENGTH)
amount_read = 0
while stdin_read:
	amount_read = amount_read + MAX_LENGTH
	msg = stdin_read

	if amount_read < MAX_LENGTH_HARD_LIMIT:
		send_msg(msg)
		stdin_read = sys.stdin.read(MAX_LENGTH)
	else:
		if VERBOSE:
			print("Limit reached")
		warn_msg = "\n[...]\n(maximum length of {} reached for this message)".format(MAX_LENGTH_HARD_LIMIT)
		to_cut = max(0, len(warn_msg))
		msg = stdin_read[:-to_cut] + warn_msg
		send_msg(msg)
		break

if VERBOSE:
	print("Finished")
