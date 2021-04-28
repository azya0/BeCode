from flask_login import login_user, logout_user, current_user, LoginManager, login_required
from classes.courses import Courses
from classes.course import Course
from classes.lesson import Lesson
from classes.user import User
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
    return flask.render_template("courses.html", title='BeCode: Courses', postfix='Courses', user=current_user,
                                 courses=Courses())


@blueprint.route('/profile', methods=['GET', 'POST'])
@blueprint.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    session = db_session.create_session()
    courses = [session.query(Course).filter(Course.id == int(course_id)).all()[0] for course_id in current_user.courses.split(", ") if course_id.strip() != '']
    return flask.render_template("profile.html", title='BeCode: Profile', postfix='Profile', user=current_user, courses=courses)


@blueprint.route('/courses/<string:name>', methods=['GET'])
@login_required
def lesson(name: str):
    try:
        Lesson(name.lower()).get()
    except IndexError:
        flask.abort(404)
    data = {
        j: [Lesson.passed_part(name, int(j.split('.')[0]), i, current_user.id) for i in
         range(1, len(Lesson(name.lower()).list(Lesson(name.lower()).get()[int(j.split('.')[0]) - 1])) + 1)]
        for j in Lesson(name.lower()).get()
    }
    data = {i: round(data[i].count(True) / len(data[i]) * 100) for i in data}
    return flask.render_template("main_course_page.html", title=f'BeCode: {name.capitalize()}',
                                 postfix=name.capitalize(), user=current_user, topic=Lesson(name.lower()),
                                 passed=data)


@blueprint.route('/courses/<string:name>/<int:lesson>/<int:part>', methods=['GET', 'POST'])
@login_required
def part(name: str, lesson: int, part: int):
    def get_kwargs(**add):
        global data, kwargs
        with open(f'courses/{name.lower()}/{Courses().get_list_of_courses(name)[lesson - 1]}/{part}.json') as file:
            data = json.loads(file.read())
        current_lesson = Lesson(name.lower())
        kwargs = {'title': f'BeCode: {name.capitalize()}',
                  'postfix': name.capitalize(),
                  'topic': Lesson(name.lower()),
                  'lesson': lesson,
                  'data': data,
                  'user': current_user,
                  'passed': current_user.id in data['passed'],
                  'part': len(current_lesson.list(current_lesson.get()[lesson - 1])),
                  'cur_part': part,
                  'passed_parts': [Lesson.passed_part(name, lesson, i, current_user.id) for i in range(1, len(current_lesson.list(current_lesson.get()[lesson - 1])) + 1)],
                  'wrong_answer': '',
                  **add}
        return data, kwargs

    data, kwargs = get_kwargs()
    if flask.request.method == 'GET':
        return flask.render_template("course_page.html", **kwargs)
    elif flask.request.method == 'POST':
        user_answer = flask.request.form.getlist('answer')
        if user_answer and user_answer[0] == data['right_answer']:
            with open(f'courses/{name.lower()}/{Courses().get_list_of_courses(name)[lesson - 1]}/{part}.json') as file:
                new_data = json.loads(file.read())
                if current_user.id not in new_data['passed']:
                    new_data['passed'] += [current_user.id]
                    con = sqlite3.connect("db/users.db")
                    cur = con.cursor()
                    cur.execute(f'''
                    UPDATE users
                    SET score = score + 1
                    WHERE id = {current_user.id}
                    ''')
                    con.commit()
                    con.close()
            with open(f'courses/{name.lower()}/{Courses().get_list_of_courses(name)[lesson - 1]}/{part}.json',
                      'w') as file:
                json.dump(new_data, file)
        elif user_answer and user_answer[0] != data['right_answer']:
            kwargs['wrong_answer'] = user_answer[0]
            return flask.render_template("course_page.html", **kwargs)
        else:
            print(f'{current_user.login} уже прошёл этот урок!')
        data, kwargs = get_kwargs()
        return flask.render_template("course_page.html", **kwargs)
