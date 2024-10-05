import asyncio
import requests
from telethon import TelegramClient
API_ID= 10247139 
API_HASH = "96b46175824223a33737657ab943fd6a"
BOT_TOKEN= "7293653178:AAGcJSttQbNUK0ORBmf6G9yy7LBLsxuU_k8" 
  # Replace with your Bot Token

# app = Client("session_bot", api_id=API_ID,api_hash=API_HASH, bot_token=BOT_TOKEN)



# Replace these with your own values

BOT_TOKEN = '"5222572158:AAGwMiAMGgj9BmMQdcxn58Cq19stEnoVarI"'
CHANNEL_ID =  -1002314161300

# Initialize the Telegram client
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

async def fetch_tom_price():
    url = "https://api.geckoterminal.com/api/v2/networks/solana/tokens/tomDEqSDN1xdrcodffuwRDoGa8eMp7dZmS5fHGoUnvo/pools?page=1"
    previous_price = None  # Variable to store the previous price

    while True:
        response = requests.get(url)
        data = response.json()
        
        # Extract the current price of TOM
        current_price = float(data['data'][0]['attributes']['token_price_usd'])
        
        # Format the message with 8 decimal places
        message = f"The current price of $TOM is ${current_price:.8f}"
        
        # Calculate percentage difference if previous price exists
        if previous_price is not None:
            difference_percentage = ((current_price - previous_price) / previous_price) * 100
            message += f"\nPrice Change: {'+' if difference_percentage >= 0 else '-'}{difference_percentage:.8f}%"
        
        # Update the previous price to the current price for the next iteration
        previous_price = current_price
        
        # Send the message to the specified channel
        await client.send_message(CHANNEL_ID, message)
        
        # Wait for 1 minute before fetching again
        await asyncio.sleep(60)

async def main():
    await fetch_tom_price()

# Run the bot
with client:
    client.loop.run_until_complete(main())
