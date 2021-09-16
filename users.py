from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    time = db.Column(db.String)
    
    def __init__(self,user_name,email,password,time):
        self.user_name = user_name
        self.email = email
        self.password = self.create_password_hash(password)
        self.time = time
    
    def __repr__(self):
        return '<User %r>' % self.user_name
        
    def create_password_hash(self,password):
        return generate_password_hash(password,method="sha256")
    
    
    def check_password(self,password):
        return check_password_hash(self.password,password)
    
    
    
def create_schema():
    db.drop_all()
    db.create_all()

def insert(new_user):
    db.session.add(new_user)
    db.session.commit()


def validar_user(user_name):
    user_query = User.query.filter_by(user_name=user_name).first()
    return user_query

def validar_email(email):
    user_mail = User.query.filter_by(email=email).first()
    return user_mail

def user_id(user_id):
    return User.query.get(int(user_id))