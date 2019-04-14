#Importing libraries and entities that we will need to use later
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

#Define our engine that will help us connect to the database
engine = create_engine('postgresql://ussd:123456@db:5432/ussd_db', echo=True)

#Defining a base class stores a catlog of classes and mapped tables
Base = declarative_base()

'''
#Defining our simple testing class
class User(Base):
	__tablename__ = "user_info"

	id = Column('user_id',Integer, primary_key=True)
	username = Column(String(20))
	email = Column(String(50))

	# Defining our constructor
	def __init__(self, username, email):
		self.username = username
		self.email = email
'''

# Defining the table that is gonna be a backbone in setting Havanao USSD 
# The queries from havanao hit our server independently, they are not concatenated
# This database will help us concatenate it and handle concurrency access of
# various users

class IncomingText(Base):

	# Defining our table
	__tablename__ = "incoming_text"

	# Defining our columns in this table	
	id = Column('text_id', Integer, primary_key=True)
	inputuser = Column(String(30), nullable=False)
	session_id = Column(String(30), nullable=False)
	phonenumber = Column(String(30), nullable=False, unique=True)
	servicecode = Column(String(30))

	# Defining our constructor
	def __init__(self, inputuser, session_id, phonenumber, servicecode):
		self.inputuser = inputuser
		self.session_id = session_id
		self.phonenumber = phonenumber
		self.servicecode = servicecode

Base.metadata.create_all(engine)










'''
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

'''

