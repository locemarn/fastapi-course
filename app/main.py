import os
import time
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth
from dotenv import load_dotenv

load_dotenv()

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

host = os.getenv('POSTGRES_HOSTNAME')
database = os.getenv('POSTGRES_DATABASE')
username = os.getenv('POSTGRES_USERNAME')
password = os.getenv('POSTGRES_PASSWORD')

while True:
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=username,
            password=password,
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

app.include_router(post.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(auth.router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Welcome to my new api!!!!"}

