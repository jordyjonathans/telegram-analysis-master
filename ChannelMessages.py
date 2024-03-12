import asyncio
import configparser
import sys
from datetime import datetime

from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError

# Reading Configs
config = configparser.ConfigParser()
config.read("config-sample.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']
from_input_channel = config['Telegram']['from_channel']
to_input_channel = config['Telegram']['to_channel']

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)
client.start()
max_current_id = 0
to_channel = None
from_channel = None

async def init():
    global to_channel,from_channel
    print("Start.")

    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    from_channel =  await client.get_entity(int(from_input_channel))
    print("From Channel :",from_channel)
    to_channel = await client.get_entity(int(to_input_channel))
    print("To Channel :",to_channel)

    user_input = input("Enter 'q' to quit: ")
    if user_input == 'q':
        sys.exit("You chose to quit the program.")
    print("\nListening Messages..")

loop = asyncio.get_event_loop()
loop.run_until_complete(init())

@client.on(events.NewMessage(from_channel))
async def listenMessages(event):
    print("time:",datetime.utcnow(),"| Author:",event.message.post_author," | message:",event.message.message,"| media:",event.message.media ,"| details: ",event.message)
    await client.send_message(entity=to_channel, message=event.message)

with client:
    client.run_until_disconnected()
