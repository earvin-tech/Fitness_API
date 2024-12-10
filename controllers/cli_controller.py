from flask import Blueprint # type: ignore

from init import db
from models.user import User
from models.exercise import Exercise

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

    db.session.add_all(users)
    db.session.add_all(exercises)

    db.session.commit()

    print("Tables seeded")