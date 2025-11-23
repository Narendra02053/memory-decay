# MongoDB Usage in Memory Decay Predictor

## Why MongoDB is Used

MongoDB is used to **persist data** (store information permanently) for the following features:
1. **Chat History** - Save conversation history between users and the AI
2. **Notes** - Store user study notes
3. **Predictions** - Save prediction records for analysis
4. **Users** - Store user information (if user management is implemented)

## Important: MongoDB is OPTIONAL

The application is designed to work **WITHOUT MongoDB**. If MongoDB is not available:
- ✅ Predictions still work (ML model doesn't need database)
- ✅ Chat still works (but history won't be saved)
- ✅ Notes won't be saved (but can still be created temporarily)
- ⚠️ All database operations fail gracefully with error messages

---

## Where MongoDB is Used

### 1. **Database Connection Setup**
**File:** `backend (3)/backend/db/connection.py`

- Sets up MongoDB connection
- Creates collections: `users`, `notes`, `chat_history`, `predictions`
- Uses lazy loading (only connects when needed)
- Handles connection failures gracefully

**Collections Created:**
- `users` - User accounts
- `notes` - Study notes
- `chat_history` - Chat conversations
- `predictions` - Prediction records

---

### 2. **Chat History Storage**
**Files:**
- `backend (3)/backend/db/chat_model.py`
- `backend (3)/backend/routes/chat_routes.py`

**What it does:**
- **Saves chat messages** when user chats with AI
- **Retrieves chat history** for a specific user (by email)

**MongoDB Operations:**
```python
# Save a message
chat_col.insert_one({
    "email": "user@example.com",
    "sender": "user" or "bot",
    "message": "message text"
})

# Get chat history
chat_col.find({"email": email}).sort("_id", 1)
```

**Used in:**
- `POST /api/chat/` - Saves user and bot messages
- `GET /api/chat/{email}` - Retrieves chat history

---

### 3. **Notes Storage**
**Files:**
- `backend (3)/backend/db/notes_model.py`
- `backend (3)/backend/routes/notes_routes.py`

**What it does:**
- **Saves study notes** created by users
- **Retrieves all notes** for a specific user

**MongoDB Operations:**
```python
# Save a note
notes_col.insert_one({
    "email": "user@example.com",
    "title": "Note title",
    "content": "Note content"
})

# Get all notes for a user
notes_col.find({"email": email}).sort("_id", -1)
```

**Used in:**
- `POST /api/notes/add` - Creates a new note
- `GET /api/notes/{email}` - Gets all notes for a user

---

### 4. **Prediction History**
**File:** `backend (3)/backend/routes/prediction_routes.py`

**What it does:**
- **Saves prediction records** (input data + prediction result)
- Used for analytics and tracking prediction history

**MongoDB Operations:**
```python
# Save prediction
pred_col.insert_one({
    "topic_name": "...",
    "category": "...",
    # ... all input fields ...
    "prediction": 5.23  # prediction result
})
```

**Used in:**
- `POST /api/predict/` - Saves prediction after making it

**Note:** This is **non-critical** - predictions work without saving to DB

---

### 5. **User Management** (if implemented)
**File:** `backend (3)/backend/db/user_model.py`

**What it does:**
- **Creates user accounts**
- **Retrieves user information**

**MongoDB Operations:**
```python
# Create user
users_col.insert_one({
    "email": "user@example.com",
    # ... other user fields
})

# Get user
users_col.find_one({"email": email})
```

---

## Summary Table

| Feature | File | Collection | Purpose | Required? |
|---------|------|------------|---------|-----------|
| **Chat History** | `db/chat_model.py`<br>`routes/chat_routes.py` | `chat_history` | Save/retrieve chat messages | ❌ Optional |
| **Notes** | `db/notes_model.py`<br>`routes/notes_routes.py` | `notes` | Save/retrieve study notes | ❌ Optional |
| **Predictions** | `routes/prediction_routes.py` | `predictions` | Save prediction records | ❌ Optional |
| **Users** | `db/user_model.py` | `users` | User account management | ❌ Optional |
| **Connection** | `db/connection.py` | - | MongoDB setup & connection | ❌ Optional |

---

## How It Works Without MongoDB

All MongoDB operations are wrapped in **try-except blocks**:

```python
try:
    chat_col = get_chat_col()
    if chat_col:
        chat_col.insert_one({...})
except Exception as e:
    print(f"MongoDB save failed (non-critical): {e}")
    # Continue without saving
```

**Result:** The app continues to work, but data won't be persisted.

---

## To Use MongoDB (Optional Setup)

1. **Install MongoDB:**
   - Download from: https://www.mongodb.com/try/download/community
   - Or use MongoDB Atlas (cloud): https://www.mongodb.com/cloud/atlas

2. **Create `.env` file** in `backend (3)/backend/`:
   ```env
   MONGO_URI=mongodb://127.0.0.1:27017
   DB_NAME=memory_decay_db
   ```

3. **Start MongoDB:**
   - Windows: MongoDB should start as a service
   - Linux/Mac: `mongod` or `sudo systemctl start mongod`

4. **Verify connection:**
   - The app will automatically connect when first database operation is needed
   - Check terminal for connection messages

---

## Database Schema

### `chat_history` Collection
```json
{
  "_id": ObjectId("..."),
  "email": "user@example.com",
  "sender": "user" | "bot",
  "message": "message text"
}
```

### `notes` Collection
```json
{
  "_id": ObjectId("..."),
  "email": "user@example.com",
  "title": "Note title",
  "content": "Note content"
}
```

### `predictions` Collection
```json
{
  "_id": ObjectId("..."),
  "topic_name": "Neuroplasticity",
  "category": "science",
  "domain": "school",
  "category_type": "concept",
  "study_time": 1.5,
  "review_count": 2,
  "confidence": 4,
  "difficulty": "medium",
  "stress_level": 2,
  "sleep_hours": 7.5,
  "mood": "calm",
  "distraction_level": 1,
  "recent_event": "none",
  "attention_level": 4,
  "prediction": 5.23
}
```

### `users` Collection
```json
{
  "_id": ObjectId("..."),
  "email": "user@example.com",
  // ... other user fields
}
```

---

## Key Points

✅ **MongoDB is completely optional** - the app works without it  
✅ **All database operations fail gracefully** - no crashes if MongoDB is unavailable  
✅ **Predictions work independently** - ML model doesn't need database  
✅ **Data persistence is the only benefit** - without MongoDB, data is lost on server restart  

