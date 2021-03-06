from flask import Blueprint, jsonify, request, json, session, abort

from models import *
from flask_login import current_user, login_required
from flask_mail import Message
from init import mail, db

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

@api.route('/get_user_data')
@login_required
def getUserData():
    new_history = History.query.join(Tuition, History.tuition_id == Tuition.id).\
                        with_entities(History.date_of_payment, Tuition.semester_tuition, Tuition.reduction, Tuition.semester, History.submitter_id).\
                            filter(History.receiver_id == current_user.student_id).all()
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
       studentId = current_user.student_id,
       name = current_user.name,
       phone_number = current_user.phone_number,
       email = current_user.email,
       money = current_user.money,
       history = history_output
   )

@api.route('/get_semester', methods=['POST'])
def getSemester():
    if request.method == 'POST' and 'studentId' in request.form:
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
            )
            
        return jsonify(
            semesters = aSemesters,
            info = aInfo
        )

@api.route('/get_tuition', methods=['POST'])
def getTuition():
    if request.method == 'POST' and 'studentId' in request.form and 'semester' in request.form:
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
        )

@api.route('/get_otp', methods=['POST'])
def getOtp():
    if 'otp' in session:
        session.pop('otp', None)
    otp = random.randrange(100000, 1000000)
    #save in session
    session['otp'] = otp

    msg = Message('Confirm payment', sender = 'a06204995@gmail.com', recipients = [current_user.email])
    msg.body = 'OTP: ' + str(otp)
    mail.send(msg)

    return 'OTP is sent to your email!'

@api.route('/test')
def test():
    return session['semester']

@api.route('/payment', methods=['POST'])
def payment():
    pStudId = request.form['pStudId']
    rStudId = request.form['rStudId']
    semester = request.form['semester']
    otp = request.form['otp']

    new_tuition = get_tuition(rStudId, semester)
    total_tuition = int(new_tuition.semester_tuition) - int(new_tuition.reduction)

    if total_tuition >= int(current_user.money):
        return jsonify(
            message = 'Your account does not have enough money!'
        )

    if otp == '' or not 'otp' in session:
        return jsonify(
            message = 'Invalid OTP'
        )

    if str(otp) == str(session['otp']):
        session.pop('otp', None)
        if pStudId != current_user.student_id or rStudId != session['search_student_id'] or semester != session['semester']:
            return jsonify(
                message = 'error'
            )

        # datetime object containing current date and time
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        new_history = History(session['tuition_id'], dt_string, pStudId, rStudId, semester)
        db.session.add(new_history)

        tuition_update = Tuition.query.\
            filter(Tuition.id == session['tuition_id'], Tuition.semester == semester).\
                update(dict(note='COMPLETED'))

        new_user_money = int(current_user.money) - (total_tuition)
        user_update = User.query.\
                        filter(User.id == current_user.id).\
                            update(dict(money = str(new_user_money)))

        db.session.commit()

        msg = Message('Payment success', sender = 'a06204995@gmail.com', recipients = [current_user.email])
        msg.body = 'Student ID: ' + rStudId + \
                    '\nSemester: ' + semester +  \
                    '\nTotal tuition paid: ' + str(total_tuition) + \
                    '\nStudent Id of payer: ' + current_user.student_id
        mail.send(msg)

        if current_user.email != session['search_student_email']:
            msg = Message('Payment success', sender = 'a06204995@gmail.com', recipients = [session['search_student_email']])
            msg.body = 'Student ID: ' + rStudId + \
                        '\nSemester: ' + semester +  \
                        '\nTotal tuition paid: ' + str(total_tuition) + \
                        '\nStudent Id of payer: ' + current_user.student_id
            mail.send(msg)

        return jsonify(
            message = 'Payment success'
        )   
    else:
        return jsonify(
            message = 'Invalid OTP'
        )

