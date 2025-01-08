from flask import Blueprint, redirect, url_for, session, request, jsonify
from authlib.integrations.flask_client import OAuth
from app.models.user import User

auth_blueprint = Blueprint('auth', __name__)

# Configure OAuth client
oauth = OAuth()
google = oauth.register(
    name='google',
    client_id='YOUR_GOOGLE_CLIENT_ID',  # Replace with your Google Client ID
    client_secret='YOUR_GOOGLE_CLIENT_SECRET',  # Replace with your Google Client Secret
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'}
)

@auth_blueprint.route('/login')
def login():
    redirect_uri = url_for('auth.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@auth_blueprint.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()

    # Check if the user already exists
    user = User.get_user_by_oauth('google', user_info['id'])
    if not user:
        # Create a new user if they don't exist
        user = User.create_user(
            username=user_info.get('name'),
            email=user_info.get('email'),
            oauth_provider='google',
            oauth_id=user_info['id']
        )

    # Log the user in (this part depends on your session management)
    session['user_id'] = user.id

    return redirect(url_for('auth.index'))

@auth_blueprint.route('/index')
def index():
    if 'user_id' in session:
        user = User.get_user_by_id(session['user_id'])
        return f"Hello, {user.username}!"
    return "Please log in."

# Initialize OAuth with the Flask app
def init_oauth(app):
    oauth.init_app(app)
