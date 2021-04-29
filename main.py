from flask_login import login_user, logout_user, current_user, LoginManager, login_required, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from form.registration import RegistrationForm
from flask import Flask, render_template
from werkzeug.utils import redirect
from classes.lesson import Lesson
from form.login import LoginForm
from classes.theme import Theme
from classes.lang import Lang
from classes.user import User
from data import db_session
import sqlite3
import flask
import json


app = Flask(__name__, static_folder="static", template_folder='templates')
app.config['SECRET_KEY'] = '#1000-7?vrDEFG22WEwefgRSDGf1243_zxc?'
app.config["UPLOAD_FOLDER"] = "static/images"
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/registration', methods=['GET', 'POST'])
@app.route('/registration/', methods=['GET', 'POST'])
def register():
    if not isinstance(current_user._get_current_object(), AnonymousUserMixin):
        return redirect('/')
    form = RegistrationForm()
    if form.validate_on_submit():
        con = sqlite3.connect('db/courses.db')
        cur = con.cursor()
        if form.username.data in map(lambda x: x[0], cur.execute('''SELECT login FROM users''').fetchall()):
            return flask.render_template('signup.html', title='BeCode: SignUp',
                                         postfix='Registration', form=form, user=current_user, error_ex='Login already exist')
        elif form.email.data in map(lambda x: x[0], cur.execute('''SELECT email FROM users''').fetchall()):
            return flask.render_template('signup.html', title='BeCode: SignUp',
                                         postfix='Registration', form=form, user=current_user, error_ex='Email already exist')
        session = db_session.create_session()
        user = User()
        user.login, user.hashed_password, user.email = [form.username.data, generate_password_hash(form.password.data.lower()),
                                                        form.email.data]
        session.add(user)
        session.commit()
        login_user(user)
        print(f'{form.username.data} successful signed in')
        return redirect('/courses')
    return flask.render_template('signup.html', title='BeCode: SignUp',
                                 postfix='Registration', form=form, user=current_user, error_ex='')


@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # if current_user:
    #     return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.login == form.username.data).first()
        if user is None:
            return flask.render_template('signin.html', title='BeCode: SignIn', postfix='Login',
                                         form=form, exception='Wrong login', user=current_user)
        if check_password_hash(user.hashed_password, form.password.data.lower()):
            login_user(user, remember=form.remember_me.data)
            return redirect("/courses")
        return flask.render_template('signin.html', title='BeCode: SignIn', postfix='Login', form=form,
                                     exception='Wrong password', user=current_user)
    return flask.render_template('signin.html', title='BeCode: SignIn',
                                 postfix='Login', form=form, user=current_user)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/test/user/<int:user_id>', methods=['GET'])
def get_user_id(user_id):
    db_sess = db_session.create_session()
    data = db_sess.query(User).get(user_id)
    if data:
        return flask.jsonify({'user': data.to_dict()})
    return flask.jsonify({'error': 'missed id'})


@app.route('/')
def main_page():
    return flask.render_template("main.html", title='BeCode', postfix='', user=current_user)


@app.route("/top/")
@app.route("/top")
def top():
    session = db_session.create_session()
    user_list = sorted(session.query(User).all(), key=lambda x: x.score, reverse=True)
    return flask.render_template("top.html", title='Becode: Top', postfix='Top', users=enumerate(user_list), user=current_user)


@app.route('/courses', methods=['GET'])
@app.route('/courses/', methods=['GET'])
@login_required
def courses():
    db_sess = db_session.create_session()
    langs = db_sess.query(Lang).all()
    data = [elm.to_dict()['name'] for elm in langs]
    return flask.render_template("courses.html", title='BeCode: Courses', postfix='Courses', user=current_user,
                                 courses=data)


@app.route('/profile', methods=['GET', 'POST'])
@app.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    return flask.render_template("profile.html", title='BeCode: Profile', postfix='Profile', user=current_user, courses=current_user.courses.split(", "))


@app.route('/courses/<string:name>', methods=['GET'])
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


@app.route('/courses/<string:name>/<int:theme_id>/<int:id>', methods=['GET', 'POST'])
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


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", title='BeCode: Error 404', postfix='Error 404', user=current_user), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("error.html", title='BeCode: Error 500', postfix='Error 500', user=current_user), 500


def main():
    db_session.global_init("db/courses.db")
    app.run()


if __name__ == '__main__':
    main()
