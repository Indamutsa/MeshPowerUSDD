# ---------------------------- Imports ------------------------
from flask import Flask, render_template, flash, redirect, request, url_for, jsonify, Blueprint
import json
from app.models.model import IncomingText, engine #, User
from array import *
from sqlalchemy.orm import sessionmaker
from json import dumps
from bottle import response

from app.utils.ussd_util import create_user_space
from app.account_statement.account_number import findAccountNumber 
from app.account_statement.balance import findBalance
from app.account_statement.account_history import top_up_history, consumption_history


main = Blueprint('main', __name__)


@main.route('/main', methods=['GET', 'POST'])
def index(): 

    # Defining our session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Retrieving data from the request object as JSON
    data = request.get_json()
   
    # Extracting data from json data
    text = data["inputuser"]
    sessioni = data["session"]
    phoneNumber = data["phonenumber"]
    serviceCode = data["serviceCode"]

    # First make sure the user is registered and the session is the same
    # If the session has changed he needs to start from the start
    # create_user_space(text, phoneNumber, sessioni, serviceCode)
    
    #variable = top_up_history("Hello world")
    variable = consumption_history("Hello world")
    

    '''
    arr = []

    # Retrieving all data in the database
    result_db = session.query(IncomingText).all()
    #result_db = session.query(IncomingText).filter(IncomingText.phonenumber == phoneNumber)

    for user in result_db:
        print("======>:  " + user.phonenumber)
        data = {"Text":user.inputuser, "Session": user.session_id, "Phone": user.phonenumber, "Ussd code": user.servicecode}
        arr.append(data)

    #return jsonify({"Text": user.inputuser, "Session": user.session_id, "Phonenumber":user.phonenumber, "Code":user.servicecode})
    #return dumps(arr)
    '''
    return variable

@main.route('/', methods=['GET', 'POST'])
def home():

    ''' 
    #==============================###### Africa's talking retrieving data #####=============================================#
  
    data = request.form

    #data = request.json["sessionId"]
    #print(data, "***********###")
    
    sessioni = data["sessionId"]
    phoneNumber = data["phoneNumber"]
    serviceCode = data["serviceCode"]
    text = data["text"]
    networkCode = data["networkCode"]
   
    print(sessioni, phoneNumber, serviceCode, text, networkCode)

    sessioni = request.args.get("sessionId")
    phoneNumber = request.args.get("phoneNumber")
    serviceCode = request.args.get('serviceCode')
    text = request.args.get('text') 
    solar = request.args.get('networkCode')

    #==============================###### END  Africa's talking retrieving data #####=============================================#
    '''

    # Defining our session
    Session = sessionmaker(bind=engine)
    session = Session()
   
    #------------ Retrieving data from request object from havanao server
    sessioni = request.args.get("session")
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
    
    print("------------out------------------")
    print("Session ===>: ",sessioni)
    print("Phone-number ===>: ",phoneNumber)
    print("Service code ===>: ",serviceCode)
    print("Text ===>: ",text)
    print( "-------------------Hello----------------")

    if phoneNumber != '250783435793' and  phoneNumber != '250786485163' and phoneNumber != '250782019621' and phoneNumber != '250784605151'\
        and phoneNumber != '250788420398':   
        return 'MeshPower USSD service under development, coming soon!'

    # If the incoming payload lacks one of the below arguments, Talk to havanao to fix incoming parameters on their end
    if sessioni is None or phoneNumber is None or text is None:
        #print(sessioni, phoneNumber, text, serviceCode)
        return "Meshpower USSD service under renovation, try again later"

    #IncomingText.__table__.drop(engine)


    create_user_space(text, phoneNumber, sessioni, serviceCode)

    #Defining the variable that will return data from database 
    #user_data = session.query(IncomingText).all()
  
    user_data = session.query(IncomingText).filter(IncomingText.phonenumber == phoneNumber)
 
    # ------------------------ Setting up USSD and facilitate concurrency access of users -------------------------- 
    # We will save data if the phone number is not yet in our database otherwise
    # We will edit the row where the incoming is saved
    #for r in result:
        
    for row in user_data:
        print("####### Input: ", row.inputuser, "Phonenumber: ", row.phonenumber, "session: ",row.session_id, "code: ", row.servicecode)    


    userInfo = ""
    '''
    #Iniitialize the database if there is none
    if size == 0: 
        init_db()   

    #If the database size is one we can operate otherwise, there is an issue that should be fixed
    if size == 1:
        if "780*1*1" in text:
            text = "1" 

        # Querying the initial data
        session_data = user_data[0].session_id
        phone_data = user_data[0].phonenumber
        code_data = user_data[0].servicecode
        input_data = user_data[0].inputuser
     
        #If the data from db is dummy, initialize it
        if input_data == "dummy":
            user_data[0].inputuser = "1*" 
        #Otherwise we will concatenate the input with *
        else:
            user_data[0].inputuser =  input_data + text + "*"
   
        # Populating the db with incoming variables        
        user_data[0].session_id = sessioni
        user_data[0].phonenumber = phoneNumber
        user_data[0].servicecode = serviceCode 
   
        #If the session is different, that means we need to reinitialize data in the db
        if session_data != sessioni and size == 1: 
            user_data[0].inputuser = "1*"
            user_data[0].phonenumber = phoneNumber
            user_data[0].session_id = sessioni
   
        #Populating variable with data from db
        session_data = user_data[0].session_id
        phone_data = user_data[0].phonenumber
        code_data = user_data[0].servicecode
        input_data = user_data[0].inputuser

        
#--------------------------------------- USSD Business logic -----------------------------------------
        # Welcome message in English
        if input_data == "1*":
            userInfo = "CON Welcome to MeshPower\nPlease choose:\n1. Kinyarwanda\n2. English"

        # Welcome message in Kinyarwanda
        elif input_data == "1*1*":
            userInfo = "CON Kanda\n1. Amafranga asigaye\n2. Uko konti yakoreshejwe\n3. Kwishyura umuriro\n00. Subira ahatangira"

        # The english menu
        elif input_data == "1*2*":
            userInfo = "CON Select:\n1. Account number\n2. Check Balance\n3. Top up history\n4.\
                    Consumption history\n5. Apply for service\n6. Report issues\n00. Back Home"       
    
        # Account functionality
        elif "1*2*1*" in input_data:
            userInfo = findAccountNumber(input_data)
            
        # The balance functionality
        elif "1*2*2*" in input_data:
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
    create_user_space(text, phoneNumber, sessioni, serviceCode)        
    db.session.commit()

    return userInfo
    '''
    return "CON Hello world"
