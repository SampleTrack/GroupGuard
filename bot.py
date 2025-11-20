from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

# Initialize the Bot Client
Bot = Client(
    "GroupGuard",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins") # This loads files from the 'plugins' folder
)

if __name__ == "__main__":
    print("---------------------------------")
    print("   GroupGuard Bot is Starting... ")
    print("---------------------------------")
    
    try:
        Bot.run()
    except Exception as e:
        print(f"Error occurred: {e}")
