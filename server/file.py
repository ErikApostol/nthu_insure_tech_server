from flask import Blueprint, render_template, send_from_directory, redirect, url_for, request, flash, jsonify, session; print('file.py', 1, 'Done')
from werkzeug.security import generate_password_hash, check_password_hash; print('file.py', 2, 'Done')
from flask_login import login_required, current_user; print('file.py', 3, 'Done')
from werkzeug.utils import secure_filename; print('file.py', 4, 'Done')
import os; print('file.py', 5, 'Done')
import hashlib; print('file.py', 6, 'Done')
import json; print('file.py', 7, 'Done')
import multiprocessing as mp; print('file.py', 8, 'Done')
import subprocess; print('file.py', 9, 'Done')
import datetime; print('file.py', 10, 'Done')
# import numpy as np
# from pandas import DataFrame
import pandas as pd; print('file.py', 13, 'Done')

from models import User, UploadFile; print('file.py', 15, 'Done')
from main import home; print('file.py', 16, 'Done')
from __init__ import db; print('file.py', 17, 'Done')
from config import *; print('file.py', 18, 'Done')

file = Blueprint('file', __name__); print('file.py', 20, 'Done')

UPLOAD_FOLDER = CRASH_DETECTION_INTPUT_FILES; print('file.py', 22, 'Done')

class detection:
    @staticmethod
    def crash_detection(video_name):
        try:
            detect_script = CRASH_DETECTION_ROOT+'/main.py'; print('file.py', 28, 'Done')
            video = video_name; print('file.py', 29, 'Done')
            #print('The current working directory is ', os.getcwd(), '\n')
            print('python3', detect_script, video); print('file.py', 31, 'Done')
            p = subprocess.Popen(['python3', detect_script, video], stdout=subprocess.PIPE, stderr=subprocess.PIPE); print('file.py', 32, 'Done')
            out = p.communicate(); print('file.py', 33, 'Done')

            upload_file = UploadFile.query.filter_by(video_hash_filename=video_name).first(); print('file.py', 35, 'Done')
            if len(str(out[0], encoding = "utf-8")) != 0:
                upload_file.analysis_state = 'SUCCESS'; print('file.py', 37, 'Done')
                upload_file.analysis_result = str(out[0], encoding = "utf-8"); print('file.py', 38, 'Done')
                print('Before commit.'); print('file.py', 39, 'Done')
                db.session.commit(); print('file.py', 40, 'Done')
                print('After commit.'); print('file.py', 41, 'Done')

            else:
                upload_file.analysis_state = 'FAIL no output'; print('file.py', 44, 'Done')
                print('Before commit.'); print('file.py', 45, 'Done')
                db.session.commit(); print('file.py', 46, 'Done')
                print('After commit.'); print('file.py', 47, 'Done')

        except:
            db.session.rollback(); print('file.py', 50, 'Done')
            upload_file = UploadFile.query.filter_by(video_hash_filename=video_name).first(); print('file.py', 51, 'Done')
            upload_file.analysis_state = 'FAIL other'; print('file.py', 52, 'Done')
            print('Before commit.'); print('file.py', 53, 'Done')
            db.session.commit(); print('file.py', 54, 'Done')
            print('After commit.'); print('file.py', 55, 'Done')


def sha_filename(filename):
    hash_name = filename.split('.'); print('file.py', 59, 'Done')
    hash_name[0] = hashlib.sha256((filename.split('.')[0] + str(datetime.datetime.now())).encode('utf-8')).hexdigest(); print('file.py', 60, 'Done')
    hash_name = '.'.join(hash_name); print('file.py', 61, 'Done')

    print('file.py', 63, 'Before Done'); return hash_name


def delete_waiting_list():
    upload_file = UploadFile.query.filter_by(analysis_state='WAITNG').all(); print('file.py', 67, 'Done')
    print(len(upload_file)); print('file.py', 68, 'Done')
    for f in upload_file:
        db.session.delete(f); print('file.py', 70, 'Done')
        print('Before commit.'); print('file.py', 71, 'Done')
        db.session.commit(); print('file.py', 72, 'Done')
        print('After commit.'); print('file.py', 73, 'Done')



@file.route('/get_result_content', methods=['GET'])
@login_required
def get_result_content():
    video_id = int(request.values.get('video_id')); print('file.py', 80, 'Done')

    d = UploadFile.query.filter_by(file_id=video_id).first(); print('file.py', 82, 'Done')
    content_list = {
        "video_id": d.file_id,
        "user_id": d.user_id,
        "video_filename": d.video_filename,
        "video_hash_filename": d.video_hash_filename,
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
    }; print('file.py', 102, 'Done')

    return_data = {
        "content": content_list
    }; print('file.py', 106, 'Done')

    # print(return_data)
    print('file.py', 109, 'Before Done'); return render_template('result_content.html', data=return_data)


@file.route('/get_result', methods=['GET'])
@login_required
def get_result():
    data = UploadFile.query.all(); print('file.py', 115, 'Done')
    print('data: ', data); print('file.py', 116, 'Done')

    content_list = []; print('file.py', 118, 'Done')
    for d in data:
        content_list.append({
            "video_id": d.file_id,
            "user_id": d.user_id,
            "video_filename": d.video_filename,
            "video_hash_filename": d.video_hash_filename,
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
        }); print('file.py', 139, 'Done')
    print('content_list set'); print('file.py', 140, 'Done')
    # print('content_list: ', content_list)

    return_data = {
        "count": len(data),
        "content": content_list
    }; print('file.py', 146, 'Done')

    print('file.py', 148, 'Before Done'); return jsonify(return_data)


