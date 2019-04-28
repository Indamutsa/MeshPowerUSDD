from sqlalchemy.orm import sessionmaker
from app.models.model import IncomingText, engine
import re

# Since havanao didn't have USSD backbone such as keeping the session in place, concatening the user input
# and so much, we set up this function to take care of user session, concatening the user input and keep track
# of the user where he/she might be down ussd tree
def create_user_space(inputuser, phonenumber, sessioni, serviceCode):
    
    # Initialize the session
    session = initialize_session()

    if isinstance(inputuser, str) or isinstance(inputuser, int):
        pass
    else:
        initialize_user_space(phonenumber, sessioni)
    

    # Querrying the database to see if we already have this number in our database
    result = session.query(IncomingText).filter(IncomingText.phonenumber == phonenumber)


    # print("########################################################################")
    print("-----------------> ", result.count())

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
            print("======== || ====>>  Number already exists")
    #----------------------------------------------------------------------------------------------------------------
    # This time the user details should be in the database
    result = session.query(IncomingText).filter(IncomingText.phonenumber == phonenumber)

    inputuser_db = result[0].inputuser
    session_db = result[0].session_id


    # If the session is different, we also make sure we reinitialize the inputuser and session because
    # He will start from the top of the tree
    print("===================================================================", type(inputuser), session_db)

    if session_db != sessioni:
        print("It is different==========================")
        initiliaze_user_space(phonenumber, sessioni)

    #----------------------------------------------------------------------------------------------------------------
    
    # If the session is the same as we have in the db, the user can go on and continue down the tree
    elif session_db == sessioni and inputuser != '0' and inputuser != '00' :
        if "1*2*5*" in inputuser_db or "1*2*6" in inputuser_db: 
            concatenateInput(inputuser, inputuser_db, phonenumber)
        
        elif re.match(r'[0-9]', inputuser):
            concatenateInput(inputuser, inputuser_db, phonenumber)


        '''
        inputuser_db = inputuser_db + inputuser + "*"
        
        # Update it to the database and commit it
        session.query(IncomingText).filter(IncomingText.phonenumber == phonenumber)\
            .update({ IncomingText.inputuser: inputuser_db }, synchronize_session = False)
        session.commit()
        '''

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

def initiliaze_user_space(phonenumber, sessioni):
    
    userInfo = "CON Welcome to MeshPower\nPlease choose:\n1. Kinyarwanda\n2. English"

    # Initialize the session
    session = initialize_session()
    
    # We reinitialize the tree back to the root
    inputuser_db = "1*"
    session_db = sessioni
    
    print("=============||=========================", session_db)

    # Update the very row we changed to the database and commit it
    session.query(IncomingText).filter(IncomingText.phonenumber == phonenumber)\
        .update({IncomingText.inputuser: inputuser_db, IncomingText.session_id: session_db}, synchronize_session = False)
    session.commit()

    result = session.query(IncomingText).filter(IncomingText.phonenumber == phonenumber)
    print(result[0].session_id, result[0].inputuser, "-------||-------------------||-------------")

    session.close()

    return userInfo

def goBackToRoot(phonenumber):

    # Initialize the session
    session = initialize_session()
    
    inputuser_db = "1*"

    # Update it to the database and commit it
    session.query(IncomingText).filter(IncomingText.phonenumber == phonenumber)\
        .update({ IncomingText.inputuser: inputuser_db }, synchronize_session = False)
    session.commit()

    session.close()

def goBackOnce(inputuser_db, phonenumber):
    
    # Initialize the session
    session =  initialize_session()

    # We would like to make sure when we reaches the root, we stop
    if len(inputuser_db) > 2:
        inputuser_db = inputuser_db[:-2]
    else:
        inputuser_db = "1*"

    # Update it to the database and commit it
    session.query(IncomingText).filter(IncomingText.phonenumber == phonenumber)\
        .update({ IncomingText.inputuser: inputuser_db }, synchronize_session = False)
    session.commit()

    session.close()

def concatenateInput(inputuser, inputuser_db, phonenumber):

    # Initialize the session
    session =  initialize_session()

    input_db = inputuser_db + inputuser + "*"

    # Update it to the database and commit it
    session.query(IncomingText).filter(IncomingText.phonenumber == phonenumber)\
       .update({ IncomingText.inputuser: input_db }, synchronize_session = False)
    session.commit()

    session.close()


def initialize_session():

    # Defining our session
    Session = sessionmaker(bind=engine)
    session = Session()

    return session    
