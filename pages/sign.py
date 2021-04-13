import flask

from data import db_session
from form.registration import RegistrationForm

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
    return flask.render_template('signin.html', title='Registration', form=form)


@blueprint.route('/login')
@blueprint.route('/login/')
def login():
    return "log_page"
