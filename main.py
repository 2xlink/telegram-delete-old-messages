import configparser
import json
import asyncio
import datetime, time

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import (
    PeerChannel
)

# Delete messages until this point
dt_until_date = datetime.datetime.now() - datetime.timedelta(weeks=52)

config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash)

async def main(phone):
    await client.start()
    print("Client Created")
    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    me = await client.get_me()
    msg_iter = client.iter_messages(entity=None, offset_date=dt_until_date)

    async for msg in msg_iter:
        # Is True if message is sent by me
        if not msg.out:
            # print(f"[-] Message not from me. Discarding …")
            pass
        else:
            try:
                print(f"[+] Found: ", end="")
                print(f"{msg.message[0:300]}")
            except:
                print("Error (no text content)")
            try:
                await msg.delete()
                print(f"[+] Deleted message: {msg.id}")
            except:
                print(f"[!] Error deleting message: {msg.id}")

with client:
    client.loop.run_until_complete(main(phone))
