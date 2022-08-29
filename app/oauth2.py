from base64 import encode
from curses.ascii import HT
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas, database, models
from . config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict, expired_delta: Union[timedelta, None] = None):
    # payload
    to_encode = data.copy()
    if expired_delta:
        expire = datetime.utcnow() + expired_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({'exp': expire})
    # creating jwt token - payload, secretkey, algorithm
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="couldn't validate credentials", headers={"WWW-Authentication": "Bearer"})
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    return user
