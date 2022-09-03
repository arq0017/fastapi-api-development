import sys
sys.path.append('./')

from app import models

import pytest 

@pytest.fixture
def test_vote(test_post, test_user, session):
     # directly commiting to votes table
     new_vote = models.Vote(post_id = test_post[3].id, user_id = test_post[3].user_id)
     session.add(new_vote)
     session.commit()

def test_vote_on_post(authorized_client, test_post):
     data = {
          'post_id' : test_post[0].id,
          'upvote' : True
     }
     response = authorized_client.post('/votes/', json=data)
     assert response.status_code == 201

def test_vote_twice_post(authorized_client, test_post, test_vote):
     data = {
          'post_id' : test_post[3].id,
          'upvote' : True
     }
     response = authorized_client.post('/votes/', json=data)
     assert response.status_code == 409

def test_delete_vote(authorized_client, test_vote, test_post):
     data = {
          'post_id' : test_post[3].id,
          'upvote' : False
     }
     response = authorized_client.post('/votes/', json=data)
     assert response.status_code == 201

def test_delete_already_false_vote(authorized_client, test_post):
     data = {
          'post_id' : test_post[3].id,
          'upvote' : False
     }
     response = authorized_client.post('/votes/', json=data)
     assert response.status_code == 409

def test_delete_non_exist_vote(authorized_client, test_post):
     data = {
          'post_id' : 999,
          'upvote' : False
     }
     response = authorized_client.post('/votes/', json=data)
     assert response.status_code == 404
