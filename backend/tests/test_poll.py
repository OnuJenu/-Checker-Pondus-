import pytest
from flask import Flask
from werkzeug.exceptions import BadRequest
from app.services.poll_service import PollService
from app.models.poll import Poll
from app.models.voting_option import VotingOption
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

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
