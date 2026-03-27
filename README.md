# Telegram Group Broadcaster

A Python script to manage a list of Telegram groups and send broadcast messages using the Telethon library.

## Requirements

* Python 3.7 or higher
* Telethon library
* Telegram API ID and API Hash

## Installation

1. Clone or download this repository.
2. Install the required dependency using pip:

pip install telethon

## Setup

1. Obtain your API ID and API Hash from https://my.telegram.org.
2. Open `sender.py` in a text editor.
3. Replace the `API_ID` and `API_HASH` placeholders with your actual credentials.

## Usage

1. Run the script:
   python sender.py

2. On the first run, enter your phone number and the OTP code sent by Telegram.
3. Use the menu options to add up to 7 groups.
4. Select the broadcast option to send a message.

## Features

* Management menu: Add, list, delete, or clear groups within the script.
* Input validation: Prevents empty messages or duplicate entries.
* Security: Saves a session file so you do not need to log in repeatedly.
* Safety: Includes a 3-second delay between messages to respect Telegram rate limits.

## Important Note

Using user accounts for automated broadcasting carries a risk of account restriction. Ensure you are only sending messages to groups that permit your content.
