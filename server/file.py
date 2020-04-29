from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

from models import User, ForumComment
from __init__ import db, app

file = Blueprint('file', __name__)

@file.route('/uploader', methods=['POST'])
def uploader():
    payload = request.get_json()
    filename = payload.get('filename')
    file = payload.get('file')
    g_sensor_file = payload.get('g_sensor_file')
    g_sensor_filename = payload.get('g_sensor_filename')
    accident_time = payload.get('accident_time')
    car_or_motor = payload.get('car_or_motor')
    object_hit = payload.get('object_hit')
    country = payload.get('country')
    description = payload.get('description')

    if file:
        file.save(os.path.join(app.config['UPLOAD_ROOT'], filename=filename))