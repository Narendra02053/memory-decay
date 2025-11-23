from .connection import get_chat_col


def save_message(email, sender, message):
    try:
        chat_col = get_chat_col()
        if chat_col:
            chat_col.insert_one(
                {
                    "email": email,
                    "sender": sender,
                    "message": message,
                }
            )
    except Exception as e:
        print(f"[CHAT MODEL] MongoDB save failed (non-critical): {e}")


def get_chat_history(email):
    try:
        chat_col = get_chat_col()
        if chat_col:
            cursor = chat_col.find({"email": email}).sort("_id", 1)
            history = []
            for doc in cursor:
                history.append(
                    {
                        "id": str(doc.get("_id")),
                        "email": doc.get("email"),
                        "sender": doc.get("sender"),
                        "message": doc.get("message"),
                    }
                )
            return history
    except Exception as e:
        print(f"[CHAT MODEL] MongoDB read failed (non-critical): {e}")
    return []
