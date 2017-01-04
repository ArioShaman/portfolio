from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import basedir
from flask.ext.mail import Mail


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'ariosha6',
	MAIL_PASSWORD = '5005abcd',
))

mail = Mail(app)
lm = LoginManager()
lm.init_app(app)

from app import views, models,admin