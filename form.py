from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError


def validate_ID():
    def _validate(form, field):
        for c in field.data:
            if not c.isnumeric():
                raise ValidationError("La matricola deve essere un numero")

    return _validate


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Campo dati obbligatorio'),
                                             Email(message='Email non valida')])
    nome = StringField('Nome', validators=[DataRequired(message='Campo dati obbligatorio')])
    cognome = StringField('Cognome', validators=[DataRequired(message='Campo dati obbligatorio')])
    matricola = StringField('Matricola', validators=[DataRequired(message='Campo dati obbligatorio'),
                                                     Length(min=6, max=6, message='La matrciola è formata da 6 numeri'),
                                                     validate_ID()])
    submit = SubmitField('Inizia esame')

    def get_attribute(self):
        return [self.email, self.nome, self.cognome, self.matricola, self.submit]
