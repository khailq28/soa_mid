from flask import Blueprint, jsonify, request, json, session, abort

from models import *
from flask_mail import Message
from init import mail, db
from flask_jwt_extended import get_jwt_identity, jwt_required

import random
from datetime import datetime

api = Blueprint('api', __name__, static_folder='static', template_folder='templates')

#Functions
#get semester by student id
def get_semester(sStudentId):
    # semesters = Tuition.query.distinct(Tuition.semester).filter(Tuition.user_id == iId)
    semesters = Tuition.query.join(User, Tuition.user_id == User.id).\
                            with_entities(Tuition.semester).\
                            filter(User.student_id == sStudentId)
    return semesters

#get tuition by student id and semester
def get_tuition(sStuId, sSemester):
    return Tuition.query.join(User, Tuition.user_id == User.id).\
                        with_entities(Tuition.id, Tuition.semester_tuition, Tuition.reduction, Tuition.note).\
                            filter(Tuition.semester == sSemester, User.student_id == sStuId).first()

#get info by studentId
def get_user_info(sStuId):
    return User.query.with_entities(User.name, User.phone_number, User.email).filter(User.student_id == sStuId).first()

@api.route('/get_user_data', methods=['POST'])
@jwt_required()
def getUserData():
    sUsername = get_jwt_identity()

    new_user = User.query.\
        with_entities(User.student_id, User.name, User.phone_number, User.email, User.money).\
            filter(User.username == sUsername).first()

    new_history = History.query.join(Tuition, History.tuition_id == Tuition.id).\
                    with_entities(History.date_of_payment, Tuition.semester_tuition, Tuition.reduction, Tuition.semester, History.submitter_id).\
                        filter(History.receiver_id == new_user.student_id).all()
    history_output = []
    for obj in new_history:
        name = User.query.with_entities(User.name).filter(User.student_id == obj.submitter_id).first()
        history_output.append({
            'semester': obj.semester,
            'date_of_payment': obj.date_of_payment,
            'semester_tuition': obj.semester_tuition,
            'reduction': obj.reduction,
            'submitter_id': obj.submitter_id,
            'name': name.name
        })
    
    return jsonify(
       studentId = new_user.student_id,
       name = new_user.name,
       phone_number = new_user.phone_number,
       email = new_user.email,
       money = new_user.money,
       history = history_output
    ), 200

@api.route('/get_semester', methods=['POST'])
@jwt_required()
def getSemester():
    sStudentId = request.form['studentId']

    #save the searched student 
    if 'search_student_id' in session:
        session.pop('search_student_id', None)
    session['search_student_id'] = sStudentId

    aSemesters = []
    for sSemester in get_semester(sStudentId):
        aSemesters.append(sSemester.semester)
    
    aInfo = []
    info = get_user_info(sStudentId)
    if info:
        aInfo.append({
            'name' : info.name,
            'phone_number' : info.phone_number,
            'email' : info.email,
        })

    if 'search_student_email' in session:
        session.pop('search_student_email', None)
    session['search_student_email'] = info.email

    if not aSemesters:
        return jsonify(
            error = 'Student ID is invalid'
        ), 200
        
    return jsonify(
        semesters = aSemesters,
        info = aInfo
    ), 200

@api.route('/get_tuition', methods=['POST'])
@jwt_required()
def getTuition():
    session.pop('semester', None)
    session['semester'] = request.form['semester']

    sStudentId = request.form['studentId']
    sSemester = request.form['semester']

    tuition = get_tuition(sStudentId, sSemester)
    #save the tuition id
    if 'tuition_id' in session:
        session.pop('tuition_id', None)
    session['tuition_id'] = tuition.id

    data = []
    data.append(
        {
            'semester_tuition' : tuition.semester_tuition,
            'reduction' : tuition.reduction,
            'note' : tuition.note
        }
    )

    if not data:
        return jsonify(
            error = 'Error'
        )

    return jsonify(
        tuition = data
    ), 200

@api.route('/get_otp', methods=['POST'])
@jwt_required()
def getOtp():
    if 'otp' in session:
        session.pop('otp', None)
    otp = random.randrange(100000, 1000000)
    #save in session
    session['otp'] = otp

    new_user = User.query.with_entities(User.email).filter(User.username == get_jwt_identity()).first()

    msg = Message('Confirm payment', sender = 'a06204995@gmail.com', recipients = [new_user.email])
    msg.body = 'OTP: ' + str(otp)
    mail.send(msg)

    return 'OTP is sent to your email!', 200

@api.route('/payment', methods=['POST'])
@jwt_required()
def payment():
    pStudId = request.form['pStudId']
    rStudId = request.form['rStudId']
    semester = request.form['semester']
    otp = request.form['otp']

    new_user = User.query.filter(User.username == get_jwt_identity()).first()

    new_tuition = get_tuition(rStudId, semester)
    total_tuition = int(new_tuition.semester_tuition) - int(new_tuition.reduction)

    if total_tuition >= int(new_user.money):
        return jsonify(
            message = 'Your account does not have enough money!'
        ), 200

    if otp == '' or not 'otp' in session:
        return jsonify(
            message = 'Invalid OTP'
        ), 200

    if str(otp) == str(session['otp']):
        session.pop('otp', None)
        if pStudId != new_user.student_id or rStudId != session['search_student_id'] or semester != session['semester']:
            return jsonify(
                message = 'error'
            ), 200

        # datetime object containing current date and time
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        new_history = History(session['tuition_id'], dt_string, pStudId, rStudId, semester)
        db.session.add(new_history)

        tuition_update = Tuition.query.\
            filter(Tuition.id == session['tuition_id'], Tuition.semester == semester).\
                update(dict(note='COMPLETED'))

        new_user_money = int(new_user.money) - (total_tuition)
        user_update = User.query.\
                        filter(User.id == new_user.id).\
                            update(dict(money = str(new_user_money)))

        db.session.commit()

        msg = Message('Payment success', sender = 'a06204995@gmail.com', recipients = [new_user.email])
        msg.body = 'Student ID: ' + rStudId + \
                    '\nSemester: ' + semester +  \
                    '\nTotal tuition paid: ' + str(total_tuition) + \
                    '\nStudent Id of payer: ' + new_user.student_id
        mail.send(msg)

        if new_user.email != session['search_student_email']:
            msg = Message('Payment success', sender = 'a06204995@gmail.com', recipients = [session['search_student_email']])
            msg.body = 'Student ID: ' + rStudId + \
                        '\nSemester: ' + semester +  \
                        '\nTotal tuition paid: ' + str(total_tuition) + \
                        '\nStudent Id of payer: ' + new_user.student_id
            mail.send(msg)

        return jsonify(
            message = 'Payment success'
        ), 200
    else:
        return jsonify(
            message = 'Invalid OTP'
        ), 200