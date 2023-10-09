#routes for staff

from app.models.user import User
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask import render_template, flash, redirect, url_for
from flask_login import logout_user

from . import staff
from ... import db  


## DECORATORS START


from flask_login import login_required
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'staff':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function
## DECORATORS END




class staffLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


@staff.route('/dashboard')
@login_required
@staff_required
def staff_dashboard():
    return "Welcome to the staff dashboard!"



class StudentForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    # ... other fields
    submit = SubmitField('Add Student')

@staff.route('/add_student', methods=['GET', 'POST'])
@login_required
@staff_required
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(username=form.username.data, email=form.email.data)
        # ... set other fields
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!')
        return redirect(url_for('staff.dashboard'))
    return render_template('add_student.html', form=form)

@staff.route('/view_student', methods=['GET', 'POST'])
@login_required
@staff_required
def view_student():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(username=form.username.data, email=form.email.data)
        # ... set other fields
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!')
        return redirect(url_for('staff.dashboard'))
    return render_template('add_student.html', form=form)

@staff.route('/update_student', methods=['GET', 'POST'])
@login_required
@staff_required
def update_student():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(username=form.username.data, email=form.email.data)
        # ... set other fields
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!')
        return redirect(url_for('staff.dashboard'))
    return render_template('add_student.html', form=form)


