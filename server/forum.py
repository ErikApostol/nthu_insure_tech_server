from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session; print('forum.py', 1, 'Done')
from werkzeug.security import generate_password_hash, check_password_hash; print('forum.py', 2, 'Done')
from flask_login import login_required, current_user; print('forum.py', 3, 'Done')
from sqlalchemy import or_, text; print('forum.py', 4, 'Done')

from models import User, ForumComment, ForumPost, UploadFile; print('forum.py', 6, 'Done')
from main import home; print('forum.py', 7, 'Done')
from __init__ import db; print('forum.py', 8, 'Done')

forum = Blueprint('forum', __name__); print('forum.py', 10, 'Done')


@forum.route('/forum/filter', methods=['GET'])
# @login_required
def forum_filter():
    filter_text = request.values.get('filter'); print('forum.py', 16, 'Done')

    data = ForumPost.query.order_by(ForumPost.insert_time.desc()).all(); print('forum.py', 18, 'Done')

    post_list = []; print('forum.py', 20, 'Done')
    for d in data:
        sql = text("SELECT * FROM 'UploadFile' \
        WHERE file_id={video_id} AND ( \
        car_to_motor LIKE '%{filter}%' \
        OR ownership LIKE '%{filter}%' \
        OR object_hit LIKE '%{filter}%' \
        OR country LIKE '%{filter}%' \
        OR crush_type LIKE '%{filter}%' \
        OR role LIKE '%{filter}%' \
        ) \
        ".format(video_id=d.video_id, filter=filter_text)); print('forum.py', 31, 'Done')
        result = db.engine.execute(sql).fetchall(); print('forum.py', 32, 'Done')
        if len(result) > 0:
            post_list.append(d); print('forum.py', 34, 'Done')

    content_list = []; print('forum.py', 36, 'Done')
    for d in post_list:
        content_list.append({
            "id": d.post_id,
            "time": d.insert_time,
            "user_id": d.user_id,
            "user_email": User.query.filter_by(id=d.user_id).first().email,
            "user_name": User.query.filter_by(id=d.user_id).first().name,
            "comment": d.comment,
            "title": d.title,
            "video_id": d.video_id
        }); print('forum.py', 47, 'Done')

    return_data = {
        "count": len(post_list),
        "content": content_list
    }; print('forum.py', 52, 'Done')

    print('forum.py', 54, 'Before Done'); return render_template('search.html', forum_data=return_data)


@forum.route('/forum')
def forum_index():
    data = ForumPost.query.order_by(ForumPost.insert_time.desc()).all(); print('forum.py', 59, 'Done')
    #data = fake_data

    content_list = []; print('forum.py', 62, 'Done')
    for d in data:
        content_list.append({
            "id": d.post_id,
            "time": d.insert_time,
            "user_id": d.user_id,
            "user_email": User.query.filter_by(id=d.user_id).first().email,
            "user_name": User.query.filter_by(id=d.user_id).first().name,
            "comment": d.comment,
            "title": d.title,
            "video_id": d.video_id
        }); print('forum.py', 73, 'Done')

    return_data = {
        "count": len(data),
        "content": content_list
    }; print('forum.py', 78, 'Done')

    print('forum.py', 80, 'Before Done'); return render_template('forum.html', forum_data=return_data)


@forum.route('/users_own_video')
@login_required
def users_own_video():
    data = ForumComment.query.filter_by(user_id=session.get('user_id')).all(); print('forum.py', 86, 'Done')

    content_list = []; print('forum.py', 88, 'Done')
    for d in data:
        content_list.append({
            "id": d.comment_id,
            "time": d.insert_time,
            "user_id": d.user_id,
            "user_email": User.query.filter_by(id=d.user_id).first().email,
            "user_name": User.query.filter_by(id=d.user_id).first().name,
            "comment": d.comment,
            "title": d.title,
            "video_id": d.video_id
        }); print('forum.py', 99, 'Done')

    return_data = {
        "count": len(data),
        "content": content_list
    }; print('forum.py', 104, 'Done')

    stats = home(); print('forum.py', 106, 'Done')

    print('forum.py', 108, 'Before Done'); return render_template('forum.html', forum_data=return_data, stats=stats)


