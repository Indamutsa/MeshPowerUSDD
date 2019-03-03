from app import db


class User(db.Model):
   # __tablename__ = "user_info"
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(50))

    def __init__(self, username, email):
        self.username = username
        self.email = email
