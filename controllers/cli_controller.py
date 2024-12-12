from flask import Blueprint # type: ignore

from init import db
from models.user import User
from models.exercise import Exercise
from models.workout import Workout
from models.workout_exercise import WorkoutExercise
from models.goal import Goal

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
            f_name="John",
            l_name="Smith",
            dob="1998-01-28",
            email="jsmith@email.com"
        ),
        User(
            f_name="Jen",
            l_name="Wang",
            dob="2000-04-20",
            email="jenw@email.com"
        ),
        User(
            f_name="Antonio",
            l_name="Chavez",
            dob="1999-02-15",
            email="Achav@email.com"
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
        ),
        Exercise(
            name="Tricep pulldown",
            muscle_group="Arms"
        ),
        Exercise(
            name="Barbell curls",
            muscle_group="Arms"
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
            user_id=2,
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
        ),
        WorkoutExercise(
            workout_id=1,
            exercise_id=3,
            sets=3,
            reps=8,
            weight=15.00
        ),
        WorkoutExercise(
            workout_id=1,
            exercise_id=4,
            sets=2,
            reps=10,
            weight=12.50
        )
    ]

    goals = [
        Goal(
            name="Stronger Arms",
            exercise_id=1,
            user_id=1,
            goal_weight=20.00,
            status_achieved=False
        )
    ]

    db.session.add_all(users)
    db.session.add_all(exercises)
    db.session.add_all(workouts)
    db.session.add_all(workout_exercises)
    db.session.add_all(goals)

    db.session.commit()

    print("Tables seeded")