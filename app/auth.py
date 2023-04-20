import re

from flask import render_template, redirect, request
from flask_login import LoginManager, login_user, UserMixin
from flask_sqlalchemy import SQLAlchemy

from db import User, db
from password import password_to_hash, verify_password_hash

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = '/login'


def get_user(login_id, database_id=False):
    if database_id:
        return db.session.execute(db.select(User).filter_by(id=login_id)).scalar_one_or_none()
    return db.session.execute(db.select(User).filter_by(login_id=login_id)).scalar_one_or_none()


class LoginUser(UserMixin):
    def __init__(self, user_id: str, user: User = None):
        if user is not None:
            self.user = user
        else:
            self.user = get_user(user_id)
        self.id = self.user.id
        self.login_id = user_id
        self.username = self.user.username
        self.email = self.user.email
        self.password = self.user.password


@login_manager.user_loader
def user_loader(user_id):
    user = get_user(user_id, True)
    if user is None:
        return
    user = LoginUser(user_id, user)
    return user


def login():
    login_id = request.form["login_id"]
    password = request.form["password"]
    if get_user(login_id) is None:
        return False
    user = LoginUser(login_id)
    if verify_password_hash(password, user.password):
        login_user(user)
        return True
    return False


def register(data, db: SQLAlchemy):
    errors = []
    if data["password"] != data["password2"]:
        errors.append("Password Not Same")
    if len(data["login_id"]) < 3:
        errors.append("Login ID Too short")
    if get_user(data["login_id"]) is not None:
        errors.append("Login ID existed")
    if not re.fullmatch("^\S+@\S+\.\S+$", data["email"]):
        errors.append("Email invalid")
    if len(errors) > 0:
        return render_template("register.html", errors=errors)
    hashed = password_to_hash(data["password"])
    new_user = User(login_id=data["login_id"], password=hashed, username=data["username"], email=data["email"])
    db.session.add(new_user)
    db.session.commit()
    login_user(LoginUser(data["login_id"]))
    resp = redirect("/")
    return resp
