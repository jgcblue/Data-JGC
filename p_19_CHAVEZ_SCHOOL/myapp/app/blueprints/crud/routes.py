#CRUD routes.py
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from functools import wraps

from app.blueprints.crud import crud_bp

from app.models.user import User
from app.database import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Decorator to ensure the user is an admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

# Sample form for adding a student
class StudentForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Add Student')

@crud_bp.route('/students', methods=['GET', 'POST'])
@login_required
@admin_required
def list_students():
    students = User.query.filter_by(role='student').all()
    return render_template('students.html', students=students)

@crud_bp.route('/student/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(username=form.username.data, email=form.email.data)
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!')
        return redirect(url_for('crud.list_students'))
    return render_template('add_student.html', form=form)

@crud_bp.route('/student/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_student(id):
    student = User.query.filter_by(role='student').get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.username = form.username.data
        student.email = form.email.data
        db.session.commit()
        flash('Student updated successfully!')
        return redirect(url_for('crud.list_students'))
    return render_template('edit_student.html', form=form, student=student)

@crud_bp.route('/student/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_student(id):
    student = User.query.filter_by(role='student').get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!')
    return redirect(url_for('crud.list_students'))

