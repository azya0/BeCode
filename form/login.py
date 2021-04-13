from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', [validators.Length(min=5, max=25)])
    password = PasswordField('Пароль', [validators.DataRequired()])
    submit = SubmitField('Авторизоваться')
    remember_me = BooleanField('Запомнить меня')
