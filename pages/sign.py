import flask

from data import db_session

blueprint = flask.Blueprint(
    'sign',
    __name__,
    template_folder='templates'
)


@blueprint.route('/reg')
@blueprint.route('/reg/')
def register():
    return "reg_page"


@blueprint.route('/log')
@blueprint.route('/log/')
def login():
    return "log_page"
