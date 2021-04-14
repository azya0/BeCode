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
    return flask.render_template("main.html", title='BeCode', postfix='')


@blueprint.route('/courses', methods=['GET'])
@blueprint.route('/courses/', methods=['GET'])
def main_page():
    return flask.render_template("main.html", title='BeCode', postfix='Courses')
