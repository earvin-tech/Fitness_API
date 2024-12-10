import os

from flask import Flask # type:ignore

from init import db, ma
from controllers.cli_controller import db_commands
from controllers.user_controller import users_bp
from controllers.exercise_controller import exercises_bp

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(users_bp)
    app.register_blueprint(exercises_bp)

    return app