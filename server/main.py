from flask import Blueprint, render_template, session, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from __init__ import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    db.create_all()

    from models import Visit
    visitor = Visit.query.filter_by(ip=request.remote_addr).first()
    if not visitor:
        new_visitor = Visit(request.remote_addr)
        db.session.add(new_visitor)
        db.session.commit()

    stats = home()

    if hasattr(current_user, 'name'):
        return render_template('index.html', name=current_user.name, step_1=True, step_2=True, stats=stats)
    else:
        return render_template('index.html', step_1=True, step_2=True, stats=stats)


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/home')
def home():
    print(session.get('user_id'))
    from models import UploadFile
    your_video = len(UploadFile.query.filter_by(user_id = session.get('user_id')).all())
    all_video = len(UploadFile.query.all())

    from models import User
    number_of_user_registered = len(User.query.all())

    from models import Visit
    visited = len(Visit.query.all())

    ret = {
        'your_video': your_video,
        'all_video': all_video,
        'number_of_user_registered': number_of_user_registered,
        'visited': visited
    }

    return jsonify(ret)


@main.route('/home/total_video')
def home_total_video():
    return redirect(url_for('forum.forum_index'))


@main.route('/home/your_video')
def home_your_video():
    return redirect(url_for('forum.users_own_video'))
