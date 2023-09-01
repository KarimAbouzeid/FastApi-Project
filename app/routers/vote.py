from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schema, models, database, oauth2

router = APIRouter(
    prefix= "/vote",
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote( vote: schema.Vote, db: Session = Depends(database.get_db), curr_user = Depends(oauth2.get_current_user)):


    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {post_id} doesnot exist")
    
    
    post_id = vote.post_id
    vote_dir = vote.dir

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == post_id, models.Vote.user_id == curr_user.id)
    found_vote = vote_query.first()

    if (vote_dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with id: {curr_user.id} has already voted on post {post_id}")
        
        new_vote = models.Vote(post_id = post_id, user_id = curr_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)

        return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Did not find vote")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted vote"}

    
    
    # user = db.query(models.User).filter(models.User.id == curr_user.id).first()
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {curr_user.id} doesnot exist")
    
    
    # if vote:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with id: {curr_user.id} already voted")

    