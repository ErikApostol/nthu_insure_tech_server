from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user

from models import User, ForumComment
from __init__ import db

forum = Blueprint('forum', __name__)

fake_data = {
    "count": 3,
    "content": [
        {
            "id": 12,
            "time": "2020-03-14",
            "user_id": 1,
            "user_name": "test",
            "user_email": "test@test",
            "comment": "hello!"
        },
        {
            "id": 12,
            "time": "2020-03-15",
            "user_id": 1,
            "user_name": "fff",
            "user_email": "fff@test",
            "comment": "計畫宗旨為希望透過AI技術解決傳統保險理賠的痛點，提升理賠流程的整體效率。透過深度學習與電腦視覺辨識判斷影片中碰撞的物體，並利用機器學習的AI模型預測整體車禍的事故嚴重度，只要上傳車禍發生的影片檔案，便可透過區塊鏈的串聯與AI分析技術快速的判斷此事故等級，藉以判斷車禍嚴重度"
        },
{
            "id": 12,
            "time": "2020-03-17",
            "user_id": 1,
            "user_name": "yuanda",
            "user_email": "yuanda@yuanda",
            "comment": "AIoT應用：行車紀錄器影像分析與辨識 嚴重度分析：AI模型針對機車的準確率高達94%"
        }
    ]
}


@forum.route('/forum')
def forum_index():
    data = ForumComment.query.order_by(ForumComment.insert_time.desc()).all()

    content_list = []
    for d in data:
        content_list.append({
            "id": d.comment_id,
            "time": d.insert_time,
            "user_id": d.user_id,
            "user_email": User.query.filter_by(user_id=d.user_id).first().email,
            "user_name": User.query.filter_by(user_id=d.user_id).first().name,
            "comment": d.comment
        })

    return_data = {
        "count": len(data),
        "content": content_list
    }

    return render_template('forum.html', forum_data=return_data)


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
            "user_email": User.query.filter_by(user_id=d.user_id).first().email,
            "user_name": User.query.filter_by(user_id=d.user_id).first().name,
            "comment": d.comment
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
    tag = ','.join(data.get('tag'))

    new_comment = ForumComment(comment=comment, user_id=user_id,
                                 video_id=video_id, tag=tag)
    db.session.add(new_comment)
    db.session.commit()

    return redirect(url_for('forum.forum_index'))
