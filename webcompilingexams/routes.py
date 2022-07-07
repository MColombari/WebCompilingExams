from werkzeug.exceptions import HTTPException
from webcompilingexams import app, db
from webcompilingexams.form import LoginForm
from flask import render_template, redirect, url_for, flash

from webcompilingexams.models import User


@app.route('/')
def hello_world():
    return render_template("hello_page.html", title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User(id=int(form.matricola.data), name=form.nome.data, surname=form.cognome.data,
                    email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'User registrato con successo\n{user}"', 'success')
        return redirect(url_for('success'))

    return render_template('user_login.html', title='Login', form=form)


@app.route('/success')
def success():
    return render_template("user_login_succeded.html", title='Success')


@app.errorhandler(HTTPException)
def errorhandler(e):
    print(e.code + e.name + e.description)
    return e  # Da completare
