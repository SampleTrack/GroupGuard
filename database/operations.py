from .connection import groups_collection

# Default settings for every new group
default_settings = {
    "welcome_enabled": True,
    "anti_link": False,   # Off by default
    "night_mode": False,
    "admin_only": True
}

async def add_group(chat_id, chat_title):
    """
    Adds a group to the database if it doesn't exist.
    """
    # Check if group already exists in DB
    group = await groups_collection.find_one({"_id": chat_id})
    
    if not group:
        # Prepare the data package
        new_group_data = {
            "_id": chat_id,
            "title": chat_title,
            "settings": default_settings
        }
        # Insert into DB
        await groups_collection.insert_one(new_group_data)
        print(f"➕ Added new group: {chat_title}")
    else:
        # Optional: Update title if changed
        pass

async def get_group_settings(chat_id):
    """
    Fetch settings for a specific group.
    """
    group = await groups_collection.find_one({"_id": chat_id})
    if group:
        return group["settings"]
    else:
        return None
