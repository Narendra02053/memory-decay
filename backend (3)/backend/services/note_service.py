from db.notes_model import add_note, get_notes

def create_note(data):
    add_note(data)

def fetch_notes(email):
    return get_notes(email)
