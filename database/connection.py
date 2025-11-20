import motor.motor_asyncio
from config import MONGO_URL

# 1. Initialize the Client
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)

# 2. Select the Database Name
db = mongo_client["GroupGuardDB"]

# 3. Select the Collection (Table) where we store group info
groups_collection = db["groups"]

print("✅ Connected to MongoDB Database")