@forum.route('/get_forum_data')
# @login_required
def get_forum_data():
    data = ForumComment.query.order_by(ForumComment.insert_time.desc()).all(); print('forum.py', 114, 'Done')

    content_list = []; print('forum.py', 116, 'Done')
    for d in data:
        content_list.append({
            "id": d.comment_id,
            "time": d.insert_time,
            "user_id": d.user_id,
            "title": d.title,
            "user_email": User.query.filter_by(id=d.user_id).first().email,
            "user_name": User.query.filter_by(id=d.user_id).first().name,
            "comment": d.comment,
            "video_id": d.video_id
        }); print('forum.py', 127, 'Done')

    return_data = {
        "count": len(data),
        "content": content_list
    }; print('forum.py', 132, 'Done')

    print('forum.py', 134, 'Before Done'); return jsonify(return_data)


@forum.route('/post', methods=['POST'])
@login_required
def post_data():
    user_id = session['user_id']; print('forum.py', 140, 'Done')
    data = request.get_json(); print('forum.py', 141, 'Done')
    comment = data.get('comment'); print('forum.py', 142, 'Done')
    video_id = data.get('video_id'); print('forum.py', 143, 'Done')
    tag = data.get('tag'); print('forum.py', 144, 'Done')
    title = data.get('title'); print('forum.py', 145, 'Done')

    new_comment = ForumPost(title=title, comment=comment, user_id=user_id,
                                 video_id=video_id, tag=tag); print('forum.py', 148, 'Done')
    db.session.add(new_comment); print('forum.py', 149, 'Done')
    print('Before commit.'); print('forum.py', 150, 'Done')
    db.session.commit(); print('forum.py', 151, 'Done')
    print('After commit.'); print('forum.py', 152, 'Done')


    print('forum.py', 155, 'Before Done'); return redirect(url_for('forum.forum_index'))


@forum.route('/comment', methods=['GET'])
@login_required
def post_comment_data():
    user_id = session['user_id']; print('forum.py', 161, 'Done')
    comment = request.values.get('comment'); print('forum.py', 162, 'Done')
    post_id = request.values.get('post_id'); print('forum.py', 163, 'Done')
    user_name = User.query.filter_by(id=user_id).first().name; print('forum.py', 164, 'Done')

    new_comment = ForumComment(comment=comment, user_id=user_id,
                                 post_id=post_id, user_name=user_name); print('forum.py', 167, 'Done')
    db.session.add(new_comment); print('forum.py', 168, 'Done')
    print('Before commit.'); print('forum.py', 169, 'Done')
    db.session.commit(); print('forum.py', 170, 'Done')
    print('After commit.'); print('forum.py', 171, 'Done')


    print('forum.py', 174, 'Before Done'); return redirect(url_for('forum.forum_index'))


@forum.route('/post_page', methods=['GET'])
# @login_required
def post_page():
    post_id = int(request.values.get('post_id')); print('forum.py', 180, 'Done')

    post = ForumPost.query.filter_by(post_id=post_id).first(); print('forum.py', 182, 'Done')
    comments = ForumComment.query.filter_by(post_id=post_id).order_by(ForumComment.insert_time.asc()).all(); print('forum.py', 183, 'Done')
    d = UploadFile.query.filter_by(file_id=post.video_id).first(); print('forum.py', 184, 'Done')

    video_content_list = {
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
    }; print('forum.py', 205, 'Done')

    post_content = {
        "post_id": post.post_id,
        "time": post.insert_time,
        "user_id": post.user_id,
        "user_email": User.query.filter_by(id=post.user_id).first().email,
        "user_name": User.query.filter_by(id=post.user_id).first().name,
        "comment": post.comment,
        "title": post.title,
        "video_id": post.video_id
    }; print('forum.py', 216, 'Done')

    comment_list = []; print('forum.py', 218, 'Done')
    for m in comments:
        comment_list.append({
            "comment": m.comment,
            "user_name": m.user_name
        }); print('forum.py', 223, 'Done')

    return_data = {
        "video_content": video_content_list,
        "post_content": post_content,
        "comment_content": comment_list,
        "comment_count": len(comment_list)
    }; print('forum.py', 230, 'Done')

    # print(return_data)
    print('forum.py', 233, 'Before Done'); return render_template('post_page.html', data=return_data)
