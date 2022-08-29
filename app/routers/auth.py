from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db

from .. import schemas, models, utils, oauth2


router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', response_model=schemas.Token)
async def login(usr_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == usr_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='incorrect userId')
    if not utils.verify_password(usr_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='incorrect password')
    # generate token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    # validate token
    print(access_token)
    return {'access_token': access_token, 'token_type': 'Bearer'}
