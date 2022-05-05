import datetime
import sqlalchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import hashing as hsh
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "User"
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, unique=True, nullable=False)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    hash_password = sqlalchemy.Column(sqlalchemy.LargeBinary, nullable=False)
    salt = sqlalchemy.Column(sqlalchemy.LargeBinary, nullable=False)
    # password = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def check_password(self, password):
        return hsh.check_password(self.salt, self.hash_password, password)


class Passwords(SqlAlchemyBase):
    __tablename__ = "Passwords"
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, unique=True, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    cite = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class LoginForm(FlaskForm):
    login = EmailField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
