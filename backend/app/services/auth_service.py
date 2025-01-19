from app.config import settings
from flask import redirect, url_for
from authlib.integrations.flask_client import OAuth
from app.models.user import User
from werkzeug.security import check_password_hash

oauth = OAuth()

def create_user(username, email, password):
    """Create a new user with the given username, email, and password"""
    return User.create_user(
        username=username,
        email=email,
        password=password,
    )

google = oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)

def authenticate_user(username, password):
    user = User.get_user_by_username(username)
    if user and check_password_hash(user.password_hash, password):
        return user
    return None

import datetime
import jwt

def generate_tokens(user):
    # Generate access token with 15 minute expiration
    access_token = jwt.encode({
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }, settings.JWT_SECRET_KEY, algorithm='HS256')

    # Generate refresh token with 7 day expiration
    refresh_token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }, settings.JWT_SECRET_KEY, algorithm='HS256')

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }

def redirect_to_google_auth():
    return google.authorize_redirect(redirect_uri=settings.GOOGLE_REDIRECT_URI)

def handle_google_callback():
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()
    return authenticate_with_google(user_info)

def authenticate_with_google(user_info):
    user = User.get_user_by_oauth_id(user_info['id'])
    if not user:
        user = User.create_user(
            username=user_info['email'],
            email=user_info['email'],
            oauth_id=user_info['id']
        )
    return user

# Twitter OAuth integration
twitter = oauth.register(
    name='twitter',
    client_id=settings.TWITTER_CLIENT_ID,
    client_secret=settings.TWITTER_CLIENT_SECRET,
    access_token_url='https://api.twitter.com/oauth2/token',
    authorize_url='https://api.twitter.com/oauth2/auth',
    api_base_url='https://api.twitter.com/v1/',
    client_kwargs={'scope': 'email profile'}
)

def redirect_to_twitter_auth():
    return twitter.authorize_redirect(redirect_uri=settings.TWITTER_REDIRECT_URI)

def handle_twitter_callback():
    token = twitter.authorize_access_token()
    user_info = twitter.get('userinfo').json()
    return authenticate_with_twitter(user_info)

def authenticate_with_twitter(user_info):
    user = User.get_user_by_oauth_id(user_info['id'])
    if not user:
        user = User.create_user(
            username=user_info['email'],
            email=user_info['email'],
            oauth_id=user_info['id']
        )
    return user

# Facebook/Instagram OAuth integration
facebook = oauth.register(
    name='facebook',
    client_id=settings.FACEBOOK_CLIENT_ID,
    client_secret=settings.FACEBOOK_CLIENT_SECRET,
    access_token_url='https://graph.facebook.com/oauth2/token',
    authorize_url='https://graph.facebook.com/oauth2/auth',
    api_base_url='https://graph.facebook.com/v1/',
    client_kwargs={'scope': 'email profile'}
)

def redirect_to_facebook_auth():
    return facebook.authorize_redirect(redirect_uri=settings.FACEBOOK_REDIRECT_URI)

def handle_facebook_callback():
    token = facebook.authorize_access_token()
    user_info = facebook.get('userinfo').json()
    return authenticate_with_facebook(user_info)

def authenticate_with_facebook(user_info):
    user = User.get_user_by_oauth_id(user_info['id'])
    if not user:
        user = User.create_user(
            username=user_info['email'],
            email=user_info['email'],
            oauth_id=user_info['id']
        )
    return user
