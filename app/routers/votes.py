from os import stat
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from .. import schemas, utils, models, database, oauth2


router = APIRouter(
     prefix='/votes',
     tags=['Votes']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
     post = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id).first()
     if post is None:
          raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f'post with {vote.post_id} not found')
     # check if user  liked or unliked
     voted = vote.upvote
     vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
     data_available = vote_query.first()
     print(voted, data_available)
     if voted:
          if data_available is not None:
               raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail ='already liked post')
          else:
               vote_data = models.Vote(post_id = vote.post_id, user_id = current_user.id)
               db.add(vote_data)
               db.commit()
               db.refresh(vote_data)
               return {'message': 'successfully added vote'}
     else:
          if data_available is None:
               raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = 'already disliked post')
          else:
               vote_query.delete(synchronize_session=False)
               db.commit()
               return {'message': 'successfully deleted vote'}
