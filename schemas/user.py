from pydantic import BaseModel, validator
from werkzeug.security import check_password_hash

from utils.database import db


class UserSignin(BaseModel):
    username: str
    password: str

    @validator('password')
    def user_is_valid(cls, password, values):
        username = values.get('username')
        user = db.user.find_one({'username': username})
        if not user:
            raise ValueError('账户或密码错误')
        pwhash = user['password']
        passwd_check = check_password_hash(pwhash, password)
        if not passwd_check:
            raise ValueError('账户或密码错误')
        return password
