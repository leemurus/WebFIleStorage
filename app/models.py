from flask_login import UserMixin

from app import db, login_manager
from werkzeug.security import check_password_hash


class BasicModelMixin:
    def commit_to_db(self):
        db.session.add(self)
        db.session.commit()


class User(UserMixin, db.Model, BasicModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(256))
    username = db.Column(db.String(100), unique=True, index=True)
    files = db.relationship('File', backref='owner', lazy='dynamic')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class File(db.Model, BasicModelMixin):
    uuid = db.Column(db.String, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    filename = db.Column(db.String(256))
    is_deleted = db.Column(db.Boolean, default=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
