from flask import redirect, url_for, request
from flask_login import login_user, logout_user

from . import api
from app.models import User


@api.route('/login', methods=['POST'])
def login():
    login_user(User.query.get(1), remember=True)
    return redirect(url_for('main.index'))


@api.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('main.login'))
