from ast import Dict
from typing import List, Optional
from fastapi import Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import models, schemas
from .. database import get_db
from .. oauth2 import get_current_user

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


# read all posts -
@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user), count: int = 5, skip: int = 0, search: Optional[str] = ""):

    results = db.query(models.Post, func.count(models.Vote.user_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id,
                                                                                         isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(count).offset(skip).all()
    return results


# read individual post -
@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = db.query(models.Post, func.count(models.Vote.user_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with the id : {id} not found!',
        )
    return result


# create a post -
@router.post('/', response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # using kwargs for automatically unwrapping the dictionary
    db_post = models.Post(**post.dict(), user_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


# delete the post -
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_data = post_query.first()
    if post_data is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='no such post found'
        )
    if post_data.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='not authorized to perform requested operation'
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update the post
@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_data = post_query.first()
    if post_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id : {id} not found'
        )
    if post_data.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='not authorized to perform requested operation'
        )
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
