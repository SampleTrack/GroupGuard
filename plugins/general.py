from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    # Get user info
    user = message.from_user.mention
    
    # Reply to the user
    await message.reply_text(
        f"Hello {user}! 👋\n\n"
        "I am **GroupGuard**. I am currently under development.\n"
        "Soon I will help you manage your groups!"
    )
