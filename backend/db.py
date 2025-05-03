import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")

client = AsyncIOMotorClient(MONGODB_URI)
db = client[DB_NAME]
<<<<<<< Updated upstream
prescriptions_collection = db["prescriptions"]
=======
prescriptions_collection = db["prescriptions"]
users_collection = db["users"]
# Function to check if the database connection is working
async def check_connection():
    try:
        # The ismaster command is cheap and does not require auth
        await client.admin.command('ismaster')
        return True
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return False
>>>>>>> Stashed changes
