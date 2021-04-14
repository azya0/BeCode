import flask
from werkzeug.utils import redirect

from data import db_session
from form.registration import RegistrationForm
from form.login import LoginForm

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
        return redirect('/success')
    return flask.render_template('signin.html', title='BeCode: SignIn', postfix='Registration', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
@blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return flask.render_template('signup.html', title='BeCode: SignUp', postfix='Login', form=form)
