import pytest
from werkzeug.exceptions import BadRequest
from app.models.poll import Poll
from app.models.vote import Vote
from app.models.voting_option import VotingOption
from app import db

from app.services.poll_service import PollService

from tests.custom_fixtures import app, client, poll_fixture, test_image_data, authenticated_client

def test_vote_valid(app, authenticated_client, poll_fixture, test_image_data):
    """Test successful vote submission"""
    # Setup test poll with active status
    test_poll = poll_fixture(test_image_data)
    
    # Get voting options
    voting_options = test_poll.voting_options

    # Submit vote for first option
    with authenticated_client.application.app_context():
      user_id = authenticated_client.user.id

      response = authenticated_client.post(
        f'/polls/{test_poll.id}/vote',
        json={
            'option_id': voting_options[0].id
        }
      )
    
    # Verify response
    assert response.status_code == 200
    assert response.get_json()['success'] is True
    
    # Verify vote is recorded in database
    with authenticated_client.application.app_context():
        user_id = authenticated_client.user.id
        vote = db.session.query(Vote).filter_by(
            poll_id=test_poll.id,
            option_id=voting_options[0].id,
            user_id=user_id
        ).first()
        
        assert vote is not None
        assert vote.poll_id == test_poll.id
        assert vote.option_id == voting_options[0].id

# def test_vote_invalid_poll_id(app, authenticated_client):
#     """Test voting on a non-existent poll"""
#     with app.app_context():
#         response = authenticated_client.post(
#             '/polls/999/vote',
#             json={
#                 'option_id': 1
#             }
#         )
    
#     assert response.status_code == 404
#     assert response.get_json()['error'] == "Poll not found"

# def test_vote_poll_not_active(app, authenticated_client, poll_fixture, test_image_data):
#     """Test voting on an inactive poll"""
#     test_poll = poll_fixture(test_image_data)
#     test_poll.is_active = False
#     db.session.commit()

#     with app.app_context():
#         response = authenticated_client.post(
#             f'/polls/{test_poll.id}/vote',
#             json={
#                 'option_id': test_poll.voting_options[0].id
#             }
#         )
    
#     assert response.status_code == 400
#     assert response.get_json()['error'] == "Poll is no longer active"

# def test_vote_user_already_voted(app, authenticated_client, poll_fixture, test_image_data):
#     """Test voting when user has already voted"""
#     test_poll = poll_fixture(test_image_data)
#     user_id = authenticated_client.user.id

#     # Create initial vote
#     vote = Vote(
#         poll_id=test_poll.id,
#         option_id=test_poll.voting_options[0].id,
#         user_id=user_id
#     )
#     db.session.add(vote)
#     db.session.commit()

#     with app.app_context():
#         response = authenticated_client.post(
#             f'/polls/{test_poll.id}/vote',
#             json={
#                 'option_id': test_poll.voting_options[0].id
#             }
#         )
    
#     assert response.status_code == 400
#     assert response.get_json()['error'] == "User has already voted on this poll"

# def test_vote_invalid_option(app, authenticated_client, poll_fixture, test_image_data):
#     """Test voting with an invalid option"""
#     test_poll = poll_fixture(test_image_data)

#     with app.app_context():
#         response = authenticated_client.post(
#             f'/polls/{test_poll.id}/vote',
#             json={
#                 'option_id': 999
#             }
#         )
    
#     assert response.status_code == 400
#     assert response.get_json()['error'] == "Invalid voting option"

# def test_vote_database_error(app, authenticated_client, poll_fixture, test_image_data):
#     """Test voting when database error occurs"""
#     test_poll = poll_fixture(test_image_data)

#     # Simulate database error
#     db.session.rollback()

#     with app.app_context():
#         response = authenticated_client.post(
#             f'/polls/{test_poll.id}/vote',
#             json={
#                 'option_id': test_poll.voting_options[0].id
#             }
#         )
    
#     assert response.status_code == 500
#     assert response.get_json()['error'] == "Failed to record vote"
