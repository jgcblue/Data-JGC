from flask import current_app,request, jsonify
import json 
import jwt
import pickle
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask import render_template, flash, redirect, url_for
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


from flask_cors import CORS  # Import the CORS package


from flask import Flask, request

from datetime import datetime

@admin_bp.route('/dashboard', methods=['GET','POST'])
def dashboard():
    # there's a point here that's kinda confusing 
    # Need to get the secret_key? 
    return render_template('dashboard.html')

@admin_bp.route('/create_session', methods=['POST'])
def create_session():
    user_id = request.json.get('user_id')
    session_data = request.json.get('session_data')
    new_session = Session(user_id=user_id, session_data=session_data)
    db.session.add(new_session)
    db.session.commit()
    return jsonify({"session_id": new_session.id}), 201

@admin_bp.route('/update_session/<int:session_id>', methods=['PUT'])
def update_session(session_id):
    session = Session.query.get_or_404(session_id)
    session_data = request.json.get('session_data')
    session.session_data = session_data
    db.session.commit()
    return jsonify({"message": "Session updated successfully"}), 200




@admin_bp.route('/save_canvas_data', methods=['POST'])
#Notice that there's no protection right now. 
def save_canvas_data():
    # Lazy loading of the models again...
    print(request)
    from app.models.user import Session  # Adjust the import statement based on your project structure
    dataList = request.json.get('elements')
    # First dump the list then we will dump the object inside. 
    # there's only one object in there. 
    with open('saved_object.pkl', 'wb') as f:
            pickle.dump(dataList, f)
    print(len(dataList))
    dataD=dataList[0]
    # Finally jsonify the dictionary so that we can store it in the database. 
    dataJson=json.dumps(dataD)

    print(type(dataList))
    # Create a new session instance and store the received canvas data
    session = Session(start_datetime=datetime.utcnow(),canvas_data=dataJson)  # Directly assigning JSON data
    db.session.add(session)
    db.session.commit()
    #return jsonify({'message': 'Data saved successfully', 'session_id': session.id})
    return jsonify({"message": "End of save_canvas_data"}), 200
    

