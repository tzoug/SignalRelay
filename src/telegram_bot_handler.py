from telegram import Bot

async def send_telegram_message(token, chat_id, message):
    try:
        bot = Bot(token=token)
        await bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f'Error sending Telegram message: {e}')
        print(f'Message was: {message}')
        raise
    else:
        print("Forwarded to Telegram successfully!")