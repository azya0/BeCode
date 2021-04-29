from flask_login import login_user, logout_user, current_user, LoginManager, login_required
from flask import Flask, make_response, jsonify, render_template
from classes.user import User
from data import db_session
from pages import main_page, sign

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = '#1000-7?vrDEFG22WEwefgRSDGf1243_zxc?'  # cursed
app.config["UPLOAD_FOLDER"] = "static/images"
login_manager = LoginManager()
login_manager.init_app(app)


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
    app.register_blueprint(main_page.blueprint)
    app.register_blueprint(sign.blueprint)
    app.run()


if __name__ == '__main__':
    main()
