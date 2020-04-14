from flask_login import UserMixin
from datetime import datetime
from __init__ import db


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class ForumComment(db.Model):
    __tablename__ = 'ForumComment'
    comment_id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(2048))
    insert_time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer)
    video_id = db.Column(db.Integer)

    # tag: taiwan,car,...
    tag = db.Column(db.String(2048))

    def __init__(self, comment, user_id, video_id, tag):
        self.comment = comment
        self.user_id = user_id
        self.video_id = video_id
        self.tag = tag
