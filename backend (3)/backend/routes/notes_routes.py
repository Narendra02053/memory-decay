from fastapi import APIRouter
from pydantic import BaseModel
from db.notes_model import add_note, get_notes

router = APIRouter(prefix="/api/notes", tags=["Notes"])

class NoteInput(BaseModel):
    email: str
    title: str
    content: str

@router.post("/add")
def add_note_api(data: NoteInput):
    add_note(data.dict())
    return {"status": "success"}

@router.get("/{email}")
def notes_api(email: str):
    return {"status": "success", "notes": get_notes(email)}
