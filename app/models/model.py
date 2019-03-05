from app import db


class User(db.Model):
    __tablename__ = "user_info"
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(50))

    def __init__(self, username, email):
        self.username = username
        self.email = email

class IncomingText(db.Model):
    __tablename__ = "incoming_text"
    
    id = db.Column('text_id', db.Integer, primary_key=True)
    inputuser = db.Column(db.String(30)) 
    session_id = db.Column(db.String(30))
    phonenumber = db.Column(db.String(30))
    servicecode = db.Column(db.String(30))

    def __init__(self, inputuser, session_id, phonenumber, servicecode):
        self.inputuser = inputuser
        self.session_id = session_id
        self.phonenumber = phonenumber
        self.servicecode = servicecode
