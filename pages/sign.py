import flask
from werkzeug.utils import redirect

from data import db_session
from form.registration import RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, LoginManager, login_required
from form.login import LoginForm
from classes.user import User

blueprint = flask.Blueprint(
    'sign',
    __name__,
    template_folder='templates'
)


@blueprint.route('/registration', methods=['GET', 'POST'])
@blueprint.route('/registration/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = User()
        user.login, user.hashed_password, user.email = [form.username.data, generate_password_hash(form.password.data),
                                                        form.email.data]
        session.add(user)
        session.commit()
        login_user(user)
        print(f'{form.username.data} successful signed in')
        return redirect('/')
    return flask.render_template('signin.html', title='BeCode: SignIn', postfix='Registration', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
@blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()  # Создание сессии.
        user = session.query(User).filter(User.login == form.username.data).first()
        if user is None:  # Если пользователя с подобный логином нет.
            return flask.render_template('signup.html', title='BeCode: SignUp', postfix='Login', form=form, exception='Wrong login')
        if check_password_hash(user.hashed_password, form.password.data):  # Проверка пароля.
            login_user(user, remember=form.remember_me.data)  # Вход.
            return redirect("/")  # Перенаправление на главную страницу.
        return flask.render_template('signup.html', title='BeCode: SignUp', postfix='Login', form=form, exception='Wrong password')
    return flask.render_template('signup.html', title='BeCode: SignUp', postfix='Login', form=form)


@blueprint.route('/test/user/<int:user_id>', methods=['GET'])
def get_user_id(user_id):
    db_sess = db_session.create_session()
    data = db_sess.query(User).get(user_id)
    if data:
        return flask.jsonify({'user': data.to_dict()})
    return flask.jsonify({'error': 'missed id'})
