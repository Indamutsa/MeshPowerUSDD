from flask import Flask, render_template, flash, redirect, request, url_for, jsonify
from app_ussd import db


@app.route('/account', methods=['GET', 'POST'])
def index():

    data = request.get_json()
    username = data["username"]
    email = data["email"]

    user = User(username, email)
    db.session.add(user)
    db.session.commit()

    db_data = User.query.all()

    for name_user in db_data:
        print("======>:  " + name_user.username)

    return jsonify({"username": name_user.username, "email": name_user.email})