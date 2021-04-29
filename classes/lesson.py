import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin


class Lesson(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'lesson'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    theme_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    topic = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    context = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    question_type = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    question = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    answers = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    task = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    right_answer = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    passed = sqlalchemy.Column(sqlalchemy.String, default='0')

