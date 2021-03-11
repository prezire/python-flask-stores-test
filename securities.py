from models.users import User
from werkzeug.security import safe_str_cmp

def auth(username:str, password:str):
  user = User.find_by_username(username)
  if user and user.password == password:
    return user
    
def identity(payload):
  return User.find_by_id(payload['identity'])