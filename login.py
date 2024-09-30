from pyrogram import Client, filters
from pyrogram.types import Message

API_ID= 10247139 
API_HASH = "96b46175824223a33737657ab943fd6a"
BOT_TOKEN= "7293653178:AAGcJSttQbNUK0ORBmf6G9yy7LBLsxuU_k8" 
  # Replace with your Bot Token

app = Client("session_bot", bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
def start_command(client: Client, message: Message):
    message.reply_text("Welcome! Please send your session string to log in.\nWe value user's privacy. Your data is safe.")

@app.on_message(filters.text)
def receive_session_string(client: Client, message: Message):
    session_string = message.text
    try:
        # Attempt to log in using the provided session string
        client = Client("session_name", session_string=session_string)
        client.start()  # Start the client
        message.reply_text("Successfully logged in!")
    except Exception as e:
        message.reply_text(f"Failed to log in: {str(e)}")

if __name__ == "__main__":
    app.run()
