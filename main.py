"""
This is the main file for this project, post management system for our blog: guildmagesforum.tw.
It is powered by FastApi, jose, pydantic passlib.
"""

import random
from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

SECRET_KEY = "" # todo
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTS = 30

class PostInfo (BaseModel):
    """the BaseModel of PostInfo"""

    hackmd_url: str
    author: str
    status: str

class User (BaseModel):
    """the BaseModel of user information"""

    username: str
    passwd: bytes
    full_name: Union[str, None] = None
    email: Union[str, None] = None
    disable: Union[str, None] = None

class Token (BaseModel):
    """the BaseModel of JWT token"""

    acess_token: str
    token_type: str

class TokenData (BaseModel):
    """the BaseModel of user data"""

    username: Union[str, None] = None

pwd_context = CryptContext ( schemes = ["bcrypt"], deprecated = "auto" )
oauth2_scheme = OAuth2PasswordBearer ( tokenUrl = "token" )

def raise_bad_request ( message ):
    """ raise bad request"""

    raise HTTPException ( status_code = 400, detail = message )
