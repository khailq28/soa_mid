from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_jwt_extended import JWTManager

# for session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "test"
  
#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/ibanking'
                                        #mysql+pymysql://username:passwd@host/databasename 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'a06204995@gmail.com'
app.config['MAIL_PASSWORD'] = 'Testemail123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# app.config['JWT_TOKEN_LOCATION'] = ['cookies', 'headers']
app.config['JWT_TOKEN_LOCATION'] = ['headers']
# app.config['JWT_COOKIE_SECURE'] = False
# app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
# app.config['JWT_REFRESH_COOKIE_PATH'] = '/refresh'
# app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_SECRET_KEY'] = 'aaaaaasdfdsf'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

app.permanent_session_lifetime = timedelta(hours=1)

jwt = JWTManager(app)

mail = Mail(app)
bootstrap = Bootstrap(app)

db = SQLAlchemy(app)
