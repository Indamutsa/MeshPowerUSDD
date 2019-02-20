from flask import Flask, render_template, flash, redirect, request, url_for, jsonify,  Blueprint
from app.models.model import User
from app import db

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():

    data = request.get_json()
    username = data["username"]
    email = data["email"]

    user = User(username, email)
    print(user.username)

    db.session.add(user)
    db.session.commit()

    db_data = User.query.all()

    for name_user in db_data:
        print("======>:  " + name_user.username)

    return jsonify({"username": name_user.username, "email": name_user.email})

    # return "hello world"
