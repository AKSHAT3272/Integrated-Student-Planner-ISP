# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from itsdangerous import URLSafeTimedSerializer
from threading import Thread
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
from flask_mail import Message
from .models import User
from . import db, mail
from project import app
import os




ts = URLSafeTimedSerializer(os.urandom(24))


auth = Blueprint('auth', __name__)

def send_async_email(msg):
    with app.app_context():
        mail.send(msg)

def send_email(recipients,subject, html_body):
    msg = Message(subject,sender = 'akshat@isp.profleune.net', recipients=[recipients])
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[msg])
    thr.start()

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/contact')
def contact():
    return render_template('contactus.html')

@auth.route('/contact', methods=['POST'])
def contact_post():
    email = request.form.get('email')
    name = request.form.get('name')
    html = request.form.get('message')

    subject = 'Contact us inquiry Name:' + name + " Email:" + email
    send_email('akshatpatel@mail.adelphi.edu',subject,html)
    flash('Inquriry sent, someone will reachout soon. Thank you!')
    return redirect(url_for('main.aboutus'))




@auth.route('/reset')
def reset():
    return render_template('reset.html')

@auth.route('/reset', methods=['GET','POST'])
def reset_post():

    email = request.form.get('email')

    user = User.query.filter_by(email=email).first()

    if user:
        subject = "Password reset requested"
        token = ts.dumps(user.email, salt='recover-key')
        recover_url = url_for('auth.reset_with_token', token=token, _external=True)
        html=render_template('recover.html', recover_url=recover_url)
        send_email(user.email, subject, html)
        return redirect(url_for('auth.login'))

    #return render_template('reset.html')

    else:
        flash('Email does not exists')
        return redirect(url_for('auth.login'))

@auth.route('/reset/<token>', methods=['GET','POST'])
def reset_with_token(token):
    try:
        email= ts.loads(token, salt="recover-key", max_age = 86400)
    except:
        abort(404)

    form = PasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        password = request.form.get('password')
        user.password = generate_password_hash(password, method='pbkdf2:sha256')
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('reset_with_token.html', form=form, token=token)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

class PasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired()])
