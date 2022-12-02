import os
from app import schemas

# Load users_db
users_db = [{
    "fullname": "admin", 
    "email":os.environ['SUPERUSER'], 
    "password":os.environ['SUPERUSER_PASSWORD']
    }]

def add_user(data: schemas.UserSchema):
    #TO DO: Use a DB instead, and don't forget to hash out the password before saving it.
    for user in users_db:
        if user.get('email') == data.email:
            return False
    users_db.append(data)
    return True

def check_user(data: schemas.UserLoginSchema):
    for user in users_db:
        if user.get('email') == data.email and user.get('password') == data.password:
            return True
    return False
