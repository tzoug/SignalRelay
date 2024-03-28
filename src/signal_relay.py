from pydbus import SystemBus
from gi.repository import GLib
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from constants import Constants
from telegram_bot_handler import send_telegram_message
import asyncio
import base64
import sys
import os

def load_config(env_file_path):
   load_dotenv(env_file_path)
   return {
      'phone_number': os.getenv(Constants.PHONE_NUMBER),
      'telegram_token': os.getenv(Constants.TELEGRAM_TOKEN),
      'telegram_chat_id': os.getenv(Constants.TELEGRAM_CHAT_ID),
      'signal_group_id': os.getenv(Constants.SIGNAL_GROUP_ID),
   }

def display_message(timestamp, source, gid, message, attachments):
   print("Message received from Signal:")
   print("Timestamp:", convert_timestamp_to_est(timestamp))
   print("Message:", message)
   print("Source:", source)
   print("Group ID:", gid)
   print("Attachments:", attachments)

def decode_group_id(groupId):
   try:
      if not groupId:
         return []

      b = bytes(groupId)
      gid = base64.b64encode(b).decode()
      return gid

   except Exception as e:
      print(f"Error in decoding group ID: {e}")
      return []
   
def convert_timestamp_to_est(timestamp):
    if timestamp:
        utc_time = datetime.fromtimestamp(timestamp / 1000, timezone.utc)
        est_time = utc_time.astimezone(timezone(timedelta(hours = -4)))
        return est_time.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return timestamp   

async def process_received_message(timestamp, source, groupID, message, attachments, config):
   gid = decode_group_id(groupID)
   display_message(timestamp, source, gid, message, attachments)

   if (gid == config['signal_group_id'] and message):
      await send_telegram_message(config['telegram_token'], config['telegram_chat_id'], message)

   print()

def signal_message_received(timestamp, source, groupID, message, attachments, config):
   asyncio.run(process_received_message(timestamp, source, groupID, message, attachments, config))

def main(env_file_path):
   config = load_config(env_file_path)

   bus = SystemBus()
   loop = GLib.MainLoop()
   
   phone_number = config['phone_number']
   phone_number = phone_number[1:] if phone_number.startswith('+') else phone_number
   
   signal = bus.get('org.asamk.Signal', f'/org/asamk/Signal/_{phone_number}')
   signal.onMessageReceived = lambda timestamp, source, groupID, message, attachments: signal_message_received(timestamp, source, groupID, message, attachments, config)
   
   print('Started SignalRelay...')
   print()
   
   try:
      loop.run()
   except KeyboardInterrupt:
      print("Stopping SignalRelay...")
      loop.quit()

if __name__ == "__main__":
   if len(sys.argv) != 2:
      print("Usage: python signal_relay.py path_to_env_file")
      sys.exit(1)
   main(sys.argv[1])
