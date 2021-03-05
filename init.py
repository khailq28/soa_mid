from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail

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

app.permanent_session_lifetime = timedelta(minutes=5)

mail = Mail(app)
bootstrap = Bootstrap(app)

db = SQLAlchemy(app)
