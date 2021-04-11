from flask import Flask, make_response, jsonify
from data import db_session
from pages import main_page, sign


app = Flask(__name__)
app.config['SECRET_KEY'] = '#1000-7?vrDEFG22WEwefgRSDGf1243_zxc?'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': f'Not found: {error}'}), 404)


def main():
    db_session.global_init("db/courses.db")
    db_session.global_init("db/users.db")
    app.register_blueprint(main_page.blueprint)
    app.register_blueprint(sign.blueprint)
    app.run()


if __name__ == '__main__':
    main()
