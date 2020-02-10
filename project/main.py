# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html', name=current_user.name)

@main.route('/home')
@login_required
def home():
    return render_template('home.html', name=current_user.name)
