from fastapi import FastAPI
# from . import models
# from .database import engine
from .routers import posts, users, votes, auth
# from pydantic import BaseSettings
# from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# # engine for sqlalchemy connecting database - creating tables
# alternate option chosen : alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(votes.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {'message': 'Welcome to FAST API container !'}
