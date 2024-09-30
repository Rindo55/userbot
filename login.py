



from telethon.sessions import StringSession
from telethon.sync import TelegramClient, events
from telethon.tl.types import InputPeerUser

APP_ID= 10247139 
API_HASH = "96b46175824223a33737657ab943fd6a"
BOT_TOKEN= "7293653178:AAGcJSttQbNUK0ORBmf6G9yy7LBLsxuU_k8" 
# Set your bot's token
BOT_TOKEN = "YOUR_BOT_TOKEN"
bot = TelegramClient('bot', APP_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Store inputs from the user
user_data = {
    "app_id": None,
    "api_hash": None
}

async def handle_start(event):
    # Start the process by asking the user for their APP ID
    await event.respond("Welcome! Please send me your APP ID.")
    user_data['app_id'] = None  # Reset previous input, if any

@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await handle_start(event)

@bot.on(events.NewMessage())
async def handle_message(event):
    # Check if we have APP ID and API Hash
    if user_data['app_id'] is None:
        # This is where we capture APP ID
        user_data['app_id'] = int(event.message.text.strip())
        await event.respond("Now, send me your API HASH.")
    elif user_data['api_hash'] is None:
        # This is where we capture API HASH
        user_data['api_hash'] = event.message.text.strip()
        await event.respond("Thank you! Trying to generate the session string now...")

        # Now we use the collected APP ID and API HASH to authenticate
        async with TelegramClient(StringSession(), user_data['app_id'], user_data['api_hash']) as client:
            session_str = client.session.save()
            await event.respond(f"Your session string is: {session_str}")
            # Optionally send it to the user directly in Telegram
            await client.send_message('me', f"Here is your session string: {session_str}")

            # Reset after process
            user_data['app_id'] = None
            user_data['api_hash'] = None

# Start the bot
print("Bot is running...")
bot.run_until_disconnected()
