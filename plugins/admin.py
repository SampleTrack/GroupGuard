from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, Message
from datetime import datetime, timedelta

# --- HELPER FUNCTIONS ---

async def get_target_user(message: Message):
    """
    Finds who the admin is trying to ban/mute.
    Target can be a Reply OR a Username/ID.
    """
    if message.reply_to_message:
        return message.reply_to_message.from_user
    elif len(message.command) > 1:
        # If they typed /ban @username
        try:
            user = await message._client.get_users(message.command[1])
            return user
        except:
            return None
    return None

def get_time_seconds(time_string):
    """
    Converts '10m', '2h', '1d' into seconds.
    """
    unit = time_string[-1].lower()
    if unit not in ['m', 'h', 'd']:
        return 0
    
    try:
        value = int(time_string[:-1])
    except ValueError:
        return 0

    if unit == 'm': return value * 60
    elif unit == 'h': return value * 3600
    elif unit == 'd': return value * 86400
    return 0

# --- COMMANDS ---

@Client.on_message(filters.command("ban") & filters.group)
async def ban_command(client: Client, message: Message):
    # 1. Check if the USER (Admin) has permission
    # (For a real production bot, we would check actual admin rights here)
    
    target = await get_target_user(message)
    if not target:
        await message.reply_text("❌ **Reply** to a user or mention them to ban.")
        return

    try:
        # Ban the user
        await client.ban_chat_member(message.chat.id, target.id)
        await message.reply_text(f"🚫 Banned **{target.mention}** from the group!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")


@Client.on_message(filters.command("unban") & filters.group)
async def unban_command(client: Client, message: Message):
    target = await get_target_user(message)
    if not target:
        await message.reply_text("❌ Give me a username or ID to unban.")
        return

    try:
        # Unban the user
        await client.unban_chat_member(message.chat.id, target.id)
        await message.reply_text(f"✅ Unbanned **{target.mention}**.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")


@Client.on_message(filters.command("mute") & filters.group)
async def mute_command(client: Client, message: Message):
    # Usage: /mute 1h (Reply to user)
    
    target = await get_target_user(message)
    if not target:
        await message.reply_text("❌ Reply to a user to mute them.")
        return
    
    # Get time (default to 1 hour if not specified)
    if len(message.command) > 1 and not message.reply_to_message:
         # Case: /mute @user 1h (complex parsing, skipping for simplicity)
         pass
    
    # Simple Case: Reply to user + type "/mute 1h"
    args = message.command
    if len(args) < 2:
        await message.reply_text("❌ Please specify time. Example: `/mute 1h`")
        return
        
    duration_str = args[1] # "1h", "30m"
    seconds = get_time_seconds(duration_str)
    
    if seconds == 0:
        await message.reply_text("❌ Invalid time format. Use `m` (mins), `h` (hours), or `d` (days).")
        return

    # Calculate the "Until Date"
    until_date = datetime.now() + timedelta(seconds=seconds)

    try:
        # Mute permissions (cannot send messages)
        permissions = ChatPermissions(can_send_messages=False)
        
        await client.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=target.id,
            permissions=permissions,
            until_date=until_date
        )
        await message.reply_text(f"🔇 Muted **{target.mention}** for `{duration_str}`.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

@Client.on_message(filters.command("unmute") & filters.group)
async def unmute_command(client: Client, message: Message):
    target = await get_target_user(message)
    if not target:
        await message.reply_text("❌ Reply to a user.")
        return
        
    try:
        # Give back all permissions
        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
        
        await client.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=target.id,
            permissions=permissions
        )
        await message.reply_text(f"🔊 Unmuted **{target.mention}**.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
