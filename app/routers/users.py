from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from .. import schemas, utils, models
from ..database import get_db  


router = APIRouter(
     prefix='/users',
     tags=['Users']
)

# create user
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hasing password
    hashed_password = utils.get_password_hash(user.password)
    user.password = hashed_password
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# get the user 
@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id : {id} not found")
    return user
