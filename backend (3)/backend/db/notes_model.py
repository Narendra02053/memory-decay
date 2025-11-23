from .connection import notes_col


def add_note(note):
    notes_col.insert_one(note)


def get_notes(email):
    cursor = notes_col.find({"email": email}).sort("_id", -1)
    notes = []
    for doc in cursor:
        notes.append(
            {
                "id": str(doc.get("_id")),
                "email": doc.get("email"),
                "title": doc.get("title"),
                "content": doc.get("content"),
            }
        )
    return notes
