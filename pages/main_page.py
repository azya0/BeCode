from flask_login import login_user, logout_user, current_user, LoginManager, login_required
import flask_login
import flask

from data import db_session

blueprint = flask.Blueprint(
    'main_page',
    __name__,
    template_folder='templates',
    static_folder="static"
)


@blueprint.route('/')
def main_page():
    print(current_user)
    return flask.render_template("main.html", title='BeCode', postfix='', user=current_user)


@blueprint.route('/courses', methods=['GET'])
@blueprint.route('/courses/', methods=['GET'])
def courses():
    return flask.render_template("main.html", title='BeCode', postfix='Courses', user=current_user)
