import os
import unittest
from app import db, app


DBUSER = 'ussd'
DBPASS = '123456'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'ussd_db'

 
class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.secret_key = '123456'

        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
 
    # executed after each test
    def tearDown(self):
        pass
 
 
###############
#### tests ####
###############
 
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
 
 
if __name__ == "__main__":
    unittest.main()