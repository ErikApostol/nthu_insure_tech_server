from flask import Blueprint, render_template, redirect, url_for, request, flash, session; print('auth.py', 1, 'Done')
from werkzeug.security import generate_password_hash, check_password_hash; print('auth.py', 2, 'Done')
from flask_login import login_user, logout_user, login_required; print('auth.py', 3, 'Done')
from datetime import datetime; print('auth.py', 4, 'Done')

from models import User; print('auth.py', 6, 'Done')
from __init__ import db; print('auth.py', 7, 'Done')

auth = Blueprint('auth', __name__); print('auth.py', 9, 'Done')


@auth.route('/login')
def login():
    print('auth.py', 14, 'Before Done'); return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email'); print('auth.py', 19, 'Done')
    password = request.form.get('password'); print('auth.py', 20, 'Done')
    remember = True if request.form.get('remember') else False; print('auth.py', 21, 'Done')

    user = User.query.filter_by(email=email).first(); print('auth.py', 23, 'Done')
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.'); print('auth.py', 25, 'Done')
        print('auth.py', 26, 'Before Done'); return redirect(url_for('auth.login'))

    print(user.name, user.id); print('auth.py', 28, 'Done')
    login_user(user, remember=remember); print('auth.py', 29, 'Done')
    session['user_id'] = user.id; print('auth.py', 30, 'Done')
    session['user_name'] = user.name; print('auth.py', 31, 'Done')
    session['user_email'] = email
    print('auth.py', 33, 'Before Done'); return redirect(url_for('main.index'))


@auth.route('/signup')
def signup():
    print('auth.py', 38, 'Before Done'); return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email'); print('auth.py', 43, 'Done')
    name = request.form.get('name'); print('auth.py', 44, 'Done')
    personal_id = request.form.get('personal_id'); print('auth.py', 45, 'Done')
    b_date = request.form.get('date'); print('auth.py', 46, 'Done')
    password = request.form.get('password'); print('auth.py', 47, 'Done')

    user = User.query.filter_by(
        email=email).first(); print('auth.py', 50, 'Done')  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists'); print('auth.py', 53, 'Done')
        print('auth.py', 54, 'Before Done'); return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email,
                    name=name,
                    password=generate_password_hash(password, method='sha256'),
                    personal_id=personal_id,
                    b_date=datetime.strptime(b_date, "%Y-%m-%d")); print('auth.py', 61, 'Done')

    # add the new user to the database
    db.session.add(new_user); print('auth.py', 64, 'Done')
    print('Before commit.'); print('auth.py', 65, 'Done')
    db.session.commit(); print('auth.py', 66, 'Done')
    print('After commit.'); print('auth.py', 67, 'Done')


    print('registered'); print('auth.py', 70, 'Done')

    print('auth.py', 72, 'Before Done'); return redirect(url_for('auth.login'))


@auth.route('/signup_ex')
def signup_ex():
    print('auth.py', 77, 'Before Done'); return render_template('signup_ex.html')


@auth.route('/signup_ex', methods=['POST'])
def signup_ex_post():
    email = request.form.get('email'); print('auth.py', 82, 'Done')
    name = request.form.get('name'); print('auth.py', 83, 'Done')
    password = request.form.get('password'); print('auth.py', 84, 'Done')

    user = User.query.filter_by(
        email=email).first(); print('auth.py', 87, 'Done')  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists'); print('auth.py', 90, 'Done')
        print('auth.py', 91, 'Before Done'); return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256')); print('auth.py', 94, 'Done')

    # add the new user to the database
    db.session.add(new_user); print('auth.py', 97, 'Done')
    print('Before commit.'); print('auth.py', 98, 'Done')
    db.session.commit(); print('auth.py', 99, 'Done')
    print('After commit.'); print('auth.py', 100, 'Done')


    print('auth.py', 103, 'Before Done'); return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user(); print('auth.py', 109, 'Done')
    session['user_id'] = -1; print('auth.py', 110, 'Done')
    print('auth.py', 111, 'Before Done'); return redirect(url_for('auth.login'))
