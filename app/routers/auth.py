from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.model import models
from app.core import oauth2, utils
from app.core.logging_config import logger

router = APIRouter(prefix="/login",
                tags=["Authentication"])


@router.post("/")
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"Login attempt for email={user_credentials.username}")

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username
    ).first()

    if not user:
        logger.warning(f"Login failed: user not found ({user_credentials.username})")
        raise HTTPException(status_code=403, detail="Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        logger.warning(f"Login failed: wrong password ({user.email})")
        raise HTTPException(status_code=403, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(
        data={"sub": str(user.id), "role": user.role.value}
    )

    logger.info(f"Login success for user_id={user.id}")
    return {"access_token": access_token, "token_type": "bearer"}
