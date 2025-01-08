# Initialize the routes package

from flask import Blueprint

auth_blueprint = Blueprint('auth', __name__)
poll_blueprint = Blueprint('poll', __name__)
media_blueprint = Blueprint('media', __name__)

# Import routes to register them with the blueprints
from app.routes import auth, poll, media
