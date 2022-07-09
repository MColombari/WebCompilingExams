from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.exceptions import HTTPException
from webcompilingexams import app, db
from webcompilingexams.form import LoginForm
from flask import render_template, redirect, url_for, flash, request

from webcompilingexams.models import User


@app.route('/')
def hello_world():
    return render_template("hello_page.html", title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Utente già loggato', 'success')
        return redirect(url_for('success'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User(id=int(form.matricola.data), name=form.nome.data, surname=form.cognome.data,
                    email=form.email.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, True)
        next_page = request.args.get('next')

        flash(f'User inserito con successo: "{user}"', 'success')
        if next_page:
            return redirect(next_page)  # Vai alla pagina a cui è cerrcato di andare senza il login.
        return redirect(url_for('success'))

    return render_template('user_login.html', title='Login', form=form)


@app.route('/success')
@login_required
def success():
    return render_template("user_login_succeded.html", title='Success')


@app.route('/logout')
def logout():
    logout_user()
    return render_template("hello_page.html", title='Logout')


@app.errorhandler(HTTPException)
def errorhandler(e):
    print(f"{e.code}, {e.name}, {e.description}")
    return e  # Da completare
