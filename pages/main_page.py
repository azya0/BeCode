from flask_login import login_user, logout_user, current_user, LoginManager, login_required
from classes.lesson import Lesson
from classes.theme import Theme
from classes.lang import Lang
from classes.user import User
from data import db_session
import sqlite3
import flask
import json

from data import db_session

blueprint = flask.Blueprint(
    'main_page',
    __name__,
    template_folder='templates',
    static_folder="static"
)


@blueprint.route('/')
def main_page():
    return flask.render_template("main.html", title='BeCode', postfix='', user=current_user)


@blueprint.route("/top/")
@blueprint.route("/top")
def top():
    session = db_session.create_session()
    user_list = sorted(session.query(User).all(), key=lambda x: x.score, reverse=True)
    return flask.render_template("top.html", title='Becode: Top', postfix='Top', users=enumerate(user_list), user=current_user)


@blueprint.route('/courses', methods=['GET'])
@blueprint.route('/courses/', methods=['GET'])
@login_required
def courses():
    db_sess = db_session.create_session()
    langs = db_sess.query(Lang).all()
    data = [elm.to_dict()['name'] for elm in langs]
    return flask.render_template("courses.html", title='BeCode: Courses', postfix='Courses', user=current_user,
                                 courses=data)


@blueprint.route('/profile', methods=['GET', 'POST'])
@blueprint.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    return flask.render_template("profile.html", title='BeCode: Profile', postfix='Profile', user=current_user, courses=current_user.courses.split(", "))


@blueprint.route('/courses/<string:name>', methods=['GET'])
@login_required
def lesson(name: str):
    def get_theme_length(theme_id):
        db_sess_new = db_session.create_session()
        lessons = [elm.to_dict() for elm in db_sess_new.query(Lesson).filter(Lesson.theme_id == theme_id)]
        return len(lessons)

    def first_theme_id(theme_id):
        db_sess_new = db_session.create_session()
        lessons = [elm.to_dict() for elm in db_sess_new.query(Lesson).filter(Lesson.theme_id == theme_id)]
        first_lesson = lessons[0]
        return first_lesson['id']

    def get_per_cent_of_passed_lessons(theme_id):
        db_sess_new = db_session.create_session()
        lessons = [elm.to_dict() for elm in db_sess_new.query(Lesson).filter(Lesson.theme_id == theme_id)]
        new_data = list(map(lambda x: str(current_user.id) in x['passed'], lessons))
        return round(new_data.count(True) / len(new_data) * 100)

    db_sess = db_session.create_session()
    themes = db_sess.query(Theme).all()
    topic = sorted([elm.to_dict() for elm in themes], key=lambda x: int(x['id']))
    return flask.render_template("main_course_page.html", title=f'BeCode: {name.capitalize()}',
                                 postfix=name.capitalize(), user=current_user, topic=topic,
                                 get_theme_length=get_theme_length, first_theme_id=first_theme_id,
                                 get_per_cent_of_passed_lessons=get_per_cent_of_passed_lessons)


@blueprint.route('/courses/<string:name>/<int:theme_id>/<int:id>', methods=['GET', 'POST'])
@login_required
def part(name: str, theme_id: int, id: int):
    def is_lennon_passed(lesson_id):
        db_sess = db_session.create_session()
        parts = db_sess.query(Lesson).filter(Lesson.id == lesson_id)
        current_lesson = [elm.to_dict() for elm in parts][0]
        return str(current_user.id) in current_lesson['passed'].split(',')

    def get_kwargs(**add):
        global data, kwargs
        db_sess = db_session.create_session()
        parts = db_sess.query(Lesson).filter(Lesson.theme_id == theme_id)
        lessons = [elm.to_dict() for elm in parts]
        current_lesson = list(filter(lambda x: x['id'] == id, lessons))[0]
        if current_lesson['task']:
            current_lesson['task'] = list(map(lambda x: x.strip(), current_lesson['task'].split('\\n')))
        passed_lesson = [elm["id"] for elm in lessons if is_lennon_passed(int(elm['id']))]
        kwargs = {'title': f'BeCode: {name.capitalize()}',
                  'postfix': name.capitalize(),
                  'lesson': theme_id,
                  'data': current_lesson,
                  'user': current_user,
                  'passed': is_lennon_passed(int(current_lesson['id'])),
                  'part': lessons,
                  'cur_part': id,
                  'passed_parts': passed_lesson,
                  'questions': list(map(str.strip, current_lesson['answers'].split(','))) if current_lesson['answers'] else '',
                  'wrong_answer': '',
                  'wrong': False,
                  **add}
        return current_lesson, kwargs

    data, kwargs = get_kwargs()
    if flask.request.method == 'GET':
        return flask.render_template("course_page.html", **kwargs)
    elif flask.request.method == 'POST':
        if name not in current_user.courses.split(", "):
            session = db_session.create_session()
            curr = session.query(User).get(current_user.id)
            curr.courses = ", ".join([i for i in curr.courses.split(", ") + [name] if i.strip() != ''])
            session.commit()
        if data['question_type'] == 'question':
            user_answer = flask.request.form.getlist('answer')
            if user_answer and user_answer[0] == data['right_answer']:
                if not is_lennon_passed(id):
                    db_sess = db_session.create_session()
                    lesson = db_sess.query(Lesson).get(id)
                    lesson.passed += ',' + str(current_user.id)
                    db_sess.commit()
                    session = db_session.create_session()
                    curr = session.query(User).get(current_user.id)
                    curr.score += 1
                    session.commit()
            elif user_answer and user_answer[0] != data['right_answer']:
                kwargs['wrong_answer'] = user_answer[0]
                return flask.render_template("course_page.html", **kwargs)
            else:
                print(f'{current_user.login} уже прошёл этот урок!')
            data, kwargs = get_kwargs()
            return flask.render_template("course_page.html", **kwargs)
        else:
            user_answer = flask.request.form.get('answer')
            if user_answer and user_answer == data['right_answer']:
                if not is_lennon_passed(id):
                    db_sess = db_session.create_session()
                    lesson = db_sess.query(Lesson).get(id)
                    lesson.passed += ',' + str(current_user.id)
                    db_sess.commit()
                    session = db_session.create_session()
                    curr = session.query(User).get(current_user.id)
                    curr.score += 1
                    session.commit()
            elif user_answer and user_answer != data['right_answer']:
                kwargs['wrong'] = True
                return flask.render_template("course_page.html", **kwargs)
            data, kwargs = get_kwargs()
            return flask.render_template("course_page.html", **kwargs)
