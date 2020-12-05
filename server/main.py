from flask import Blueprint, render_template, session, jsonify, request, redirect, url_for, Response; print('main.py', 1, 'Done')
from flask_login import login_required, current_user; print('main.py', 2, 'Done')
from __init__ import db; print('main.py', 3, 'Done')

main = Blueprint('main', __name__); print('main.py', 5, 'Done')


@main.route('/')
def index():
    db.create_all(); print('main.py', 10, 'Done')

    from models import Visit; print('main.py', 12, 'Done')
    visitor = Visit.query.filter_by(ip=request.remote_addr).first(); print('main.py', 13, 'Done')
    if not visitor:
        new_visitor = Visit(request.remote_addr); print('main.py', 15, 'Done')
        db.session.add(new_visitor); print('main.py', 16, 'Done')
        print('Before commit.'); print('main.py', 17, 'Done')
        db.session.commit(); print('main.py', 18, 'Done')
        print('After commit.'); print('main.py', 19, 'Done')


    print('main.py', 22, 'Before Done'); return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    print('main.py', 28, 'Before Done'); return render_template('profile.html', name = current_user.name if hasattr(current_user, 'name') else '')


@main.route('/anaylsis_result')
@login_required
def anaylsis_result():
    print('main.py', 34, 'Before Done'); return render_template('result.html')


@main.route('/new_post')
@login_required
def new_post():
    print('main.py', 40, 'Before Done'); return render_template('new_post.html')


@main.route('/home')
def home():
    from models import UploadFile; print('main.py', 45, 'Done')
    your_video = len(UploadFile.query.filter_by(user_id = session.get('user_id')).all()); print('main.py', 46, 'Done')
    all_video = len(UploadFile.query.all()); print('main.py', 47, 'Done')

    from models import User; print('main.py', 49, 'Done')
    number_of_user_registered = len(User.query.all()); print('main.py', 50, 'Done')

    from models import Visit; print('main.py', 52, 'Done')
    visited = len(Visit.query.all()); print('main.py', 53, 'Done')

    ret = {
        'your_video': your_video,
        'all_video': all_video,
        'number_of_user_registered': number_of_user_registered,
        'visited': visited
    }; print('main.py', 60, 'Done')

    print('main.py', 62, 'Before Done'); return jsonify(ret)


@main.route('/home/total_video')
def home_total_video():
    print('main.py', 67, 'Before Done'); return redirect(url_for('forum.forum_index'))


@main.route('/home/your_video')
def home_your_video():
    print('main.py', 72, 'Before Done'); return redirect(url_for('forum.users_own_video'))


@main.route('/get_username')
def get_username():
    username = ''; print('main.py', 77, 'Done')
    try:
        print('take username'); print('main.py', 79, 'Done')
        if hasattr(current_user, 'name'):
            username = current_user.name; print('main.py', 81, 'Done')
        else:
            username = ''; print('main.py', 83, 'Done')
        print('username: ', username); print('main.py', 84, 'Done')
    except:
        print('main.py', 86, 'Before Done'); pass

    ret = {
        'username': username
    }; print('main.py', 90, 'Done')
    print('ret: ', ret); print('main.py', 91, 'Done')

    print('main.py', 93, 'Before Done'); return jsonify(ret)

# Source: https://medium.com/@ericwuehler/using-let-s-encrpyt-9175feb76632
@main.route('/.well-known/acme-challenge/<challenge>')
def letsencrypt_check(challenge):
    challenge_response = {
        "zWYD-opVM50G4Exmbzd3XPuL7lEPDSVGq8W88Y6exq4":"zWYD-opVM50G4Exmbzd3XPuL7lEPDSVGq8W88Y6exq4.oU8XRNS5izeH5v3gYpgwJFgc-5cPO6iDNvn3A2EJ2Qw"
    }
    return Response(challenge_response[challenge], mimetype='text/plain')

# redirect all http to https
# @main.before_request
# def before_request():
#     if request.url.startswith('http://'):
#         return redirect(request.url.replace('http://', 'https://'), code=301)
