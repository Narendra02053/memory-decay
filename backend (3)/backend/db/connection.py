from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017")
DB_NAME = os.getenv("DB_NAME", "memory_decay_db")

# Lazy connection - only connect when needed, with timeout
_client = None
_db = None

def get_client():
    global _client
    if _client is None:
        try:
            _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
            # Test connection
            _client.server_info()
        except Exception as e:
            print(f"[DB] MongoDB connection failed (non-critical): {e}")
            _client = None
    return _client

def get_db():
    global _db
    if _db is None:
        client = get_client()
        if client:
            _db = client[DB_NAME]
        else:
            return None
    return _db

def get_collection(name):
    db = get_db()
    if db:
        return db[name]
    return None

# Collections with lazy loading
def get_users_col():
    return get_collection("users")

def get_notes_col():
    return get_collection("notes")

def get_chat_col():
    return get_collection("chat_history")

def get_prediction_col():
    return get_collection("predictions")

# Backward compatibility - but these will be None if MongoDB is not available
users_col = None
notes_col = None
chat_col = None
prediction_col = None
