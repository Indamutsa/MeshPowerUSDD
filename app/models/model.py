#Importing libraries and entities that we will need to use later
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.pool import QueuePool, StaticPool, NullPoll


# Define our engine that will help us connect to the database || You can add echo=True
# within create engine to echo any query make to the database (engine = create_engine('postgresql://ussd:123456@db:5432/ussd_db, echo=True')
engine = create_engine('postgresql://ussd:123456@db:5432/ussd_db', pool_size=100, max_overflow=0)

#Defining a base class stores a catlog of classes and mapped tables
Base = declarative_base()


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


# Defining the table that is gonna be a backbone in setting Havanao USSD 
# The queries from havanao hit our server independently, they are not concatenated
# This database will help us concatenate it and handle concurrency access of
# various users

class IncomingText(Base):

    # Defining our table
    __tablename__ = "incoming_text"

    # Defining our columns in this table        
    id = Column('text_id', Integer, primary_key=True)
    inputuser = Column(String, nullable=False)
    session_id = Column(String, nullable=False)
    phonenumber = Column(String, nullable=False, unique=True)
    servicecode = Column(String)

    # Defining our constructor
    def __init__(self, inputuser, session_id, phonenumber, servicecode):
        self.inputuser = inputuser
        self.session_id = session_id
        self.phonenumber = phonenumber
        self.servicecode = servicecode

class ServiceApplication(Base):

    # Defining our table
    __tablename__ = "service_application"

    # Defining our columns in this table
    id = Column('text_id', Integer, primary_key=True)
    sector = Column(String, nullable=False)
    district = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phonenumber = Column(String, nullable=False)

    # Defining our constructor def __init__(self, village, cell, sector, district, province, phonenumber):
    def __init__(self, sector, district, name, phonenumber):
        self.sector = sector
        self.district = district
        self.name = name
        self.phonenumber = phonenumber

class IssueReport(Base):

    # Defining our table
    __tablename__ = "issue_report"

    #Defining our columns in this table
    id = Column('text_id', Integer, primary_key=True)
    account = Column(String(30), nullable=False)
    phonenumber = Column(String(30), nullable=False)
    issue = Column(String, nullable=False)

    # Defining our constructor
    def __init__(self, account, phonenumber, issue):
        self.account = account
        self.phonenumber = phonenumber
        self.issue = issue


Base.metadata.create_all(engine)
