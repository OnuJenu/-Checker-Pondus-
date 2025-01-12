import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__, instance_path=os.path.join(os.getcwd()))
    CORS(app)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Initialize services
    from app.services.poll_service import PollService
    app.poll_service = PollService()

    from app.routes.auth import auth_blueprint, init_oauth
    from app.routes.poll import poll_blueprint
    from app.routes.media import media_blueprint

    with app.app_context():
        app.register_blueprint(auth_blueprint)
        app.register_blueprint(poll_blueprint)
        app.register_blueprint(media_blueprint)

    return app
