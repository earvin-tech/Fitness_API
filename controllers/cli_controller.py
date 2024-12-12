from flask import Blueprint # type: ignore

from init import db
from models.user import User
from models.exercise import Exercise
from models.workout import Workout
from models.workout_exercise import WorkoutExercise

db_commands = Blueprint("db", __name__)


@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")


@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")


@db_commands.cli.command("seed")
def seed_tables():

    users = [
        User(
            f_name="User",
            l_name="One",
            dob="1998-01-28",
            email="user1@email.com"
        ),
        User(
            f_name="User",
            l_name="Two",
            dob="2000-04-20",
            email="user2@email.com"
        )
    ]

    exercises = [
        Exercise(
            name="Bicep curl",
            muscle_group="Arms"
        ),
        Exercise(
            name="Squat",
            muscle_group="Lower body"
        )
    ]

    workouts = [
        Workout(
            name="Arm workout",
            user_id=1,
            workout_date="2024-12-08",
            duration="01:40:00"
        ),
        Workout(
            user_id=1,
            workout_date="2024-12-10",
            duration="01:20:00"
        )
    ]

    workout_exercises = [
        WorkoutExercise(
            workout_id=1,
            exercise_id=1,
            sets=3,
            reps=12,
            weight=12.00
        )
    ]

    db.session.add_all(users)
    db.session.add_all(exercises)
    db.session.add_all(workouts)
    db.session.add_all(workout_exercises)

    db.session.commit()

    print("Tables seeded")