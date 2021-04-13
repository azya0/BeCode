import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    courses = sqlalchemy.Column(sqlalchemy.String, default='')
    banned = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
