# Importing the flask class
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


#----------------------------------- Extesnsions  -------------------------------------------

#The database we are using here
db = SQLAlchemy()



#-------------------------------------------  The function that creates our app ------------------------------------------------------------

def create_app():
	# ---------------------


	app = Flask(__name__)

	app.config['SQLALCHEMY_DATABASE_URI'] = \
	    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
	        user=os.environ.get('DBUSER'),
	        passwd=os.environ.get('DBPASS'),
	        host=os.environ.get('DBHOST'),
	        db=os.environ.get('DBNAME')

	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.secret_key = '123456'

	# -----------------------

	db.init_app(app)

	return app

