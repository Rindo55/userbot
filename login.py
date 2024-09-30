



import logging
import telethon
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest

# Configure logging
logging.basicConfig(level=logging.INFO)

# Your API ID and hash from my.telegram.org
API_ID = 10247139 
API_HASH = "96b46175824223a33737657ab943fd6a"
BOT_TOKEN ="7293653178:AAGcJSttQbNUK0ORBmf6G9yy7LBLsxuU_k8" 

# Create the client and connect
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Welcome! Please register using /register command.')
    logging.info(f'Start command received from {event.sender_id}')

@client.on(events.NewMessage(pattern='/register'))
async def register(event):
    await event.respond('Please enter your phone number:')
    response = await client.wait_for_new_message(event.chat_id)
    phone_number = response.message.message

    await event.respond('Please enter the OTP you received:')
    otp_response = await client.wait_for_new_message(event.chat_id)
    otp_code = otp_response.message.message

    # Sign in process
    async with TelegramClient('userbot', API_ID, API_HASH) as user_client:
        try:
            await user_client.sign_in(phone_number, otp_code)
            await event.respond('Successfully logged in!')
            # Monitor drug trafficking related chats here...
            # Example: Join a specific channel or group
            await user_client(JoinChannelRequest('DrugTraffickingChannel'))
        except Exception as e:
            await event.respond(f'Error during login: {str(e)}')

client.start()
client.run_until_disconnected()
