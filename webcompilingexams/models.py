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
    exam_started = db.Column(db.Boolean, unique=False, default=False)
    exam_finished = db.Column(db.Boolean, unique=False, default=False)
    exam_checked = db.Column(db.Boolean, unique=False, default=False)
    restart_token = db.Column(db.Boolean, unique=False, default=False)
    index_question = db.Column(db.Integer, unique=False, default=0)
    questions = db.relationship('Question', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.id:06}', '{self.name}', '{self.surname}', '{self.email}')"


class Question(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    number = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String, nullable=False)
    options = db.Column(db.String, nullable=False, default="")
    answer = db.Column(db.String, nullable=False, default="")
    correct_answer = db.Column(db.String, nullable=False, default="")
    points = db.Column(db.Integer, nullable=False, default=0)
    question_weight = db.Column(db.Integer, nullable=False, default=1)
    compiler_output = db.Column(db.String, nullable=False, default="")
    test_output = db.Column(db.String, nullable=False, default="")
    test_output_summary = db.Column(db.String, nullable=False)
    test_output_icon = db.Column(db.String, nullable=False)

    # Tipi:
    #       0 - Open question.
    #       1 - Multiple choice question.
    #       2 - Compilation Java.
    #       3 - Compilation Python.

    def __repr__(self):
        return f"Question('{self.user_id:06}', '{self.number}', '{self.type}', '{self.text}', '{self.options}'," \
               f"'{self.correct_answer}', '{self.answer}', '{self.compiler_output}', '{self.test_output}')"
