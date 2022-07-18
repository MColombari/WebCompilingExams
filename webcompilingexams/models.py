from webcompilingexams import db, login_manager
from flask_login import UserMixin


# db.create_all()
# db.drop_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    exam_started = db.Column(db.Boolean, unique=False)
    exam_finished = db.Column(db.Boolean, unique=False)
    questions = db.relationship('Question', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.name}', '{self.surname}', '{self.email}', '{self.exam_started}', " \
               f"'{self.exam_finished}')"


class Question(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    number = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)
    compiler_output = db.Column(db.String, nullable=False)
    test_output = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Question('{self.user_id}', '{self.number}', '{self.type}', '{self.text}', '{self.answer}', " \
               f"'{self.compiler_output}', '{self.test_output}')"