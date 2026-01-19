from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..model import models
from ..database import get_db
from ..core import oauth2, utils
from ..schema import schemas
from typing import List


router = APIRouter(prefix="/user",
                    tags=["User"])

@router.post("/create",status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(
    user: schemas.CreateUser,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    hashed_password = utils.hash(user.password)

    user_count = db.query(models.User).count()

    role = (
        models.UserRole.admin
        if user_count == 0
        else models.UserRole.user
    )

    new_user = models.User(
        email=user.email,
        password=hashed_password,
        role=role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = oauth2.create_access_token(
        data={
            "sub": str(new_user.id),
            "role": new_user.role.value
        }
    )

    return {
        "user": new_user,
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get('/all', response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.admin_only)):

    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=204,
                            detail="There are no users")
    
    return users



@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with this {id} id was not found")
    
    if user.id != current_user.id and current_user.role != models.UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )
   
    db.delete(user)
    db.commit()

    return None
    