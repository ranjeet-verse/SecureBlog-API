from dotenv import load_dotenv
load_dotenv()
from app.core.logging_config import logger
from fastapi import FastAPI
from .database import engine
from .model import models
from .routers import user, post, auth
from fastapi.middleware.cors import CORSMiddleware




models.Base.metadata.create_all(bind=engine)

app = FastAPI()

logger.info("🚀 FastAPI application started")



@app.get('/')
def main():
    return{'data': 'Non NOM NOM '}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(post.router, prefix="/api/v1")