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

    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/anaylsis_result')
@login_required
def anaylsis_result():
    return render_template('result.html')


@main.route('/new_post')
@login_required
def new_post():
    return render_template('new_post.html')


@main.route('/home')
def home():
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


@main.route('/get_username')
def get_uaername():
    uaername = ''
    try:
        username = current_user.name
    except:
        pass

    ret = {
        'username': username
    }

    return jsonify(ret)

# Source: https://medium.com/@ericwuehler/using-let-s-encrpyt-9175feb76632
#@main.route('/.well-known/acme-challenge/<challenge>')
#def letsencrypt_check(challenge):
#    challenge_response = {
#        "<challenge_token>":"<challenge_response>",
#        "<challenge_token>":"<challenge_response>"
#    }
#    return Response(challenge_response[challenge], mimetype='text/plain')

# redirect all http to https
# @main.before_request
# def before_request():
#     if request.url.startswith('http://'):
#         return redirect(request.url.replace('http://', 'https://'), code=301)
