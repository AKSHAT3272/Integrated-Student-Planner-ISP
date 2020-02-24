# main.py

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name, type=current_user.type)

@main.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html', name=current_user.name, email=current_user.email, type=current_user.type)

@main.route('/tracker')
@login_required
def tracker():
    return render_template('tracker.html', name=current_user.name, type=current_user.type)

@main.route('/home')
@login_required
def home():
    return render_template('home.html', name=current_user.name, type=current_user.type)

@main.route('/admin')
@login_required
def admin():
    type=current_user.type
    if type == 'admin':
      return render_template('admin.html', name=current_user.name, type=current_user.type)
    else:
      flash('Access denied')
      return redirect(url_for('main.home'))
