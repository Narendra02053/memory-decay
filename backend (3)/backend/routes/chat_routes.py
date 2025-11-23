from fastapi import APIRouter
from pydantic import BaseModel
from services.chat_service import chat_with_ai
from db.chat_model import save_message, get_chat_history

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatInput(BaseModel):
    email: str
    message: str

@router.post("/")
def chat_api(data: ChatInput):
    try:
        user_msg = data.message.strip()
        email = data.email.strip()
        
        if not user_msg:
            return {"status": "error", "reply": "Message cannot be empty."}
        if not email:
            return {"status": "error", "reply": "Email is required."}

        bot_reply = chat_with_ai(user_msg)

        save_message(email, "user", user_msg)
        save_message(email, "bot", bot_reply)

        return {"status": "success", "reply": bot_reply}
    except Exception as e:
        print(f"[CHAT API] Error: {e}")
        return {"status": "error", "reply": "An error occurred while processing your message. Please try again."}

@router.get("/{email}")
def history(email: str):
    return {"status": "success", "history": get_chat_history(email)}
