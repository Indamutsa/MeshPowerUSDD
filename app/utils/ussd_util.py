from sqlalchemy.orm import sessionmaker
from app.models.model import IncomingText, engine
from app.utils.log import log

import re


logger = log(__name__, './logs/utils.log')



# Setting up the function that identify which language has been chosen
def identify_language(input_data):
    lang_id = {}

    if  "1*1*" in input_data[:4]:
       lang_id = dict(num = "1", lang = "kin" )
    elif  "1*2*" in input_data[:4]:
       lang_id = dict(num = "2", lang = "en")

    return lang_id

# Since havanao didn't have USSD backbone such as keeping the session in place, concatening the user input
# and so much, we set up this function to take care of user session, concatening the user input and keep track
# of the user where he/she might be down ussd tree
def create_user_space(inputuser, phonenumber, sessioni, serviceCode, language):
    
    # Initialize the session
    session = initialize_session()

    if isinstance(inputuser, str) or isinstance(inputuser, int):
        pass
    else:
        initialize_user_space(phonenumber, sessioni)
    

    # Querrying the database to see if we already have this number in our database
    result = session.query(IncomingText).filter(IncomingText.phonenumber == phonenumber)


    logger.debug("Number of rows of a given number : -----------------> " + str( result.count()))

    #-----------------------------------------------------------------------------------------------------------------
    # If the user is not in the database, we make sure we add the user according to his phone number
    if result.count() == 0:

        # We want to make sure that when the number does not exist that we catch the exception
        try:

            # Populatating our object using a constructor
            userinfo = IncomingText('1*', sessioni, phonenumber, serviceCode)

            # Adding in in the databsase
            session.add(userinfo)
            session.commit()

            return

        except:
            logger.debug("======== || ====>>  Number already exists " + str(phonenumber))
    #----------------------------------------------------------------------------------------------------------------
    # This time the user details should be in the database
    result = session.query(IncomingText).filter(IncomingText.phonenumber == phonenumber)

    inputuser_db = result[0].inputuser
    session_db = result[0].session_id


    # If the session is different, we also make sure we reinitialize the inputuser and session because
    # He will start from the top of the tree
    print("===================================================================", type(inputuser), session_db)
    
    lang_id = identify_language(inputuser_db)
    print(lang_id, inputuser_db, "/////////////////////////////////////")

    if session_db != sessioni:
        logger.debug("Session is different, we shall go ahead and reinitialize user space ===================")
        initiliaze_user_space(phonenumber, sessioni, language)

    #----------------------------------------------------------------------------------------------------------------
   
    #lang_id = identify_language(inputuser_db)

    # If the session is the same as we have in the db, the user can go on and continue down the tree
    elif session_db == sessioni and inputuser != '0' and inputuser != '00' :
        print(bool(lang_id), inputuser_db, "+++++++++++++++++++++++++++++++++++++++++")
        
        # We first make sure the dict is loaded
        if bool(lang_id) == True: 
            
            if "1*" + lang_id['num'] + "*5*" in inputuser_db or "1*" + lang_id['num'] + "*6" in inputuser_db: 
                concatenateInput(inputuser, inputuser_db, phonenumber)

            elif re.match(r'[0-9]', inputuser):
                concatenateInput(inputuser, inputuser_db, phonenumber)

        elif re.match(r'[0-9]', inputuser):
            concatenateInput(inputuser, inputuser_db, phonenumber)

    #---------------------------------- Going back once -------------------------------------------------------------

    # If the session is the same as we have in the db, we would to go back once until we hit the root
    elif session_db == sessioni and inputuser == '0':
        # Go back to back once
        goBackOnce(inputuser_db, phonenumber)

    #---------------------------------- Going back HOME (on the root of the tree ) ----------------------------------

    # If the session is the same as we have in the db, the user can go on and continue down the tree
    elif session_db == sessioni and inputuser == '00':
        # Go back to root of the tree (home)
        goBackToRoot(phonenumber)
    #----------------------------------------------------------------------------------------------------------------
    session.close()


    ###########################################################################################
    #                     REUSABLE FUNCTIONS                                                  #
    ###########################################################################################

def initiliaze_user_space(phonenumber, sessioni, language):
    
    userInfo = 'CON '+ language['en']['welcome-msg']

    # Initialize the session
    session = initialize_session()
    
    # We reinitialize the tree back to the root
    inputuser_db = "1*"
    session_db = sessioni
    
    print("=============||=========================", session_db)
    
    try:
        # Update the very row we changed to the database and commit it
        session.query(IncomingText).filter(IncomingText.phonenumber == phonenumber)\
            .update({IncomingText.inputuser: inputuser_db, IncomingText.session_id: session_db}, synchronize_session = False)
    except Exception as e:
        logger.debug(e)
    else:
        # We will commit if no exception is thrown
        session.commit()

        result = session.query(IncomingText).filter(IncomingText.phonenumber == phonenumber)
        print(result[0].session_id, result[0].inputuser, "-------||-------------------||-------------")
        session.close()
    finally:
        logger.debug("Inside reinitialized" + str(phonenumber))

    return userInfo

def goBackToRoot(phonenumber):

    # Initialize the session
    session = initialize_session()
    
    inputuser_db = "1*"

    try:
        # Update it to the database and commit it
        session.query(IncomingText).filter(IncomingText.phonenumber == phonenumber)\
            .update({ IncomingText.inputuser: inputuser_db }, synchronize_session = False)
    
    except Exception as e:
        logger.debug(e)
    else:
        session.commit()

        session.close()
    finally:
        logger.debug("Inside goback to root" + str(phonenumber))

def goBackOnce(inputuser_db, phonenumber):
    
    # Initialize the session
    session =  initialize_session()

    # We would like to make sure when we reaches the root, we stop
    if len(inputuser_db) > 2:
        inputuser_db = re.sub('\*[\w \d]+\*$', '', inputuser_db ) + "*"

        print(inputuser_db, "*************************************")
    else:
        inputuser_db = "1*"

    try:
        # Update it to the database and commit it
        session.query(IncomingText).filter(IncomingText.phonenumber == phonenumber)\
            .update({ IncomingText.inputuser: inputuser_db }, synchronize_session = False)
    except Exception as e:
        logger.debug(e)

    else:

        session.commit()

        session.close()
    finally:
       logger.debug("Inside goback once" + str(phonenumber))


def concatenateInput(inputuser, inputuser_db, phonenumber):

    # Initialize the session
    session =  initialize_session()

    input_db = inputuser_db + inputuser + "*"
    try:
        # Update it to the database and commit it
        session.query(IncomingText).filter(IncomingText.phonenumber == phonenumber)\
           .update({ IncomingText.inputuser: input_db }, synchronize_session = False)
    except Exception as e:
        logger.debug(e)
    else:
    
        session.commit()

        session.close()
    finally:
        logger.debug('inside concatenate function' + str(phonenumber))

def initialize_session():

    # Defining our session
    Session = sessionmaker(bind=engine)
    session = Session()

    return session   

