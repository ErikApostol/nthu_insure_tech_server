from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import hashlib

from models import User, UploadFile
from __init__ import db

file = Blueprint('file', __name__)

UPLOAD_FOLDER = 'E:\\nthu_insure_tech_server\\server\\upload'


def sha_filename(filename):
    hash_name = filename.split('.')
    hash_name[0] = hashlib.sha256(filename.split('.')[0].encode('utf-8')).hexdigest()
    hash_name = '.'.join(hash_name)

    return hash_name


@file.route('/uploader', methods=['POST'])
@login_required
def uploader():
    file = request.files['file']
    filename = file.filename
    hash_filename = sha_filename(filename)
    g_sensor_file = request.files['g_sensor_file']
    g_sensor_filename = g_sensor_file.filename
    hash_g_sensor_filename = sha_filename(g_sensor_filename)

    payload = request.get_json()
    accident_time = payload.get('accident_time')
    car_or_motor = payload.get('car_or_motor')
    ownership = payload.get('ownership')
    object_hit = payload.get('object_hit')
    country = payload.get('country')
    description = payload.get('description')

    if file:
        file.save(os.path.join(UPLOAD_FOLDER, hash_filename))
    if g_sensor_file:
        g_sensor_file.save(os.path.join(UPLOAD_FOLDER, hash_g_sensor_filename))

    new_upload_file = UploadFile(session['user_id'], filename, hash_filename, g_sensor_filename, hash_g_sensor_filename,
                                 accident_time, car_or_motor, ownership, object_hit, country, description)

    db.session.add(new_upload_file)
    db.session.commit()

    return 'file uploaded successfully'
