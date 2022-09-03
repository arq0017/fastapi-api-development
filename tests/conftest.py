import sys
sys.path.append('./')

from app.models import Post
from app.database import Base, get_db
from app.oauth2 import create_access_token
from app.main import app
import pytest
from app.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient



# database connection dependency
# assign postgres url
SQLALCHEMY_TEST_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"


# create engine
test_engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)


# each instance of SessionLocal will be a database session
TestSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine)


# session fixture - for creating sessions
# return - sqlalchemy.orm.Session
@pytest.fixture()
def session():
    # using sqlalchemy for creating and deleting table
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    # database
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# client fixture - for getting and manipulating db object
# return type - session - sqlalchemy.orm.Session
# return type TestClient(app) - startlette.testclient.TestClient
@pytest.fixture
def client(session):
    def get_test_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = get_test_db
    yield TestClient(app)

# creating user


@pytest.fixture
def test_user(client):
    user_data = {"email": "arqam123@gmail.com", "password": "password123"}
    response = client.post('/users/', json=user_data)
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user

# getting token

@pytest.fixture
def test_another_user(client):
    user_data = {"email": "amber123@gmail.com", "password": "password123"}
    response = client.post('/users/', json=user_data)
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token(data={'user_id': test_user['id']})

# client authorization - The HTTP Authorization request header can be used to provide credentials that authenticate a user agent with a server, allowing access to a protected resource.


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token}'}
    return client


@pytest.fixture
def test_post(test_user,test_another_user, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "user_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "user_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "user_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "user_id": test_user['id']
    }, {
        "title": "4rth title",
        "content": "4rth content",
        "user_id": test_another_user['id']
    }]

    def create_post_model(post):
        return Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    # adding post to database
    session.add_all(posts)
    session.commit()
    response = session.query(Post).all()
    return response
