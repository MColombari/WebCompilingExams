from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError

from webcompilingexams.models import User


def validate_email():
    def _validate(form, field):
        count = User.query.filter_by(email=field.data).count()
        if not count == 0:
            raise ValidationError("Un utente con questa mail si è già registrato")

    return _validate


def validate_ID():
    def _validate(form, field):
        for c in field.data:
            if not c.isnumeric():
                raise ValidationError("La matricola deve essere un numero")

        count = User.query.filter_by(id=int(field.data)).count()
        if not count == 0:
            raise ValidationError("Un utente con questa matricola si è già registrato")

    return _validate


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Campo dati obbligatorio'),
                                             Email(message='Email non valida'),
                                             validate_email()])
    nome = StringField('Nome', validators=[DataRequired(message='Campo dati obbligatorio')])
    cognome = StringField('Cognome', validators=[DataRequired(message='Campo dati obbligatorio')])
    matricola = StringField('Matricola', validators=[DataRequired(message='Campo dati obbligatorio'),
                                                     Length(min=6, max=6, message='La matrciola è formata da 6 numeri'),
                                                     validate_ID()])
    submit = SubmitField('Inizia esame')

    def get_attribute(self):
        return [self.email, self.nome, self.cognome, self.matricola, self.submit]
