# Importing the flask class
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# The database we are using here
db = SQLAlchemy()


# -------------------------------------------  The function that creates our app ------------------------------------------------------------
def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ussd:123456@db:5432/ussd_db"

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = '123456'

    db.init_app(app)

    print()

    # -----------------------

    from app.main.route import main

    print("----------------------------------: ")
    app.register_blueprint(main)

    return app
