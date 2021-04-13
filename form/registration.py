from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    username = StringField('Логин', [validators.Length(min=5, max=25)])
    email = StringField('Email', [validators.Email()])
    password = PasswordField('Пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Повторите пароль')
    submit = SubmitField('Зарегестрироваться')
    remember_me = BooleanField('Запомнить меня')
