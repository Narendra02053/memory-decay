from .connection import users_col

def create_user(user):
    users_col.insert_one(user)

def get_user(email):
    return users_col.find_one({"email": email})
