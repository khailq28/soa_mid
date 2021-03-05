from flask_sqlalchemy import SQLAlchemy
from init import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    name = db.Column(db.String(100))
    student_id = db.Column(db.String(8))
    phone_number = db.Column(db.String(10))
    money = db.Column(db.String(255))
  
    def __init__(self, username, email, password, name, student_id, phone_number, money):
        self.username = username
        self.email = email
        self.password = password
        self.name = name
        self.student_id = student_id
        self.phone_number = phone_number
        self.money = money

class UserSchema():
    class Meta:
        model = User

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tuition_id = db.Column(db.Integer)
    date_of_payment = db.Column(db.String(20))
    submitter_id =  db.Column(db.Integer)
    receiver_id = db.Column(db.Integer)
    semester = db.Column(db.String(100))
    
    def __init__(self, tuition_id, date_of_payment, submitter_id, receiver_id, semester):
        self.tuition_id = tuition_id
        self.date_of_payment = date_of_payment
        self.submitter_id = submitter_id
        self.receiver_id = receiver_id
        self.semester = semester

class Tuition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    semester = db.Column(db.String(100))
    semester_tuition = db.Column(db.String(50))
    reduction = db.Column(db.String(50))
    note = db.Column(db.String(50))

    def __init__(self, user_id, semester, semester_tuition, reduction, note):
        self.user_id = user_id
        self.semester = semester
        self.semester_tuition = semester_tuition
        self.reduction = reduction
        self.note = note