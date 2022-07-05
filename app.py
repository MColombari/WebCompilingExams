# "docker build -t web_app ."
# "docker run -p 5000:5000 -v $(pwd):/app web_app"

from flask import Flask, render_template, redirect, url_for, flash
import os
from werkzeug.exceptions import HTTPException

from form import LoginForm

app = Flask(__name__)

# Chiave di sicurezza, abbiamo messo una string di caratteri casuali (hex).
app.config['SECRET_KEY'] = '9c986a8dac94804409f30ecf62c2ce22'


@app.route('/')
def hello_world():
    return render_template("hello_page.html", title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Ciao "{form.nome.data}"', 'success')
        return redirect(url_for('success'))
    return render_template('user_login.html', title='Login', form=form)


@app.route('/success')
def success():
    return render_template("user_login_succeded.html", title='Success')


@app.errorhandler(HTTPException)
def errorhandler(e):
    print(e.code + e.name + e.description)
    return e  # Da completare


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
