import pytest, sys
sys.path.append('./')

from app import schemas
from app.config import settings
from jose import jwt



def test_login_user(client, test_user):
    response = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**response.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    assert payload['user_id'] == test_user['id']
    assert login_res.token_type == 'Bearer'
    assert response.status_code == 200


@pytest.mark.parametrize('email, password, status_code', [
     ('arqam123@gmail.com', 'password123', 200),
    ('arqam123@gmail.com', 'wrongpassword', 401),
    ('wrongemail@gmail.com', 'password123', 401),
    ('wrongemail@gmail.com', 'wrongpassword', 401),
    (None, 'password123', 422),
    ('arqam123@gmail.com', None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    response = client.post(
        "/login", data={"username": email, "password": password})
    assert response.status_code == status_code
