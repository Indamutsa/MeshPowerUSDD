import time
from flask import Flask, render_template, flash, redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD

DBUSER = 'ussd'
DBPASS = '123456'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'ussd_db'
=======
from MeshPower.app.config import AppConfig
>>>>>>> master


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user= AppConfig.DBUSER,
        passwd=AppConfig.DBPASS,
        host=AppConfig.DBHOST,
        port=AppConfig.DBPORT,
        db=AppConfig.DBNAME)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = AppConfig.SECRET_KEY

#This fb contains app instance, when it is invoked it has all app context with it regarding the db
db = SQLAlchemy(app)


class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))

    def __init__(self, name, city, addr):
        self.name = name
        self.city = city
        self.addr = addr

class User(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(50))

    def __init__(self, username, email):
        self.username = username
        self.email = email


class Customer(db.Model):
   # __tablename__ = "customers"
    id = db.Column('customer_id', db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    account_no = db.Column(db.String(20))
    phone_no = db.Column(db.String(20))
    site = db.Column(db.String(100))
    balance = db.Column(db.Integer)
    tarrif = db.Column(db.String(50))

    def __init__(self,fullname,phone_no,account_no,site,tarrif):
        self.fullname = fullname
        self.account_no = account_no
        self.phone_no = phone_no
        self.site = site
        self.balance = 10000
        self.tarrif = tarrif

class Consumption(db.Model):
   # __tablename__ = "consumption"
    id = db.Column('consumption_id',db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer)
    amount = db.Column(db.Integer)

    def __init__(self,customer_id,amount,date_created):
        self.customer_id =customer_id
        self.amount = amount
        self.date_created = date_created


class TopUp(db.Model):
  #  __tablename__ = "topup"
    id = db.Column('topup_id',db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer)
    amount = db.Column(db.Integer)

    def __init__(self,customer_id,amount,date_created):
        self.customer_id =customer_id
        self.amount = amount
        self.date_created = date_created


class Complaint(db.Model):
  #  __tablename__ = "complaint"
    id = db.Column('complaint_id',db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer)
    description = db.Column(db.String(100))
    category = db.Column(db.String(50))

    def __init__(self,customer_id,category, description,date_created):
        self.customer_id =customer_id
        self.category = category
        self.description = description
        self.date_created = date_created



class Site(db.Model):
   # __tablename__ = "site"
    id = db.Column('site_id',db.Integer, primary_key=True)
    site_name = db.Column(db.String(100))
    district = db.Column(db.String(100))
    sector = db.Column(db.String(100))

    def __init__(self,site_name,district,sector):
        self.site_name =site_name
        self.district = district
        self.sector = sector


class Application(db.Model):
 #   __tablename__ = "application"
    id = db.Column('application_id',db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    district = db.Column(db.String(100))
    sector = db.Column(db.String(100))
    site = db.Column(db.String(100))
    distance = db.Column(db.Integer)

    def __init__(self,fullname,district,sector, site, distance):
        self.fullname = fullname
        self.district = district
        self.sector = sector
        self.site = site 
        self.distance = distance


def database_initialization():
    db.create_all()
    test_rec = students(
            'John Doe',
            'Los Angeles',
            '123 Foobar Ave')

    db.session.add(test_rec)
    db.session.rollback()
    db.session.commit()

    # Adding dummy customer, site data

    customer1 = Customer("Ivan","078405151","101","Kigali","3 LED")
    customer2 = Customer("Arsene","078405151","102","Kigali","3 LED")
    customer3 = Customer("Leandre","078405151","103","Kigali","3 LED")
    db.session.add(customer1)
    db.session.commit()
    db.session.add(customer2)
    db.session.commit()
    db.session.add(customer3)
    db.session.commit()
    

    


@app.route('/', methods=['GET', 'POST'])
def index():

    data = request.get_json()
    username = data["username"]
    email = data["email"]

    user = User(username, email)
    db.session.add(user)
    db.session.commit()

    db_data = User.query.all()

    for name_user in db_data:
        print("======>:  " + name_user.username)



    # student = students(
    #         request.form['name'],
    #         request.form['city'],
    #         request.form['addr'])

    # db.session.add(student)
    # db.session.commit()
    return  jsonify({"username": name_user.username, "email": name_user.email})


if __name__ == '__main__':
    dbstatus = False
    while dbstatus == False:
        try:
            db.create_all()
        except:
            time.sleep(2)
        else:
            dbstatus = True
    database_initialization()
    app.run(debug=True, host='0.0.0.0')
