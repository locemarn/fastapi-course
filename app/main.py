from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(post.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(vote.router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Welcome to my new api!!!!"}

