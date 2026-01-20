from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..model import models
from ..database import get_db
from ..core import oauth2, utils
from ..schema import schemas
from app.core.logging_config import logger

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/me", response_model=schemas.UserOut)
def get_current_user(
    current_user: models.User = Depends(oauth2.get_current_user)
):
    logger.info(f"GET /users/me user_id={current_user.id}")
    return current_user


@router.get("/all", response_model=List[schemas.UserOut])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    logger.info(f"GET /users/all requested by user_id={current_user.id}")

    if current_user.role != models.UserRole.admin:
        logger.warning(f"Unauthorized access by user_id={current_user.id}")
        raise HTTPException(status_code=403, detail="Not authorized")

    try:
        users = db.query(models.User).all()
        logger.info(f"Returned {len(users)} users")
        return users
    except Exception:
        logger.exception("Failed to fetch users")
        raise


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserResponse
)
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
        data={"sub": str(new_user.id), "role": new_user.role.value}
    )

    logger.info(f"New user created id={new_user.id}, role={role.value}")

    return {
        "user": new_user,
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )

    if user.id != current_user.id and current_user.role != models.UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user"
        )

    db.delete(user)
    db.commit()

    logger.info(f"User deleted id={id}")
    return None
