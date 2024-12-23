import os

from flask import Flask # type:ignore
from marshmallow.exceptions import ValidationError # type: ignore
from dotenv import load_dotenv # type: ignore
load_dotenv()

from init import db, ma
from controllers.cli_controller import db_commands
from controllers.user_controller import users_bp
from controllers.exercise_controller import exercises_bp
from controllers.workout_controller import workouts_bp
from controllers.workout_exercise_controller import workout_exercises_bp
from controllers.goal_controller import goals_bp

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    db.init_app(app)
    ma.init_app(app)

    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {"message": err.messages}, 400
    
    @app.errorhandler(400)
    def bad_request(err):
        return {"message": str(err)}, 400
    
    @app.errorhandler(404)
    def not_found(err):
        return {"message": str(err)}, 404

    app.register_blueprint(db_commands)
    app.register_blueprint(users_bp)
    app.register_blueprint(exercises_bp)
    app.register_blueprint(workouts_bp)
    app.register_blueprint(workout_exercises_bp)
    app.register_blueprint(goals_bp)
    
    app.json.sort_keys = False

    return app