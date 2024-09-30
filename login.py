


from telethon import TelegramClient, events
from telethon.types import User
import asyncio
API_ID = 10247139 
API_HASH = "96b46175824223a33737657ab943fd6a"
BOT_TOKEN ="7293653178:AAGcJSttQbNUK0ORBmf6G9yy7LBLsxuU_k8" 

# SESSION, API_ID, API_HASH, and BOT_TOKEN should be previously defined
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

phone = None
login_token = None
code = None
password = None

# Start the bot
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Welcome! Please enter your phone number to log in.')
    global phone
    phone = None  # Resetting phone for a fresh login process

@bot.on(events.NewMessage)
async def handle_input(event):
    global phone, login_token, code, password

    if not phone:
        # Step 1: Get the phone number
        phone = event.raw_text
        try:
            login_token = await bot.send_code_request(phone)
            await event.respond('A login code has been sent to your phone. Please enter the code.')
        except Exception as e:
            await event.respond(f"Error sending code: {str(e)}")
            phone = None  # Reset if error
    elif not code:
        # Step 2: Get the code
        code = event.raw_text
        try:
            user_or_token = await bot.sign_in(phone, code)
            if isinstance(user_or_token, User):
                await event.respond("Logged in successfully!")
            else:
                password_token = user_or_token
                await event.respond("Please enter your password:")
        except Exception as e:
            await event.respond(f"Error logging in: {str(e)}")
            code = None  # Reset if error
    elif password is None:
        # Step 3: Get the password (if necessary)
        password = event.raw_text
        try:
            user = await bot.sign_in(password=password)
            await event.respond("Logged in successfully!")
        except Exception as e:
            await event.respond(f"Error with password: {str(e)}")
            password = None  # Reset if error

async def main():
    # Starts the bot event loop
    await bot.run_until_disconnected()

# Start the bot event loop
asyncio.run(main())

