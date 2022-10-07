import logging
import os
from datetime import datetime, timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

# Secret Key, generated randomly.
app.config['SECRET_KEY'] = '9c986a8dac94804409f30ecf62c2ce22'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'  # Database will be created in the app directory.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable signal after object modification.
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'registration'  # Page to redirect the user if is not registered.
login_manager.login_message = 'Per eccedere a questa pagina è encessario registrarsi'  # Message to flash.
login_manager.login_message_category = 'danger'  # Type of message to flash.

# Logging
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

ICON_FOLDER = os.path.join('static', 'icon')
app.config['UPLOAD_FOLDER'] = ICON_FOLDER

QUESTION_TYPE = {0: 'Domanda a risposta aperta', 1: 'Domanda a risposta multipla',
                 2: 'Programmazione Java', 3: 'Programmazione Python'}
CHARACTER_SEPARATOR = '\n'
ADMIN_ID = 1000000

DATE = str((datetime.today() + timedelta(hours=2)).strftime('%Y / %m / %d'))
DIR_DATE = str((datetime.today() + timedelta(hours=2)).strftime('%Y_%m_%d'))

from webcompilingexams import routes
