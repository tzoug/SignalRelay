import asyncio
from telegram import Bot
import sys

async def main(token):
    bot = Bot(token)
    updates = await bot.get_updates()

    if updates:
        chat_id = updates[-1].message.chat_id
        print("Chat ID:", chat_id)
    else:
        print("No messages found")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python telegram_chat_id.py telegram_token")
        sys.exit(1)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sys.argv[1]))