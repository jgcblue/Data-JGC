from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from functools import wraps

from . import mlda_bp

# Decorator to ensure the user is an admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@mlda_bp.route('/')
@login_required
@admin_required
def index():
    return "Welcome to the Machine Learning and Data Analysis section!"

@mlda_bp.route('/data_visualization')
@login_required
@admin_required
def data_visualization():
    # Placeholder
    pass

@mlda_bp.route('/predictive_modeling')
@login_required
@admin_required
def predictive_modeling():
    # Placeholder
    pass

@mlda_bp.route('/data_cleaning')
@login_required
@admin_required
def data_cleaning():
    # Placeholder
    pass

@mlda_bp.route('/advanced_analysis')
@login_required
@admin_required
def advanced_analysis():
    # Placeholder
    pass

@mlda_bp.route('/report_generation')
@login_required
@admin_required
def report_generation():
    # Placeholder
    pass

