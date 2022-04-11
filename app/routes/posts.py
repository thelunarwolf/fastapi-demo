from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app import database, models, schemas
from sqlalchemy.orm import Session

from app.oauth import get_current_user

router = APIRouter( 
    prefix="/posts",
    tags=['Posts'])

@router.get("/", response_model=List[schemas.Post])
async def get_posts_list(db: Session = Depends(database.get_db), user: schemas.User = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.owner_id == user.id)
    posts = post_query.join(models.User, models.User.id == models.Post.owner_id).all()
    return posts


@router.post("/", response_model=schemas.Post)
async def create_post(post_body: schemas.PostCreate, db: Session = Depends(database.get_db), user: schemas.User = Depends(get_current_user)):
   post = models.Post(**post_body.dict())
   post.owner_id = user.id
   db.add(post)
   db.commit()
   db.refresh(post)
   return post

@router.get("/{post_id}", response_model=schemas.Post)
async def get_post(post_id: int, db: Session = Depends(database.get_db), user: schemas.User = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.join(models.User, models.User.id == models.Post.owner_id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {post_id} does not exist")
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You cannot access this post")
    return post

@router.put("/{post_id}")
async def update_post(post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(database.get_db), user: schemas.User = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {post_id} does not exist")
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You cannot access this post")
    post_query.update(updated_post.dict())
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{post_id}")
async def delete_post(post_id: int,  db: Session = Depends(database.get_db), user: schemas.User = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {post_id} does not exist")
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You cannot access this post")
    post_query.delete()
    db.commit()
    return {"message": 'Delete Successful'}