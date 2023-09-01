from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter 
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import schema, models, oauth2
from ..database import get_db
from typing import List, Optional


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# @router.get("/", response_model=List[schema.Post])
@router.get("/", response_model=List[schema.PostOut])
def get_posts(db: Session = Depends(get_db), curr_user = Depends(oauth2.get_current_user), limit: int = 10, search: Optional[str] = "",
skip: int = 0):

    # posts = cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    print(curr_user.email)
    # posts =  db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(posts)
    posts = list ( map (lambda x : x._mapping, posts) )
    return posts


@router.get("/{id}", response_model=schema.PostOut) # Path parameter 
def get_post(id: int, db: Session = Depends(get_db), curr_user =  Depends(oauth2.get_current_user)):
    
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()

    # post = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Vote.post_id).filter(models.Post.id == id).first()
    # post2 = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    post2 = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter= True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(post2)
    if not post2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=  f"Post with id {id} was not found!")
    # post2 = list ( map (lambda x : x._mapping, post2) )
    return post2


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db), curr_user= Depends(oauth2.get_current_user)):

    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    
    new_post = models.Post(owner_id=curr_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post




@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), curr_user = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    # deleted_post = cursor.fetchone()



    deleted_post = db.query(models.Post).filter(models.Post.id==id)
    if not deleted_post.first():
        # conn.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} does not exist")
    
    if deleted_post.first().owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authourized to peform requested action")

    deleted_post.delete(synchronize_session=False)
    db.commit()
   
    # conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, post:schema.PostCreate, db: Session = Depends(get_db), curr_user= Depends(oauth2.get_current_user)):
    
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",(post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = post_query.first()

    if not updated_post:
        # conn.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} does not exist")
    
    if updated_post.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authourized to peform requested action")
    
    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit() 
    
    return post_query.first()