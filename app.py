from flask import render_template, redirect, url_for, flash, jsonify, request
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    set_access_cookies, set_refresh_cookies,
     jwt_required,
    get_jwt_identity, unset_jwt_cookies
)

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from init import app, db
from models import *

from api.api import api

app.register_blueprint(api, url_prefix='/api')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=6, max=15, message="Username should be between 6-15 characters!")])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=15, message="Password should be between 8-15 characters!")])

#Routes
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)

                access_token = create_access_token(identity=username)
                # refresh_token = create_refresh_token(identity=username)
                resp = jsonify({
                    'login': True,
                    'token': access_token
                })
                # set_access_cookies(resp, access_token)
                # set_refresh_cookies(resp, refresh_token)
                return resp, 200
        #error
        return jsonify(message = 'Invalid username or password')

    return render_template('login.html', form=form)

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    resp = jsonify({'logout': True})
    # unset_jwt_cookies(resp)
    return resp, 200

if __name__ == "__main__":
    app.run(debug=True)