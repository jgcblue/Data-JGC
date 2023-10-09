# app/staff/__init__.py

from flask import Blueprint

student = Blueprint('student', __name__)

from . import routes

