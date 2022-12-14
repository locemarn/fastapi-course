from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(vote.router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Welcome to my new api!!!!"}

