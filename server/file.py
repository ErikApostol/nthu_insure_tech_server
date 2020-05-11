from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import hashlib
import json

from models import User, UploadFile
from __init__ import db

file = Blueprint('file', __name__)

UPLOAD_FOLDER = './tmp'

def sha_filename(filename):
    hash_name = filename.split('.')
    hash_name[0] = hashlib.sha256(filename.split('.')[0].encode('utf-8')).hexdigest()
    hash_name = '.'.join(hash_name)

    return hash_name


@file.route('/upload_video', methods=['POST'])
@login_required
def upload_video():
    file = request.files['file']
    filename = file.filename
    hash_filename = sha_filename(filename)

    if file:
        file.save(os.path.join(UPLOAD_FOLDER, hash_filename))

    session['video_filename'] = filename
    session['video_hash_filename'] = hash_filename

    return render_template('index.html', step_1=False, step_2=True)


@file.route('/upload_g_sensor', methods=['POST'])
@login_required
def upload_g_sensor():
    file = request.files['file']
    filename = file.filename
    hash_filename = sha_filename(filename)

    if file:
        file.save(os.path.join(UPLOAD_FOLDER, hash_filename))

    session['g_sensor_filename'] = filename
    session['g_sensor_hash_filename'] = hash_filename

    return render_template('index.html', step_1=False, step_2=False)


@file.route('/upload_info', methods=['POST'])
@login_required
def uploader():
    accident_time = request.form['accident_time']
    car_or_motor = request.form['car_or_motor']
    ownership = request.form['ownership']
    object_hit = request.form['object_hit']
    country = request.form['country']
    description = request.form['description']

    new_upload_file = UploadFile(session['user_id'], session['video_filename'], session['video_hash_filename'], session['g_sensor_filename'], session['g_sensor_hash_filename'],
                                 accident_time, car_or_motor, ownership, object_hit, country, description)

    db.session.add(new_upload_file)
    db.session.commit()

    return render_template('index.html', step_1=True, step_2=True)
