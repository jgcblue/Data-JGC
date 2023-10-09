
import jwt
from flask import current_app, render_template
from flask_login import login_required, current_user
from . import admin_bp  # or your appropriate import for admin_bp

@admin_bp.route('/dashboard')
@login_required
# @admin_required  # Uncomment this if you have this decorator defined
def dashboard():
    # ... other code ...
    
    # Access the secret key from app's configuration
    secret_key = current_app.config.get('SECRET_KEY')
    
    # Create a JWT
    payload = {
        'username': current_user.username,
        'data': 99713
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    
    return render_template('dashboard.html', token=token)

