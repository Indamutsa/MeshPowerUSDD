from flask import Flask, render_template, flash, redirect, request, url_for, jsonify,  Blueprint
from app.models.model import User, IncomingText
from app import db
from array import *

main = Blueprint('main', __name__)


@main.route('/main', methods=['GET', 'POST'])
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



userinfo = ["text", "session", "phone", "ussdcode"]



@main.route('/', methods=['GET', 'POST'])
def home():
    sessioni = request.args.get("SessionID")
    phoneNumber = request.args.get("msisdn")
    serviceCode = request.args.get('welcome')
    text = request.args.get('input') 
    solar = request.args.get('solars')

    #------------ Converting incoming arguments into text from encoders ------
    text = str(text)
    serviceCode = str(serviceCode)
    phoneNumber = str(phoneNumber)
    sessioni = str(sessioni)
   
     
    print("------------i-----------------------")
    print(sessioni)
    print(phoneNumber)
    print(serviceCode)
    print(text)
    print(solar)
    print(userinfo[1] + "-------------------Hello----------------")



    if text == "780*1*1":
        print("yes")    
        userInfo = "CON Welcome to MeshPower\nPlease choose:\n1. Kinyarwanda\n2. English"
 
    elif len(text) == 1:
        print("sfhjksdhfl")

        if text == "2":
             userInfo = "CON Press\n1. Balance\n2. Account history\n3. Payment"
        elif text == "1":
             userInfo = "CON Kanda\n1. Amafranga asigaye\n2. Uko konti yakoreshejwe\n3. Kwishyura umuriro"
        elif len(text) == 3:             
             return userInput
    else:
        return "Please choose the right choice, Try again"
    return userInfo