@file.route('/upload_video')
@login_required
def upload():

    print('file.py', 155, 'Before Done'); return render_template('upload_video.html')


@file.route('/upload_video_car')
@login_required
def upload_car():

    print('file.py', 162, 'Before Done'); return render_template('upload_video_car.html')


@file.route('/upload_success')
@login_required
def upload_success():

    print('file.py', 169, 'Before Done'); return render_template('upload_success.html')


@file.route('/upload_video', methods=['POST'])
@login_required
def upload_video():
    file = request.files['file']; print('file.py', 175, 'Done')
    filename = file.filename; print('file.py', 176, 'Done')
    hash_filename = sha_filename(filename); print('file.py', 177, 'Done')

    print(hash_filename); print('file.py', 179, 'Done')

    if file:
        file.save(os.path.join(UPLOAD_FOLDER, hash_filename)); print('file.py', 182, 'Done')

    session['video_filename'] = filename; print('file.py', 184, 'Done')
    session['video_hash_filename'] = hash_filename; print('file.py', 185, 'Done')

    accident_time = request.form['accident_time']; print('file.py', 187, 'Done')
    car_or_motor = request.form['car_or_motor']; print('file.py', 188, 'Done')
    ownership = request.form['ownership']; print('file.py', 189, 'Done')
    object_hit = request.form['object_hit']; print('file.py', 190, 'Done')
    country = request.form['country']; print('file.py', 191, 'Done')
    description = request.form['description']; print('file.py', 192, 'Done')
    crush_type = request.form['crush_type']; print('file.py', 193, 'Done')
    role = request.form['role']; print('file.py', 194, 'Done')

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
                                 role); print('file.py', 208, 'Done')

    db.session.add(new_upload_file); print('file.py', 210, 'Done')
    print('Before commit.'); print('file.py', 211, 'Done')
    db.session.commit(); print('file.py', 212, 'Done')
    print('After commit.'); print('file.py', 213, 'Done')


    new_detection = mp.Process(target=detection.crash_detection, args=(session['video_hash_filename'], )); print('file.py', 216, 'Done')
    new_detection.start(); print('file.py', 217, 'Done')

    print('file.py', 219, 'Before Done'); return redirect(url_for('file.upload_success'))


@file.route('/upload_video_car', methods=['POST'])
@login_required
def upload_video_car():
    POSTED_SPEED_LIMIT = request.form['POSTED_SPEED_LIMIT']; print('file.py', 225, 'Done')
    weather = request.form['weather']; print('file.py', 226, 'Done')
    light = request.form['light']; print('file.py', 227, 'Done')
    FIRST_CRASH_TYPE = request.form['FIRST_CRASH_TYPE']; print('file.py', 228, 'Done')
    CRASH_HOUR = request.form['CRASH_HOUR']; print('file.py', 229, 'Done')
    description = request.form['description']; print('file.py', 230, 'Done')

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
                     }); print('file.py', 263, 'Done')

    X_test.loc[0, 'weather_' + weather] = 1; print('file.py', 265, 'Done')
    X_test.loc[0, 'light_' + light] = 1; print('file.py', 266, 'Done')
    X_test.loc[0, 'FIRST_CRASH_TYPE_' + FIRST_CRASH_TYPE] = 1; print('file.py', 267, 'Done')

    from joblib import dump, load; print('file.py', 269, 'Done')
    car_model = load('car_model.joblib'); print('file.py', 270, 'Done')
    test_y_predicted=car_model.predict(X_test)[0]; print('file.py', 271, 'Done')

    print('The crash type is ' + str(test_y_predicted)); print('file.py', 273, 'Done')

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
                                ); print('file.py', 290, 'Done')

    db.session.add(new_upload_file); print('file.py', 292, 'Done')
    print('Before commit.'); print('file.py', 293, 'Done')
    db.session.commit(); print('file.py', 294, 'Done')
    print('After commit.'); print('file.py', 295, 'Done')


    print('file.py', 298, 'Before Done'); return redirect(url_for('file.upload_success'))


@file.route('/download_list')
@login_required
def download_list():
    if session['user_email']=='CKI_89c05@admin':
        data = UploadFile.query.all(); print('file.py', 305, 'Done')
        content_list = []; print('file.py', 118, 'Done')
        for d in data:
            content_list.append({
                "video_id": d.file_id,
                "user_id": d.user_id,
                "video_filename": d.video_filename,
                "video_hash_filename": d.video_hash_filename,
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
            }); print('file.py', 139, 'Done')
        return render_template('download_list.html', data=content_list)
    else:
        return render_template('not_allowed.html')


@file.route('/download/<video_filename>', methods=['GET', 'POST'])
@login_required
def download(video_filename):
    if session['user_email']=='CKI_89c05@admin':
        uploads = os.path.join(CRASH_DETECTION_INTPUT_FILES)
        return send_from_directory(directory=uploads, filename=video_filename)
    else:
        return render_template('not_allowed.html')




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



