from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import hashlib
import json
import multiprocessing as mp
import subprocess
import datetime
# import numpy as np
# from pandas import DataFrame
import pandas as pd

from models import User, UploadFile
from main import home
from __init__ import db
from config import *

file = Blueprint('file', __name__)

UPLOAD_FOLDER = CRASH_DETECTION_INTPUT_FILES

class detection:
    @staticmethod
    def crash_detection(video_name):
        try:
            detect_script = CRASH_DETECTION_ROOT+'/main.py'
            video = video_name
            #print('The current working directory is ', os.getcwd(), '\n')
            print('python3', detect_script, video)
            p = subprocess.Popen(['python3', detect_script, video], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out = p.communicate()

            upload_file = UploadFile.query.filter_by(vidoe_hash_filename=video_name).first()
            if len(str(out[0], encoding = "utf-8")) != 0:
                upload_file.analysis_state = 'SUCCESS'
                upload_file.analysis_result = str(out[0], encoding = "utf-8")
                db.session.commit()
            else:
                upload_file.analysis_state = 'FAIL no output'
                db.session.commit()
            
        except:
            db.session.rollback()
            upload_file = UploadFile.query.filter_by(vidoe_hash_filename=video_name).first()
            upload_file.analysis_state = 'FAIL other'
            db.session.commit()

def sha_filename(filename):
    hash_name = filename.split('.')
    hash_name[0] = hashlib.sha256((filename.split('.')[0] + str(datetime.datetime.now())).encode('utf-8')).hexdigest()
    hash_name = '.'.join(hash_name)

    return hash_name


def delete_waiting_list():
    upload_file = UploadFile.query.filter_by(analysis_state='WAITNG').all()
    print(len(upload_file))
    for f in upload_file:
        db.session.delete(f)
        db.session.commit()


@file.route('/get_result_content', methods=['GET'])
@login_required
def get_result_content():
    video_id = int(request.values.get('video_id'))

    d = UploadFile.query.filter_by(file_id=video_id).first()
    content_list = {
        "video_id": d.file_id,
        "user_id": d.user_id,
        "vidoe_filename": d.vidoe_filename,
        "vidoe_hash_filename": d.vidoe_hash_filename,
        "g_sensor_hash_filename": d.g_sensor_hash_filename,
        "accident_time": d.accident_time,
        "car_to_motor": d.car_to_motor,
        "ownership": d.ownership,
        "object_hit": d.object_hit,
        "country": d.country,
        "description": d.description,
        "crush_type": d.crush_type,
        "role": d.role,
        "insert_time": d.insert_time,
        "analysis_state": d.analysis_state,
        "analysis_result": d.analysis_result,
        "user_email": User.query.filter_by(id=d.user_id).first().email,
        "user_name": User.query.filter_by(id=d.user_id).first().name
    }

    return_data = {
        "content": content_list
    }

    # print(return_data)
    return render_template('result_content.html', data=return_data)


@file.route('/get_result', methods=['GET'])
@login_required
def get_result():
    data = UploadFile.query.all()
    print('data: ', data)

    content_list = []
    for d in data:
        content_list.append({
            "video_id": d.file_id,
            "user_id": d.user_id,
            "vidoe_filename": d.vidoe_filename,
            "vidoe_hash_filename": d.vidoe_hash_filename,
            "g_sensor_hash_filename": d.g_sensor_hash_filename,
            "accident_time": d.accident_time,
            "car_to_motor": d.car_to_motor,
            "ownership": d.ownership,
            "object_hit": d.object_hit,
            "country": d.country,
            "description": d.description,
            "crush_type": d.crush_type,
            "role": d.role,
            "insert_time": d.insert_time,
            "analysis_state": d.analysis_state,
            "analysis_result": d.analysis_result,
            "user_email": User.query.filter_by(id=d.user_id).first().email,
            "user_name": User.query.filter_by(id=d.user_id).first().name
        })
    print('content_list set')
    # print('content_list: ', content_list)

    return_data = {
        "count": len(data),
        "content": content_list
    }

    return jsonify(return_data)


@file.route('/upload_video')
@login_required
def upload():

    return render_template('upload_video.html')


@file.route('/upload_video_car')
@login_required
def upload_car():

    return render_template('upload_video_car.html')


@file.route('/upload_success')
@login_required
def upload_success():

    return render_template('upload_success.html')


@file.route('/upload_video', methods=['POST'])
@login_required
def upload_video():
    file = request.files['file']
    filename = file.filename
    hash_filename = sha_filename(filename)

    print(hash_filename)

    if file:
        file.save(os.path.join(UPLOAD_FOLDER, hash_filename))

    session['video_filename'] = filename
    session['video_hash_filename'] = hash_filename

    accident_time = request.form['accident_time']
    car_or_motor = request.form['car_or_motor']
    ownership = request.form['ownership']
    object_hit = request.form['object_hit']
    country = request.form['country']
    description = request.form['description']
    crush_type = request.form['crush_type']
    role = request.form['role']

    new_upload_file = UploadFile(session['user_id'],
                                 session['video_filename'],
                                 session['video_hash_filename'],
                                 'g_sensor_filename',
                                 'g_sensor_hash_filename',
                                 accident_time,
                                 car_or_motor,
                                 ownership,
                                 object_hit,
                                 country,
                                 description,
                                 crush_type,
                                 role)

    db.session.add(new_upload_file)
    db.session.commit()

    new_detection = mp.Process(target=detection.crash_detection, args=(session['video_hash_filename'], ))
    new_detection.start()

    return redirect(url_for('file.upload_success'))


@file.route('/upload_video_car', methods=['POST'])
@login_required
def upload_video_car():
    POSTED_SPEED_LIMIT = request.form['POSTED_SPEED_LIMIT']
    weather = request.form['weather']
    light = request.form['light']
    FIRST_CRASH_TYPE = request.form['FIRST_CRASH_TYPE']
    CRASH_HOUR = request.form['CRASH_HOUR']
    description = request.form['description']

    X_test = pd.DataFrame({
                     'POSTED_SPEED_LIMIT': [POSTED_SPEED_LIMIT,],
                     'weather_CLEAR': [0, ],
                     'weather_CLOUDY/OVERCAST': [0, ],
                     'weather_FOG/SMOKE/HAZE': [0, ],
                     'weather_OTHER': [0, ],
                     'weather_RAIN': [0, ],
                     'weather_SEVERE CROSS WIND GATE': [0, ],
                     'weather_SLEET/HAIL': [0, ],
                     'weather_SNOW': [0, ],
                     'light_DARKNESS': [0, ],
                     'light_DARKNESS: 0,  LIGHTED ROAD': [0, ],
                     'light_DAWN': [0, ],
                     'light_DAYLIGHT': [0, ],
                     'light_DUSK': [0, ],
                     'FIRST_CRASH_TYPE_ANGLE': [0,  ],
                     'FIRST_CRASH_TYPE_ANIMAL': [0, ],
                     'FIRST_CRASH_TYPE_FIXED OBJECT': [0,  ],
                     'FIRST_CRASH_TYPE_HEAD ON': [0,  ],
                     'FIRST_CRASH_TYPE_OTHER NONCOLLISION': [0,  ],
                     'FIRST_CRASH_TYPE_OTHER OBJECT': [0, ],
                     'FIRST_CRASH_TYPE_OVERTURNED': [0,  ],
                     'FIRST_CRASH_TYPE_PARKED MOTOR VEHICLE': [0,  ],
                     'FIRST_CRASH_TYPE_PEDELCYCLIST': [0,  ],
                     'FIRST_CRASH_TYPE_PEDESTRIAN': [0, ],
                     'FIRST_CRASH_TYPE_REAR END': [0,  ],
                     'FIRST_CRASH_TYPE_SIDESWIPE OPPOSITE DIRECTION': [0,  ],
                     'FIRST_CRASH_TYPE_SIDESWIPE SAME DIRECTION': [0, ],
                     'FIRST_CRASH_TYPE_TRAIN': [0, ],
                     'FIRST_CRASH_TYPE_TURNING': [0,  ],
                     'CRASH_HOUR': [CRASH_HOUR, ]
                     })

    X_test.loc[0, 'weather_' + weather] = 1
    X_test.loc[0, 'light_' + light] = 1
    X_test.loc[0, 'FIRST_CRASH_TYPE_' + FIRST_CRASH_TYPE] = 1

    from joblib import dump, load
    car_model = load('car_model.joblib')
    test_y_predicted=car_model.predict(X_test)[0]

    print('The crash type is ' + str(test_y_predicted))

    new_upload_file = UploadFile(session['user_id'],
                                 '無影片',            #session['video_filename'],
                                 '',            #session['video_hash_filename'],
                                 '',            #'g_sensor_filename',
                                 '',            #'g_sensor_hash_filename',
                                 str(CRASH_HOUR), #accident_time,
                                 '汽車',          #car_or_motor,                    
                                 '',            #ownership,
                                 '',            #object_hit,
                                 '',            #country,
                                 '速限：'+str(POSTED_SPEED_LIMIT)+', 天氣：'+weather+', 照明度：'+light+'\n'+description,            #description,
                                 FIRST_CRASH_TYPE,#crush_type,                                
                                 '',            #role)
                                 '事故等級：'+str(test_y_predicted)+
                                     '\n(說明：0: FATAL, 1: INCAPACITATING INJURY, 2: REPORTED, NOT EVIDENT, 3: NONINCAPACITATING INJURY, 4: NO INDICATION OF INJURY)' 
                                )

    db.session.add(new_upload_file)
    db.session.commit()

    return redirect(url_for('file.upload_success'))


# @file.route('/upload_g_sensor', methods=['POST'])
# @login_required
# def upload_g_sensor():
#     file = request.files['file']
#     filename = file.filename
#     hash_filename = sha_filename(filename)

#     if file:
#         file.save(os.path.join(UPLOAD_FOLDER, hash_filename))

#     session['g_sensor_filename'] = filename
#     session['g_sensor_hash_filename'] = hash_filename

#     return render_template('index.html')


# @file.route('/upload_info', methods=['POST'])
# @login_required
# def uploader():
#     accident_time = request.form['accident_time']
#     car_or_motor = request.form['car_or_motor']
#     ownership = request.form['ownership']
#     object_hit = request.form['object_hit']
#     country = request.form['country']
#     description = request.form['description']
#     crush_type = request.form['crush_type']
#     role = request.form['role']

#     new_upload_file = UploadFile(session['user_id'],
#                                  session['video_filename'],
#                                  session['video_hash_filename'],
#                                  session['g_sensor_filename'],
#                                  session['g_sensor_hash_filename'],
#                                  accident_time,
#                                  car_or_motor,
#                                  ownership,
#                                  object_hit,
#                                  country,
#                                  description,
#                                  crush_type,
#                                  role)

#     db.session.add(new_upload_file)
#     db.session.commit()

#     new_detection = mp.Process(target=detection.crash_detection, args=(session['video_hash_filename'], ))
#     new_detection.start()

#     return render_template('index.html')



