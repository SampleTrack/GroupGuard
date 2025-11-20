import asyncio
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
from web import start_server  # Import the server function

# Initialize the Bot Client
Bot = Client(
    "GroupGuard",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

async def main():
    print("-------------------")
    print("   System Check... ")
    print("-------------------")
    
    # 1. Start the Bot
    await Bot.start()
    print("✅ Bot Started")

    # 2. Start the Fake Web Server (To keep Render happy)
    await start_server()
    print("✅ Web Server Started on Port 8080")

    # 3. Keep the bot running indefinitely
    await idle()
    
    # 4. Stop gracefully if the script is killed
    await Bot.stop()

if __name__ == "__main__":
    # Use asyncio to run the main function
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
