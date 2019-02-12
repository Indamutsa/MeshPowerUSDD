import time
from flask import Flask, render_template, flash, redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy


DBUSER = 'ussd'
DBPASS = '123456'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'ussd_db'


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '123456'

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



def database_initialization():
    db.create_all()
    test_rec = students(
            'John Doe',
            'Los Angeles',
            '123 Foobar Ave')

    db.session.add(test_rec)
    db.session.rollback()
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
