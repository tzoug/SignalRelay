# Telegram Setup

## Create A Telegram Bot

You can easily create a Telegram bot by following the [Obtain Your Bot Token](https://core.telegram.org/bots/tutorial#obtain-your-bot-token) section of the Telegram tutorial

## Obtaining the Chat ID

Once the bot is created and the stored the token is stored in a safe space, you need to add the bot to a group chat or a direct message

Now, we need to get the chat ID where the bot was added. To do this, you need to start by sending a message in the Telegram chat where the bot was added.

You can obtain the chat ID by [running the python script](#running-the-python-script) or [via your brower](#telegram-updates-url).

### Running The Python Script

```bash
# Install dependencies
pip install python-telegram-bot

# Run telegram_chat_id.py
python3 destination/telegram_chat_id.py YOUR_BOT_TOKEN

# Example output:
# Chat ID: 12345678

# Note: The chat IDs of group chats start with "-" and direct messages don't
```

### Telegram Updates URL

You can visit `https://api.telegram.org/bot<YourBOTToken>/getUpdates` and grab the `id` of the correct chat.