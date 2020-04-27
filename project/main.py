# main.py

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import db
from project import app
import os

UPLOAD_FOLDER = '/home/akshat/isp/project/static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','ical'}

main = Blueprint('main', __name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        #mycursor.execute('SELECT name FROM user')
        data = db.session.query('name FROM user').all()
        return render_template('admin.html', name=current_user.name, type=current_user.type, output_data = data)
    else:
      flash('Access denied')
      return redirect(url_for('main.home'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
       if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('main.home'))
       file = request.files['file']

       if file.filename == '':
           flash('No selected file')
           return redirect(url_for('main.home'))

       if file and allowed_file(file.filename):
           filename = secure_filename(file.filename)
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

      #f = request.files['file']
      #f.save(f.filename)
           flash('file uploaded successfully')
           return redirect(url_for('main.home'))
