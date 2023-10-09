class StaffForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    # ... other fields
    submit = SubmitField('Add Student')

@admin_bp.route('/add_staff', methods=['GET', 'POST'])
@login_required
@admin_required
def add_student():
    form = StaffForm()
    if form.validate_on_submit():
        staff = StaffForm(username=form.username.data, email=form.email.data)
        # ... set other fields
        db.session.add(student)
        db.session.commit()
        flash('Staff added successfully!')
        return redirect(url_for('admin.dashboard'))
    return render_template('add_staff.html', form=form)



