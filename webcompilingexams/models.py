from webcompilingexams import db, login_manager
from flask_login import UserMixin


# db.create_all()
# db.drop_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    exam_started = db.Column(db.Boolean, unique=False)
    exam_finished = db.Column(db.Boolean, unique=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.name}', '{self.surname}', '{self.email}', '{self.exam_started}', " \
               f"'{self.exam_finished}')"
