import os
import time
import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models
from alembic import command

load_dotenv()

username = os.getenv('POSTGRES_USERNAME')
password = os.getenv('POSTGRES_PASSWORD')
hostname = os.getenv('POSTGRES_HOSTNAME')
database_name = os.getenv('POSTGRES_DATABASE')

SQLALCHEMY_DATABASE_URL = f'postgresql://{username}:{password}@{hostname}/{database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

while True:
    try:
        conn = psycopg2.connect(
            host=hostname,
            database=database_name,
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

@pytest.fixture
def test_user2(client):
    user_data = {"email": "marcelo123@email.com", "password": "password123"}
    res = client.post("/api/users", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user(client):
    user_data = {"email": "sanjeev@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()

    posts = session.query(models.Post).all()
    return posts