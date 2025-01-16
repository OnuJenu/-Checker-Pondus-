import os
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.databases.database import db
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=None):
    app = Flask(__name__, instance_path=os.path.join(os.getcwd()))
    CORS(app)
    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_object('app.config.Config')

    # Initialize database
    from app.databases.database import init_db
    init_db()
    
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Initialize services
    from app.services.poll_service import PollService
    app.poll_service = PollService()

    from app.routes.auth import auth_blueprint
    from app.routes.poll import poll_blueprint
    from app.routes.media import media_blueprint

    with app.app_context():
        app.register_blueprint(auth_blueprint)
        app.register_blueprint(poll_blueprint)
        app.register_blueprint(media_blueprint)

    return app
