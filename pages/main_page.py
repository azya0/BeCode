from flask_login import login_user, logout_user, current_user, LoginManager, login_required
from classes.courses import Courses
from classes.lesson import Lesson
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


@blueprint.route('/courses', methods=['GET'])
@blueprint.route('/courses/', methods=['GET'])
@login_required
def courses():
    return flask.render_template("courses.html", title='BeCode: Courses', postfix='Courses', user=current_user,
                                 courses=Courses())


@blueprint.route('/profile', methods=['GET'])
@blueprint.route('/profile/', methods=['GET'])
@login_required
def profile():
    return flask.render_template("profile.html", title='BeCode: Profile', postfix='Profile', user=current_user)


@blueprint.route('/courses/<string:name>', methods=['GET'])
@login_required
def lesson(name: str):
    return flask.render_template("main_course_page.html", title=f'BeCode: {name.capitalize()}',
                                 postfix=name.capitalize(), user=current_user, topic=Lesson(name.lower()))


@blueprint.route('/courses/<string:name>/<int:lesson>', methods=['GET', 'POST'])
@login_required
def part(name: str, lesson: int):
    def get_kwargs(**add):
        global data, kwargs
        with open(f'courses/{name.lower()}/{Courses().get_list_of_courses(name)[lesson - 1]}/task.json') as file:
            data = json.loads(file.read())
        kwargs = {'title': f'BeCode: {name.capitalize()}',
                  'postfix': name.capitalize(),
                  'topic': Lesson(name.lower()),
                  'lesson': lesson,
                  'data': data,
                  'user': current_user,
                  'passed': current_user.id in data['passed'],
                  **add}
        return data, kwargs

    data, kwargs = get_kwargs()
    if flask.request.method == 'GET':
        return flask.render_template("course_page.html", **kwargs)
    elif flask.request.method == 'POST':
        user_answer = flask.request.form.getlist('answer')
        if user_answer and user_answer[0] == data['right_answer']:
            with open(f'courses/{name.lower()}/{Courses().get_list_of_courses(name)[lesson - 1]}/task.json') as file:
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
            with open(f'courses/{name.lower()}/{Courses().get_list_of_courses(name)[lesson - 1]}/task.json',
                      'w') as file:
                json.dump(new_data, file)
        else:
            print(f'{current_user.login} уже прошёл этот урок!')
        data, kwargs = get_kwargs()
        return flask.render_template("course_page.html", **kwargs)
