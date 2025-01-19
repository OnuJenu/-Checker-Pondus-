import pytest
from flask import json
from app import create_app
from app.models.user import User
from app.services.auth_service import create_user, authenticate_user, generate_tokens

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_user(clean_db):
    # Test creating a new user
    user = create_user('testuser', 'newuser@example.com', 'testpass')
    assert user.username == 'testuser'
    assert user.password_hash is not None

def test_authenticate_user(clean_db):
    # Test authenticating a user
    user = create_user('testuser', 'newuser@example.com', 'testpass')
    user = authenticate_user('testuser', 'testpass')
    assert user is not None
    assert user.username == 'testuser'

def test_generate_tokens(clean_db):
    # Test token generation
    user = create_user('testuser', 'newuser@example.com', 'testpass')
    tokens = generate_tokens(user)
    assert 'access_token' in tokens
    assert 'refresh_token' in tokens
    assert tokens['token_type'] == 'bearer'

def test_login_route(clean_db, client):
    # Test login route with valid credentials
    user = create_user('testuser', 'newuser@example.com', 'testpass')
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data
    assert 'refresh_token' in data

def test_login_route_invalid_credentials(clean_db, client):
    # Test login route with invalid credentials
    user = create_user('testuser', 'newuser@example.com', 'testpass')
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'wrongpass'
    })
    assert response.status_code == 401

def test_register_route(client):
    # Test user registration
    response = client.post('/register', json={
        'username': 'newuser',
        'password': 'newpass',
        'email': 'newuser@example.com'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data
    assert 'refresh_token' in data

def test_register_route_missing_fields(client):
    # Test registration with missing fields
    response = client.post('/register', json={
        'username': 'newuser',
        'password': 'newpass'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
