# ---------------------------- Imports ------------------------
from flask import Flask, render_template, flash, redirect, request, url_for, jsonify, Blueprint

import json
import logging

from app.models.model import IncomingText, engine, Base, User, IssueReport, ServiceApplication
from app.client_query.user_information import reportIssues, applyForService
 
from array import *
from sqlalchemy.orm import sessionmaker
from json import dumps
from bottle import response

from app.utils.ussd_util import create_user_space, initiliaze_user_space, identify_language
from app.utils.log import log
from app.account_statement.account_number import findAccountNumber 
from app.account_statement.balance import findBalance,  find_account_summary
from app.account_statement.account_history import top_up_history, consumption_history


# ---------------------------- Opening localization --------------------------
with open('app/config/lang.json') as lang:
    language = json.load(lang)

# ---------------------------- Setting u the logger ----------------------

logger = log(__name__, './logs/main_controller.log')
'''
current_module = __name__
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('applogs.log')
stream_handler = logging.StreamHandler()

file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
'''
'''
# Setting up the function that identify which language has been chosen
def identify_language(input_data):
    lang_id = {}

    if input_data[:4] == "1*1*":
       lang_id = dict(num = "1", lang = "kin" )
    elif input_data[:4] == "1*2*":
       lang_id = dict(num = "2", lang = "en")
 
    return lang_id
'''


main = Blueprint('main', __name__)


@main.route('/main', methods=['GET', 'POST'])
def index(): 

    # Defining our session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Retrieving data from the request object as JSON
    data = request.get_json()

    village = data["village"]
    cell = data["cell"]
    sector = data["sector"]
    district = data["district"]
    province = data["province"]
    phonenumber = data["phonenumber"]

    # ServiceApplication.__table__.drop(engine)

    print(village, cell, sector, district, province, phonenumber)
    application = ServiceApplication(village, cell, sector, district, province, phonenumber)
    
    session.add(application)
    session.commit()

    result_db = session.query(ServiceApplication).all()

    for app in result_db:
        print(app.village, app.cell, app.sector, app.district, app.province, app.phonenumber)


    # Extracting data from json data
    '''
    text = data["inputuser"]
    sessioni = data["session"]
    phoneNumber = data["phonenumber"]
    serviceCode = data["serviceCode"]
    '''

    '''
    # User 
    # ----
    username = data['username']
    email = data['email']

    print(username, email)
    variable = "Hello world"

    userinfo = User(username, email)

    # Adding in in the databsase
    session.add(userinfo)
    session.commit()

    result_db = session.query(User).all()

    for user in result_db:
        print("Username: ", user.username, "  ||  ", "Email: ", user.email)
    '''

    # First make sure the user is registered and the session is the same
    # If the session has changed he needs to start from the start
    # create_user_space(text, phoneNumber, sessioni, serviceCode)
    
    #variable = top_up_history("Hello world")
    #variable = consumption_history("Hello world") 
    #variable = reportIssues("hello world")

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

    session.close()

    return "Successfully reached"

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

    ''' ########################  Configuring allowed phones to communicate with the server ################################
    if phoneNumber != '250783435793' and  phoneNumber != '250786485163' and phoneNumber != '250782019621' and phoneNumber != '250784605151'\
        and phoneNumber != '250788420398' and phoneNumber != '250787362618' and phoneNumber != '250786367970':   
        return 'MeshPower USSD service under development, coming soon!'
    '''
    # If the incoming payload lacks one of the below arguments, Talk to havanao to fix incoming parameters on their end
    if sessioni is None or phoneNumber is None or text is None:
        logger.debug("Query missed parameters", "Session: ",sessioni,"Phone: ", phoneNumber,"User input: ", text)
        return "Meshpower USSD service under renovation, try again later"

    # IncomingText.__table__.drop(engine)
    

    create_user_space(text, phoneNumber, sessioni, serviceCode, language)

    # -------------------------------------------------- ## TODO CLEAN up ---------------------------------------------------
    # Defining the variable that will return data from database 
    # user_data = session.query(IncomingText).all()
    # ----------------------------------------------------------------------------------------------------------------------
  
    user_data = session.query(IncomingText).filter(IncomingText.phonenumber == phoneNumber)
 
    # ------------------------ Setting up USSD and facilitate concurrency access of users -------------------------- 
    # We will save data if the phone number is not yet in our database otherwise
    # We will edit the row where the incoming is saved
        
    for row in user_data:
        logger.debug("#### Input: " + str(row.inputuser) + "Phonenumber: " + str(row.phonenumber) + "session: " + str(row.session_id) + "code: " + str(row.servicecode))    


    userInfo = ""
        
    # Querying the initial data
    session_data = user_data[0].session_id
    phone_data = user_data[0].phonenumber
    code_data = user_data[0].servicecode
    input_data = user_data[0].inputuser
    
    lang_id = identify_language(input_data)

#--------------------------------------- USSD Business logic -----------------------------------------
    # Welcome message in English
    if input_data == "1*":
        userInfo = 'CON '+ language['en']['welcome-msg']

    # Menu
    elif input_data == "1*" + lang_id['num']+"*":
        userInfo = 'CON ' + language[lang_id['lang']]['menu']

    # Account functionality
    elif "1*" + lang_id['num'] +"*1*" in input_data:
        userInfo = findAccountNumber(input_data, lang_id, language)
        
    # The balance functionality
    elif "1*" + lang_id['num'] + "*2*" in input_data:
        userInfo = findBalance(input_data, lang_id, language)
    
    # The top up functionality
    elif "1*" + lang_id['num'] + "*3*" in input_data:
        userInfo = top_up_history(input_data, lang_id, language)


    elif "1*" + lang_id['num'] + "*4*" in input_data:
        userInfo = consumption_history(input_data, lang_id, language)

    elif '1*' + lang_id['num'] + '*5*' in input_data:
        userInfo = applyForService(input_data, lang_id, language)


    elif "1*" + lang_id['num'] + "*6*" in input_data:
        userInfo = reportIssues(input_data, lang_id, language)

    elif "1*" + lang_id['num'] + "*7" in input_data:
        userInfo =  find_account_summary(input_data, lang_id, language)

    else:
        # When he clicks something different, we will take him back
        userInfo = initiliaze_user_space(phone_data,  session_data, language)

    session.close()

    
    return userInfo
    
    #return "CON Hello world"

