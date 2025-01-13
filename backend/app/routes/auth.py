from flask import Blueprint, request, jsonify
from app.services.auth_service import (
    authenticate_user,
    generate_tokens,
    redirect_to_google_auth,
    handle_google_callback,
    redirect_to_twitter_auth,
    handle_twitter_callback,
    redirect_to_facebook_auth,
    handle_facebook_callback
)

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = authenticate_user(username, password)
    if user:
        tokens = generate_tokens(user)
        return jsonify(tokens)
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_blueprint.route('/google/auth')
def google_auth():
    return redirect_to_google_auth()

@auth_blueprint.route('/google/callback')
def google_callback():
    user = handle_google_callback()
    tokens = generate_tokens(user)
    return jsonify(tokens)

@auth_blueprint.route('/twitter/auth')
def twitter_auth():
    return redirect_to_twitter_auth()

@auth_blueprint.route('/twitter/callback')
def twitter_callback():
    user = handle_twitter_callback()
    tokens = generate_tokens(user)
    return jsonify(tokens)

@auth_blueprint.route('/facebook/auth')
def facebook_auth():
    return redirect_to_facebook_auth()

@auth_blueprint.route('/facebook/callback')
def facebook_callback():
    user = handle_facebook_callback()
    tokens = generate_tokens(user)
    return jsonify(tokens)
