import sys
sys.path.append('./')
import pytest
from app import schemas

from app import schemas
# authorized : client session
def test_get_all_posts(authorized_client, test_post):
     response = authorized_client.get('/posts/')
     assert response.status_code == 200

def test_get_one_posts(authorized_client, test_post):
     response = authorized_client.get(f'/posts/{test_post[0].id}')
     post = schemas.PostOut(**response.json())
     print(test_post[0])
     assert response.status_code == 200
     assert post.Post.id == test_post[0].id

# unauthorized : client session
def test_get_unauthorized_posts(client, test_post):
     response = client.get('/posts/')
     assert response.status_code == 401
     

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client, test_user, test_post, title, content, published):
     response = authorized_client.post('/posts/', json={'title': title, 'content': content, 'published': published})
     post_details = schemas.Post(**response.json())
     assert post_details.user_id == test_user['id']
     assert post_details.title == title
     assert post_details.content == content
     assert post_details.published == published

def test_create_post_default_published_true(authorized_client, test_user):
     title = 'tesla'
     content = 'Model-Y'
     response = authorized_client.post('/posts/', json={'title': title, 'content' : content})
     post = schemas.Post(**response.json())
     assert response.status_code == 201
     assert post.title == title
     assert post.content == content

def test_unauthorized_user_create_post(client):
     title = 'tesla'
     content = 'Model-Y'
     response = client.post('/posts/', json={'title': title, 'content' : content})
     assert response.status_code == 401 

def test_unauthorized_user_delete_post(client, test_post):
     response = client.delete(f'/posts/{test_post[0].id}')
     assert response.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_post):
     response = authorized_client.delete(f'/posts/{test_post[0].id}')
     assert response.status_code == 204 

def test_delete_post_non_exist(authorized_client, test_user, test_post):
     res = authorized_client.delete('/posts/9999')
     assert res.status_code == 400

def test_delete_other_user_post(authorized_client, test_user, test_post):
     response = authorized_client.delete(f'/posts/{test_post[4].id}')
     assert response.status_code == 401



def test_update_post(authorized_client, test_user, test_post):
    data = {
        "title": "updated title",
        "content": "updatd content",

    }
    res = authorized_client.put(f"/posts/{test_post[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_unauthorized_update_post(authorized_client, test_user, test_another_user, test_post):
     data = {
        "title": "updated title",
        "content": "updatd content"
    }
     response = authorized_client.put(f"/posts/{test_post[4].id}", json=data)
     assert response.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_post):
     data = {
        "title": "updated title",
        "content": "updatd content"
    }
     res = authorized_client.delete('/posts/9999', json=data)
     assert res.status_code == 400