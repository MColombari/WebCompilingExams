from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, Length, ValidationError

from webcompilingexams.models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Campo dati obbligatorio'),
                                             Email(message='Email non valida')])
    nome = StringField('Nome', validators=[DataRequired(message='Campo dati obbligatorio')])
    cognome = StringField('Cognome', validators=[DataRequired(message='Campo dati obbligatorio')])
    matricola = StringField('Matricola', validators=[DataRequired(message='Campo dati obbligatorio'),
                                                     Length(min=6, max=6, message='La matrciola è formata da 6 numeri')
                                                     ])

    def validate_email(self, field):
        flag = False

        for c in field.data:
            if not c.isnumeric():
                flag = True

        if flag or User.query.filter_by(email=field.data, id=int(self.matricola.data), restart_token=True).count() == 0:
            count = User.query.filter_by(email=field.data, restart_token=False).count()
            if not count == 0:
                raise ValidationError("Un utente con questa mail si è già registrato")

    def validate_matricola(self, field):
        for c in field.data:
            if not c.isnumeric():
                raise ValidationError("La matricola deve essere un numero")

        if User.query.filter_by(email=self.email.data, id=int(field.data), restart_token=True).count() == 0:
            count = User.query.filter_by(id=int(field.data), restart_token=False).count()
            if not count == 0:
                raise ValidationError("Un utente con questa matricola si è già registrato")

    def get_attribute(self):
        return [self.email, self.nome, self.cognome, self.matricola]


class AdminLoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message='Campo dati obbligatorio')])
    password = PasswordField('Password', validators=[DataRequired(message='Campo dati obbligatorio')])

    def get_attribute(self):
        return [self.name, self.password]


class QuestionForm(FlaskForm):
    text = TextAreaField('Answer')
    multiple_field_data = []  # Possible choice.
    multiple_field_selection = []  # Selected choice.


class AdminForm(FlaskForm):
    text = TextAreaField('Filter')
