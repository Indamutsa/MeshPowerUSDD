from app_ussd import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column('student_id', db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(50))

    def __init__(self, username, email):
        self.username = username
        self.email = email
