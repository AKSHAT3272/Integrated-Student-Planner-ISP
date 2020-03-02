# init.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_httpauth import HTTPBasicAuth


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
auth = HTTPBasicAuth()
auth_token = HTTPBasicAuth()
app = Flask(__name__)
app.config.update(
	#DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='localhost',
	MAIL_PORT=587,
	MAIL_USE_TLS=True,
    	)
mail = Mail(app)
#def create_app():
    #app = Flask(__name__)
mail.init_app(app)
app.config['SECRET_KEY'] = 'p4K5pYXDm4McH53R5mB9tCYpy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import User

@login_manager.user_loader
def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)
#return app
