from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db
from ..model import models
from ..core import oauth2, utils
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(prefix="/login",
                tags=["Authentication"])


@router.post('/')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(data={
            "sub": str(user.id),
            "role": user.role.value
        })

    return {'access_token': access_token, 'token_type': 'bearer'}
