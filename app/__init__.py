import os
# import redis as redis
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config.config import Config
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    # rest of connection code using the connection string `uri`
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5000"}})
    jwt.init_app(app)

    MIGRATION_DIR = os.path.join('config', 'database_migrations_psql')
    migrate.init_app(app, db, directory=MIGRATION_DIR, compare_type=True)

    from app.api import bp as api_bp
    from app.api import payload
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(payload)

    with app.app_context():
        from app import models
        db.create_all()
    return app

#     from app.api import bp as api_bp
#     app.register_blueprint(api_bp, url_prefix='/api')
