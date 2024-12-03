from flask import Flask # type:ignore

from init import db, ma

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://fitness_dev:123456@localhost:5432/fitness_db"