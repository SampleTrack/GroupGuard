from pyrogram import Client, filters
from pyrogram.types import Message
from database.operations import add_group

# This filter runs when "New Members" join a chat
@Client.on_message(filters.new_chat_members)
async def on_new_chat_members(client: Client, message: Message):
    # Check if the "New Member" is actually ME (The Bot)
    bot_id = client.me.id
    
    for member in message.new_chat_members:
        if member.id == bot_id:
            # The bot was just added to this group!
            chat_id = message.chat.id
            chat_title = message.chat.title
            
            # Save to Database
            await add_group(chat_id, chat_title)
            
            await message.reply_text(
                "**Thanks for adding me!** 🛡\n\n"
                "I have saved this group's default settings.\n"
                "Make me **Admin** so I can protect the chat!"
            )
