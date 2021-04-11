import flask

from data import db_session

blueprint = flask.Blueprint(
    'main_page',
    __name__,
    template_folder='templates'
)


@blueprint.route('/')
def main_page():
    return flask.render_template("main.html")

