from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
# Chiave di sicurezza, abbiamo messo una string di caratteri casuali (hex).
app.config['SECRET_KEY'] = '9c986a8dac94804409f30ecf62c2ce22'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'  # Il database verrà creato nella directory dell'app.
db = SQLAlchemy(app)  # Funziona come Room.
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Pagina a cui vado nel caso in cui l'utente cerchi accedere a una pagina senza
# aver fatto l'accesso.
login_manager.login_message = 'Per eccedere a questa pagina è encessario prima loggarsi'  # Messaggio mostrato.

from webcompilingexams import routes
