from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..model import models
from ..database import get_db
from ..core import oauth2, utils
from ..schema import schemas
from typing import List

router = APIRouter(
    prefix="/post",
    tags=["Posts"]
)


@router.get('/', response_model=List[schemas.PostResponse])
def get_all_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    posts = db.query(models.Post).all()

    return posts

@router.get('/own', response_model=List[schemas.PostResponse])
def get_own_post(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found")
    
    return posts



@router.post('/create', status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.CreatePost, 
                db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(**post.model_dump(), owner_id = current_user.id)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/update/{id}", response_model=schemas.PostResponse)
def update_post(
    id: int,
    post: schemas.UpdatePost,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    existing_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if existing_post.owner_id != current_user.id and current_user.role != models.UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post"
        )

    for key, value in post.model_dump().items():
        setattr(existing_post, key, value)

    db.commit()
    db.refresh(existing_post)
    return existing_post


@router.patch("/patch/{id}", response_model=schemas.PostResponse)
def patch_post(
    id: int,
    post: schemas.PatchPost,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    existing_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if existing_post.owner_id != current_user.id and current_user.role != models.UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post"
        )

    update_data = post.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(existing_post, key, value)

    db.commit()
    db.refresh(existing_post)
    return existing_post


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found")
    
    if post.owner_id != current_user.id and current_user.role !=  models.UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )

    db.delete(post)
    db.commit()
    return None






