from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database, utils


router = APIRouter( 
    prefix="/users",
    tags=['Users'])

@router.get("/", response_model=List[schemas.User])
async def get_users_list(db: Session = Depends(database.get_db)):
    return db.query(models.User).all()

@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_password = utils.get_password_hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, update_user: schemas.UserUpdate, db: Session = Depends(database.get_db)):
    user_query = db.query(models.User).filter(models.User.id == user_id)
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    
    if update_user.password:
        update_user.password = utils.get_password_hash(update_user.password)
    user_query.update(update_user.dict(), synchronize_session=False)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, db: Session = Depends(database.get_db)):
    try:
        user_query = db.query(models.User).filter(models.User.id == user_id)
        user = user_query.outerjoin(models.Post, models.Post.owner_id == models.User.id).group_by(models.User.id).first()
    except Exception as e:
        raise e
    return user
