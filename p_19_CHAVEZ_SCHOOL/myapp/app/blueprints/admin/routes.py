#from app.models.user import User 
#from app.models.tutoring import Tutoring
#from app.models.subject import Subject

from flask import current_app

import jwt

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask import render_template, flash, redirect, url_for
from flask_login import logout_user, login_required, current_user
from functools import wraps
from flask_login import login_user
from app import login_manager
from . import admin_bp
from ... import db  
from werkzeug.security import generate_password_hash


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField






''' 
DECORATORS: 
'''
# The admin_required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function



'''

FLASK LOGIN


'''

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User  # Adjust the import statement based on your project structure
    return User.query.get(int(user_id))

'''
LOGGING IN USING OUR JINJA TEMPLATES , FLASK FORMS AND 
ADMIN BLUEPRINT ROUTES

'''

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
# the login route


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    from app.models.user import User  # Adjust the import statement based on your project structure
    print("Hi there")
    print(db)
    form = AdminLoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(role='admin', username=form.username.data).first()  # Adjusted to User
        if user and user.check_password(form.password.data):  # Adjusted to user
            login_user(user)  # Adjusted to user
            
            # Create a JWT
            secret_key = current_app.config['SECRET_KEY']  # Use the secret key from your app's config
            payload = {
                'username': user.username,  # Adjusted to user
                'data': 99713  # Any additional data you want to include
            }
            token = jwt.encode(payload, secret_key, algorithm='HS256')
            
            # Redirect to the dashboard route with the token as a parameter
            return redirect(url_for('admin.dashboard', token=token,secret_key=secret_key))
        #Note that you don't really want to pass the key, this is just for
        #testing
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@admin_bp.route('/logout')
@login_required
@admin_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))


'''

DASHBOARD

'''
#@admin_bp.route('/dashboard', methods=['GET'])
#@login_required
#@admin_required
#def dashboard(token,secretKey):
#    return render_template('dashboard.html', token=token,secret_key=secretKey)

@admin_bp.route('/dashboard/<token>/<secret_key>', methods=['GET'])
@login_required
@admin_required
def dashboard(token, secret_key):
    return render_template('dashboard.html', token=token, secret_key=secret_key)

# 
# STUDENT ROUTES#
#

class StudentForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password_hash = StringField('Password', validators = [DataRequired()])
    submit = SubmitField('Add Student')

@admin_bp.route('/add_student', methods=['GET', 'POST'])
@login_required
@admin_required
def add_student():
    from app.models.user import User  # Adjust the import statement based on your project structure
    form = StudentForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password_hash.data, method='sha256')
        student = User(username=form.username.data,\
                      email=form.email.data,\
                      password_hash=hashed_password,\
                      role='student')
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!')
        return redirect(url_for('admin.dashboard'))
    return render_template('add_student.html', form=form)

# Create Student/Tutor Relationship


# Model for the Tutoring Relationship, keeping here for the time being: 
#class Subject(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(64), unique=True, nullable=False)
#

class TutoringForm(FlaskForm):
    student = QuerySelectField('Student', query_factory=lambda: User.query.filter_by(role='student'), get_label='username')
    tutor = QuerySelectField('Tutor', query_factory=lambda: User.query.filter_by(role='tutor'), get_label='username')
    subject = QuerySelectField('Subject', query_factory=lambda: Subject.query.all(), get_label='name')
    submit = SubmitField('Add Relationship')


@admin_bp.route('/add_tutoring', methods=['GET', 'POST'])
@login_required
@admin_required
def add_tutoring():
    from app.models.user import User  # Adjust the import statement based on your project structure
    form = TutoringForm()
    if form.validate_on_submit():
        tutoring = Tutoring(student_id=form.student.data.id, tutor_id=form.tutor.data.id, subject_id=form.subject.data.id)
        db.session.add(tutoring)
        db.session.commit()
        flash('Tutoring relationship added successfully!')
        return redirect(url_for('admin.dashboard'))
    return render_template('add_tutoring.html', form=form)




