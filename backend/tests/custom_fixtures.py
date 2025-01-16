import pytest
from app.models.user import User
from app.services.auth_service import generate_tokens
from app.databases.database import db

@pytest.fixture
def test_image_data():
    return {
        "question": "Which color do you prefer?",
        "option1": {
            "media_type": "image",
            "media_url": "https://example.com/image1.jpg",
            "description": "Blue"
        },
        "option2": {
            "media_type": "image",
            "media_url": "https://example.com/image2.jpg",
            "description": "Red"
        }
    }

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def authenticated_client(app, test_db):
    """Fixture to create and login a test user"""
    with app.app_context():    
        # Ensure database is initialized
        test_db
        db.commit()
            
        test_user = db.query(User).filter_by(username="test_user").first()
        
        # If test_user doesn't exist, create a new one
        if not test_user:
            test_user = User(
                username="test_user",
                email="test@example.com",
                password="test_password"
            )
            db.add(test_user)
            db.commit()

        # Login user
        client = app.test_client()
        with client:
            # Set session variables within request context
            with client.session_transaction() as sess:
                sess['user_id'] = test_user.id

        client.user = test_user
        client.tokens = generate_tokens(test_user)

        return client

@pytest.fixture
def poll_fixture(app):
    """Fixture to create a test poll"""
    def create_poll(test_data):
        with app.app_context():
            return app.poll_service.create_new_poll(
                question=test_data['question'],
                option_one=test_data['option1'],
                option_two=test_data['option2'],
                user_id=1
            )
    return create_poll
