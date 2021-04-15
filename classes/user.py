import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin


class User(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    courses = sqlalchemy.Column(sqlalchemy.String, default='')
    avatar = sqlalchemy.Column(sqlalchemy.String, default='images/default.png')
    banned = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