# This in its current form does not make sense as the user has not submitted
# any data yet ... so nothing renders and there's some sort of message too. 
#def add_student():
#if form.validate_on_submit():
#    existing_user = Student.query.filter_by(username=form.username.data).first()
#    if existing_user:
#        flash('A student with that username already exists. Please choose a different username.')
#        return redirect(url_for('admin.add_student'))
#    
#    hashed_password = generate_password_hash(form.password.data)
#    student = User(
#        username=form.username.data,
#        email=form.email.data,
#        password_hash=hashed_password,
#        role='student'
#    )
#    db.session.add(student)
#    db.session.commit()
#    flash('Student added successfully!')
#    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/view_all_students', methods=['GET', 'POST'])
@login_required
@admin_required
def view_all_students():
    from app.models.user import User  # Adjust the import statement based on your project structure
    students = User.query.filter_by(role='student').all()
    return render_template('view_all_students.html', students=students)

@admin_bp.route('/view_student', methods=['GET', 'POST'])
@login_required
@admin_required
def view_student():
    from app.models.user import User  # Adjust the import statement based on your project structure
    ''' 
    Needs to be changed so that it just views the students. Maybe should return
    a table if the admin is logged in and just let them select based on some
    other logic. 
    '''
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(username=form.username.data, email=form.email.data, password= form.password.data, role=form.role.data)
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!')
        return redirect(url_for('admin.dashboard'))
    return render_template('add_student.html', form=form)

@admin_bp.route('/update_student', methods=['GET', 'POST'])
@login_required
@admin_required
def update_student():
    from app.models.user import User  # Adjust the import statement based on your project structure
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(username=form.username.data, email=form.email.data)
        # ... set other fields
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!')
        return redirect(url_for('admin.dashboard'))
    return render_template('add_student.html', form=form)


'''
WORKING WITH STAFF
'''

class StaffForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password_hash = StringField('Password', validators = [DataRequired()])
    submit = SubmitField('Add Staff')

@admin_bp.route('/add_staff', methods=['GET', 'POST'])
@login_required
@admin_required
def add_staff():
    from app.models.user import User  # Adjust the import statement based on your project structure
    form = StaffForm()
    if form.validate_on_submit():
        # Create an instance of User model with role set to 'Staff'
        hashed_password = generate_password_hash(form.password_hash.data, method='sha256')
        user = User(username=form.username.data,\
                email=form.email.data,\
                password_hash=hashed_password,\
                role='Staff')
        db.session.add(user)
        db.session.commit()
        flash('Staff added successfully!')
        return redirect(url_for('admin.dashboard'))
    return render_template('add_staff.html', form=form)

@admin_bp.route('/view_staff', methods=['GET', 'POST'])
@login_required
@admin_required
def view_staff():
    form = StaffForm()
    if form.validate_on_submit():
        staff = StaffForm(username=form.username.data, email=form.email.data)
        db.session.add(student)
        db.session.commit()
        flash('Staff added successfully!')
        return redirect(url_for('admin.dashboard'))
    return render_template('add_staff.html', form=form)


@admin_bp.route('/view_all_stafff', methods=['GET', 'POST'])
@login_required
@admin_required
def view_all_staff():
    from app.models.user import User  # Adjust the import statement based on your project structure
    staff = User.query.filter_by(role='Staff').all()
    return render_template('view_all_staff.html', staff=staff)







#ROUTES FOR SESSIONS: Creating the sessions, Finding Old Sessions, Loading the
# whiteboards for the old sessions etc





# Remember the idea is that you simply find the database connection for the
# current user, i.e.



### ROUTES FOR THE QUIZZES/RELATED ENDPOINTS
#from models.question_models import *
#
## Initialize a session
#session = Session()
#
#def add_question_routes(app):
#
#    @app.route('/add_question', methods=['POST'])
#    def add_question():
#        try:
#            # Get form data
#            question_text = request.form.get('question')
#            topic = request.form.get('topic')
#            answers = request.form.getlist('answers')
#            correct_index = int(request.form.get('correct_index'))
#
#            # Create a new question
#            new_question = Question(text=question_text, topic=topic)
#            
#            # Add answers
#            for i, answer_text in enumerate(answers):
#                is_correct = (i == correct_index)
#                new_answer = Answer(text=answer_text, is_correct=is_correct, topic=topic, question=new_question)
#                session.add(new_answer)
#
#            # Add question to session and commit
#            session.add(new_question)
#            session.commit()
#
#            return jsonify({"status": "success", "message": "Question and answers added successfully"}), 200
#
#        except Exception as e:
#            return jsonify({"status": "error", "message": str(e)}), 400
#
