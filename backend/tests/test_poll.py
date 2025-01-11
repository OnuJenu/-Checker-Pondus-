import pytest
from werkzeug.exceptions import BadRequest
from app.models.poll import Poll
from app import db

from app.services.poll_service import PollService

from tests.custom_fixtures import app, client, poll_fixture, test_image_data

def test_get_poll_success(client, poll_fixture, test_image_data):
    """Test successful retrieval of an existing poll"""
    test_poll = poll_fixture(test_image_data)

    response = client.get(f'/polls/{test_poll.id}')
    poll_data = response.get_json()
    
    assert poll_data['question'] == "Which color do you prefer?"
    assert len(poll_data['options']) == 2
    assert poll_data['options'][0]['media_type'] == "image"
    assert poll_data['options'][1]['media_type'] == "image"

def test_get_poll_not_found(client):
    """Test retrieval of non-existent poll"""
    response = client.get('/polls/999999')
    assert response.status_code == 404
    assert "Poll not found" in response.get_json()['error']

def test_get_poll_with_closed_status(client, poll_fixture, test_image_data):
    """Test retrieval of closed poll"""
    test_poll = poll_fixture(test_image_data)

    with client.application.app_context():
        test_poll.is_active = False
        db.session.commit()
        
    response = client.get(f'/polls/{test_poll.id}')
    assert response.status_code == 200
    assert response.get_json()['is_active'] is False

def test_create_poll_success(app):
    """Test successful poll creation with valid inputs"""
    test_data = {
        "question": "Which color do you prefer?",
        "option1": {
            "media_type": "text",
            "media_url": "https://example.com/text1",
            "description": "Blue"
        },
        "option2": {
            "media_type": "text",
            "media_url": "https://example.com/text2",
            "description": "Red"
        }
    }
    
    with app.app_context():
        poll_service = PollService()
        poll = poll_service.create_new_poll(
            question=test_data['question'],
            option_one=test_data['option1'],
            option_two=test_data['option2'],
            user_id=1  # Assuming test user ID
        )
    
    assert isinstance(poll, Poll)
    assert poll.question == test_data['question']
    assert len(poll.voting_options) == 2

def test_create_poll_missing_fields(app):
    """Test poll creation with missing required fields"""
    test_data = {
        "question": "Which color do you prefer?",
        "option1": {
            "media_type": "text",
            "media_url": "https://example.com/text1"
        },
        # Missing option2
    }
    
    with app.app_context():
        poll_service = PollService()
        with pytest.raises(BadRequest) as exc_info:
            poll_service.create_new_poll(
                question=test_data['question'],
                option_one=test_data['option1'],
                option_two={},  # Empty option
                user_id=1
            )
        
        assert "Options must contain media_type and media_url" in str(exc_info.value)

def test_create_poll_invalid_media_type(app):
    """Test poll creation with invalid media type"""
    test_data = {
        "question": "Which color do you prefer?",
        "option1": {
            "media_type": "invalid",
            "media_url": "https://example.com/text1"
        },
        "option2": {
            "media_type": "text",
            "media_url": "https://example.com/text2"
        }
    }
    
    with app.app_context():
        poll_service = PollService()
        with pytest.raises(BadRequest) as exc_info:
            poll_service.create_new_poll(
                question=test_data['question'],
                option_one=test_data['option1'],
                option_two=test_data['option2'],
                user_id=1
            )
    
    assert "Invalid media_type" in str(exc_info.value)

def test_create_poll_invalid_url_format(app):
    """Test poll creation with invalid URL format"""
    test_data = {
        "question": "Which color do you prefer?",
        "option1": {
            "media_type": "text",
            "media_url": "invalid-url"
        },
        "option2": {
            "media_type": "text",
            "media_url": "https://example.com/text2"
        }
    }
    
    with app.app_context():
        poll_service = PollService()
        with pytest.raises(BadRequest) as exc_info:
            poll_service.create_new_poll(
                question=test_data['question'],
                option_one=test_data['option1'],
                option_two=test_data['option2'],
                user_id=1
            )
    
    assert "Invalid media URL" in str(exc_info.value)

def test_create_poll_missing_media_fields(app):
    """Test poll creation with missing media fields"""
    test_data = {
        "question": "Which color do you prefer?",
        "option1": {
            "media_url": "https://example.com/text1"
        },
        "option2": {
            "media_type": "text",
            "media_url": "https://example.com/text2"
        }
    }
    
    with app.app_context():
        poll_service = PollService()
        with pytest.raises(BadRequest) as exc_info:
            poll_service.create_new_poll(
                question=test_data['question'],
                option_one=test_data['option1'],
                option_two=test_data['option2'],
                user_id=1
            )
    
    assert "must contain media_type and media_url" in str(exc_info.value)
