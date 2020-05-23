from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user

from models import User, ForumComment
from main import home
from __init__ import db

forum = Blueprint('forum', __name__)


@forum.route('/forum/filter', methods=['POST'])
def forum_filter():
    country = request.form['country']
    car_or_motor = request.form['car_or_motor']
    crush_type = request.form['crush_type']
    role = request.form['role']

    from models import UploadFile
    video_data = UploadFile.query_by(country=country, car_or_motor=car_or_motor, crush_type=crush_type, role=role).all()
    video_id_set = [d.file_id for d in video_data]
    data = ForumComment.query.filter(ForumComment.video_id.in_(video_id_set))

    content_list = []
    for d in data:
        content_list.append({
            "id": d.comment_id,
            "time": d.insert_time,
            "user_id": d.user_id,
            "user_email": User.query.filter_by(user_id=d.user_id).first().email,
            "user_name": User.query.filter_by(user_id=d.user_id).first().name,
            "comment": d.comment,
            "video_id": d.video_id
        })

    return_data = {
        "count": len(data),
        "content": content_list
    }

    return jsonify(return_data)


@forum.route('/forum')
def forum_index():
    data = ForumComment.query.order_by(ForumComment.insert_time.desc()).all()
    #data = fake_data

    content_list = []
    for d in data:
        content_list.append({
            "id": d.comment_id,
            "time": d.insert_time,
            "user_id": d.user_id,
            "user_email": User.query.filter_by(id=d.user_id).first().email,
            "user_name": User.query.filter_by(id=d.user_id).first().name,
            "comment": d.comment,
            "video_id": d.video_id
        })

    return_data = {
        "count": len(data),
        "content": content_list
    }

    stats = home()

    return render_template('forum.html', forum_data=return_data, stats=stats)


@forum.route('/users_own_video')
@login_required
def users_own_video():
    data = ForumComment.query.filter_by(user_id=session.get('user_id')).all()

    content_list = []
    for d in data:
        content_list.append({
            "id": d.comment_id,
            "time": d.insert_time,
            "user_id": d.user_id,
            "user_email": User.query.filter_by(user_id=d.user_id).first().email,
            "user_name": User.query.filter_by(user_id=d.user_id).first().name,
            "comment": d.comment,
            "video_id": d.video_id
        })

    return_data = {
        "count": len(data),
        "content": content_list
    }

    stats = home()

    return render_template('forum.html', forum_data=return_data, stats=stats)


@forum.route('/get_forum_data')
# @login_required
def get_forum_data():
    data = ForumComment.query.order_by(ForumComment.insert_time.desc()).all()

    content_list = []
    for d in data:
        content_list.append({
            "id": d.comment_id,
            "time": d.insert_time,
            "user_id": d.user_id,
            "user_email": User.query.filter_by(id=d.user_id).first().email,
            "user_name": User.query.filter_by(id=d.user_id).first().name,
            "comment": d.comment,
            "video_id": d.video_id
        })

    return_data = {
        "count": len(data),
        "content": content_list
    }

    return jsonify(return_data)


@forum.route('/comment', methods=['POST'])
@login_required
def post_comment_data():
    user_id = session['user_id']
    data = request.get_json()
    comment = data.get('comment')
    video_id = data.get('video_id')
    tag = data.get('tag')

    new_comment = ForumComment(comment=comment, user_id=user_id,
                                 video_id=video_id, tag=tag)
    db.session.add(new_comment)
    db.session.commit()

    return redirect(url_for('forum.forum_index'))
