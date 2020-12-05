from flask import request; print('models.py', 1, 'Done')
from flask_login import UserMixin; print('models.py', 2, 'Done')
from datetime import datetime; print('models.py', 3, 'Done')
from __init__ import db; print('models.py', 4, 'Done')


class Visit(db.Model):
    __tablename__ = 'Visit'; print('models.py', 8, 'Done')
    id = db.Column(db.Integer, primary_key=True); print('models.py', 9, 'Done')
    ip = db.Column(db.String(1000), unique=True); print('models.py', 10, 'Done')
    insert_time = db.Column(db.DateTime, default=datetime.now); print('models.py', 11, 'Done')

    def __init__(self, ip):
        self.ip = ip; print('models.py', 14, 'Done')

class User(UserMixin, db.Model):
    __tablename__ = 'User'; print('models.py', 17, 'Done')
    id = db.Column(db.Integer, primary_key=True); print('models.py', 18, 'Done')
    email = db.Column(db.String(100), unique=True); print('models.py', 19, 'Done')
    password = db.Column(db.String(100)); print('models.py', 20, 'Done')
    name = db.Column(db.String(1000)); print('models.py', 21, 'Done')
    personal_id = db.Column(db.String(1000)); print('models.py', 22, 'Done')
    b_date = db.Column(db.DateTime); print('models.py', 23, 'Done')
    insert_time = db.Column(db.DateTime, default=datetime.now); print('models.py', 24, 'Done')


class ForumComment(db.Model):
    __tablename__ = 'ForumComment'; print('models.py', 28, 'Done')
    comment_id = db.Column(db.Integer, primary_key=True); print('models.py', 29, 'Done')
    comment = db.Column(db.String(2048)); print('models.py', 30, 'Done')
    insert_time = db.Column(db.DateTime, default=datetime.now); print('models.py', 31, 'Done')
    user_id = db.Column(db.Integer); print('models.py', 32, 'Done')
    post_id = db.Column(db.Integer); print('models.py', 33, 'Done')
    user_name = db.Column(db.String(100)); print('models.py', 34, 'Done')

    def __init__(self, comment, user_id, post_id, user_name):
        self.comment = comment; print('models.py', 37, 'Done')
        self.user_id = user_id; print('models.py', 38, 'Done')
        self.post_id = post_id; print('models.py', 39, 'Done')
        self.user_name = user_name; print('models.py', 40, 'Done')


class ForumPost(db.Model):
    __tablename__ = 'ForumPost'; print('models.py', 44, 'Done')
    post_id = db.Column(db.Integer, primary_key=True); print('models.py', 45, 'Done')
    comment = db.Column(db.String(2048)); print('models.py', 46, 'Done')
    title = db.Column(db.String(100)); print('models.py', 47, 'Done')
    insert_time = db.Column(db.DateTime, default=datetime.now); print('models.py', 48, 'Done')
    user_id = db.Column(db.Integer); print('models.py', 49, 'Done')
    video_id = db.Column(db.Integer); print('models.py', 50, 'Done')

    # tag: taiwan,car,...
    tag = db.Column(db.String(2048)); print('models.py', 53, 'Done')

    def __init__(self, title, comment, user_id, video_id, tag):
        self.title = title; print('models.py', 56, 'Done')
        self.comment = comment; print('models.py', 57, 'Done')
        self.user_id = user_id; print('models.py', 58, 'Done')
        self.video_id = video_id; print('models.py', 59, 'Done')
        self.tag = tag; print('models.py', 60, 'Done')


class UploadFile(db.Model):
    __tablename__ = 'UploadFile'; print('models.py', 64, 'Done')
    file_id = db.Column(db.Integer, primary_key=True); print('models.py', 65, 'Done')
    user_id = db.Column(db.Integer); print('models.py', 66, 'Done')

    video_filename = db.Column(db.String(2048)); print('models.py', 68, 'Done')
    video_hash_filename = db.Column(db.String(2048)); print('models.py', 69, 'Done')
    g_sensor_filename = db.Column(db.String(2048)); print('models.py', 70, 'Done')
    g_sensor_hash_filename = db.Column(db.String(2048)); print('models.py', 71, 'Done')

    accident_time = db.Column(db.String(2048)); print('models.py', 73, 'Done')
    car_to_motor = db.Column(db.String(2048)); print('models.py', 74, 'Done')
    ownership = db.Column(db.String(2048)); print('models.py', 75, 'Done')
    object_hit = db.Column(db.String(2048)); print('models.py', 76, 'Done')
    country = db.Column(db.String(2048)); print('models.py', 77, 'Done')
    description = db.Column(db.String(2048)); print('models.py', 78, 'Done')
    crush_type = db.Column(db.String(2048)); print('models.py', 79, 'Done')
    role = db.Column(db.String(2048)); print('models.py', 80, 'Done')

    insert_time = db.Column(db.DateTime, default=datetime.now); print('models.py', 82, 'Done')
    analysis_state = db.Column(db.String(20), default='WAITING'); print('models.py', 83, 'Done')
    analysis_result = db.Column(db.String(100), default=''); print('models.py', 84, 'Done')

    def __init__(self, user_id, filename, hash_filename, g_sensor_filename, hash_g_sensor_filename, accident_time,
                 car_or_motor, ownership, object_hit, country, description, crush_type, role, analysis_result=None):
        self.user_id = user_id; print('models.py', 88, 'Done')
        self.video_filename = filename; print('models.py', 89, 'Done')
        self.video_hash_filename = hash_filename; print('models.py', 90, 'Done')
        self.g_sensor_filename = g_sensor_filename; print('models.py', 91, 'Done')
        self.g_sensor_hash_filename = hash_g_sensor_filename; print('models.py', 92, 'Done')
        self.accident_time = accident_time; print('models.py', 93, 'Done')
        self.car_to_motor = car_or_motor; print('models.py', 94, 'Done')
        self.ownership = ownership; print('models.py', 95, 'Done')
        self.object_hit = object_hit; print('models.py', 96, 'Done')
        self.country = country; print('models.py', 97, 'Done')
        self.description = description; print('models.py', 98, 'Done')
        self.crush_type = crush_type; print('models.py', 99, 'Done')
        self.role = role; print('models.py', 100, 'Done')

        if analysis_result:
            self.analysis_result = analysis_result; print('models.py', 103, 'Done')
            self.analysis_state = 'SUCCESS'; print('models.py', 104, 'Done')
