from flask import Flask, render_template, flash, redirect, request, url_for, jsonify,  Blueprint
from app.models.model import User, IncomingText
from app import db
from array import *
from app.balance.hello import world
from app.account_statement.account_number import findAccountNumber 
from app.account_statement.balance import findBalance

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

@main.route('/', methods=['GET', 'POST'])
def home():
    
    # import pdb 
    # pdb.set_trace()

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
    serviceCode = "780*1*1" 
   
    world()
     
    #return "Hello world"
 
    print("------------out----------------")
    print(sessioni)
    print(phoneNumber)
    print(serviceCode)
    print(text)
    print( "-------------------Hello----------------")
 
    user_data = IncomingText.query.all()
    size = len(user_data)
    print("Size is ", size)
   
    userInfo = ""

    if size == 0: 
        init_db()   
    
    if size == 1:
        if "780*1*1" in text:
            text = "1" 

        session_data = user_data[0].session_id
        phone_data = user_data[0].phonenumber
        code_data = user_data[0].servicecode
        input_data = user_data[0].inputuser
     
        if input_data == "dummy":
            user_data[0].inputuser = "1*" 
        else:
            user_data[0].inputuser =  input_data + text + "*"
        
        user_data[0].session_id = sessioni
        user_data[0].phonenumber = phoneNumber
        user_data[0].servicecode = serviceCode 
   
        
        if session_data != sessioni and size == 1: 
            user_data[0].inputuser = "1*"
            user_data[0].phonenumber = phoneNumber
            user_data[0].session_id = sessioni


        session_data = user_data[0].session_id
        phone_data = user_data[0].phonenumber
        code_data = user_data[0].servicecode
        input_data = user_data[0].inputuser


       
        print("Size is ==> ", input_data)

        if input_data == "1*":
            userInfo = "CON Welcome to MeshPower\nPlease choose:\n1. Kinyarwanda\n2. English"
        elif input_data == "1*1*":
            userInfo = "CON Kanda\n1. Amafranga asigaye\n2. Uko konti yakoreshejwe\n3. Kwishyura umuriro\n00. Subira ahatangira"
        elif input_data == "1*2*":
            userInfo = "CON Press\n1. Account number\n2. Check Balance\n3. Payment\n4. Account history\n5. Review the service\n\
6. Apply for service\n7. Report issues\n00. Back Home"       
        elif "1*2*1*" in input_data:
            userInfo = findAccountNumber(input_data)
            
        elif input_data == "1*2*2*":
            print("Reached")
            userInfo = findBalance(input_data)

        elif input_data == "1*2*3*":
            userInfo = "Account history functionality in progress"


        elif input_data == "1*2*4*":
            userInfo = "Review functionality in progress"


        elif input_data == "1*2*5*":
            userInfo = "Application for service functionality in progress"


        elif input_data == "1*2*6*":
            userInfo = "Report issues functionality in progress"

        else:
            user_data[0].inputuser = "1*"
            userInfo = "CON Welcome to MeshPower\nPlease choose:\n1. Kinyarwanda\n2. English"
            
    db.session.commit()

    return userInfo
    
    #return "CON Hello world"

def init_db():
    userinfo = IncomingText("dummy", "dummy", "dummy", "dummy")
    db.session.add(userinfo)
    db.session.commit()
      
