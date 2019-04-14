from sqlalchemy.orm import sessionmaker
from app.models.model import IncomingText, engine

# Since havanao didn't have USSD backbone such as keeping the session in place, concatening the user input
# and so much, we set up this function to take care of user session, concatening the user input and keep track
# of the user where he/she might be down ussd tree
def create_user_space(inputuser, phonenumber, sessioni, serviceCode):

    # Defining our session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Querrying the database to see if we already have this number in our database
    result = session.query(IncomingText).filter(IncomingText.phonenumber == phonenumber)


    print("########################################################################")
    print("-----------------> ", result.count())

    #-----------------------------------------------------------------------------------------------------------------
    # If the user is not in the database, we make sure we add the user according to his phone number
    if result.count() == 0 and  "780*1*1" in inputuser:

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

    if session_db != sessioni:
        print("It is different==========================")

        # We update the user input and session
        inputuser_db = "1*"
        session_db = sessioni

        # Update it to the database and commit it
        session.query(IncomingText).filter(IncomingText.phonenumber == phonenumber)\
            .update({IncomingText.inputuser: inputuser_db, IncomingText.session_id: session_db}, synchronize_session = False)
        session.commit()
    #----------------------------------------------------------------------------------------------------------------

    # If the session is the same as we have in the db, the user can go on and continue down the tree
    elif session_db == sessioni and inputuser != 0 and inputuser != 00 :
        inputuser_db = inputuser_db + inputuser + "*"

        # Update it to the database and commit it
        session.query(IncomingText).filter(IncomingText.phonenumber == phonenumber)\
            .update({ IncomingText.inputuser: inputuser_db }, synchronize_session = False)
        session.commit()

