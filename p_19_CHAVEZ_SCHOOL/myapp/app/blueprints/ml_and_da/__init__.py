# app/staff/__init__.py

from flask import Blueprint

mlda_bp = Blueprint('ml_and_da', __name__)

from . import routes


