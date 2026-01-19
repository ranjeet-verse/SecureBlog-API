from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from .database import engine
from .model import models
from .routers import user, post, auth




models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
def main():
    return{'data': 'Non NOM NOM '}

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)