# "docker build -t web_app ."
# "docker run -p 5000:5000 -v $(pwd):/app web_app"

from flask import Flask, render_template, redirect, url_for, request, flash
import os
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)

# Chiave di sicurezza, abbiamo messo una string di caratteri casuali (hex).
app.config['SECRET_KEY'] = '9c986a8dac94804409f30ecf62c2ce22'

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

@app.route('/')
def hello_world():
  return render_template("hello_page.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = MyForm()
    if form.validate_on_submit():
        flash(f'Ciao "{form.name.data}"', 'success')
        return redirect('/success')
    return render_template('user_login.html', form=form)

@app.route('/success')
def success():
  return render_template("user_login_succeded.html")


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(debug=True, host='0.0.0.0', port=port)