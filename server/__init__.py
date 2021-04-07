from flask import Flask; print('__init__.py', 1, 'Done')
from flask_sqlalchemy import SQLAlchemy; print('__init__.py', 2, 'Done')
from flask_login import LoginManager; print('__init__.py', 3, 'Done')

db = SQLAlchemy(); print('__init__.py', 5, 'Done')


def create_app():
    app = Flask(__name__); print('__init__.py', 9, 'Done')

    app.config['SECRET_KEY'] = 'nthu_insure_tech_server'; print('__init__.py', 11, 'Done')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'; print('__init__.py', 12, 'Done')
    app.config['UPLOAD_ROOT'] = '/tmp'; print('__init__.py', 13, 'Done')

    db.init_app(app); print('__init__.py', 15, 'Done')

    login_manager = LoginManager(); print('__init__.py', 17, 'Done')
    login_manager.login_view = 'auth.login'; print('__init__.py', 18, 'Done')
    login_manager.init_app(app); print('__init__.py', 19, 'Done')

    from models import User; print('__init__.py', 21, 'Done')

    @login_manager.user_loader
    def load_user(user_id):
        print('__init__.py', 25, 'Before Done'); return User.query.get(int(user_id))

    from auth import auth as auth_blueprint; print('__init__.py', 27, 'Done')
    app.register_blueprint(auth_blueprint); print('__init__.py', 28, 'Done')

    from main import main as main_blueprint; print('__init__.py', 30, 'Done')
    app.register_blueprint(main_blueprint); print('__init__.py', 31, 'Done')

    from forum import forum as forum_blueprint; print('__init__.py', 33, 'Done')
    app.register_blueprint(forum_blueprint); print('__init__.py', 34, 'Done')

    from file import file as file_blueprint; print('__init__.py', 36, 'Done')
    app.register_blueprint(file_blueprint); print('__init__.py', 37, 'Done')


    print('__init__.py', 40, 'Before Done'); return app


if __name__ == "__main__":
    app = create_app(); print('__init__.py', 44, 'Done')
    # db.create_all(app)
    app.debug = False; print('__init__.py', 46, 'Done')
    # https://stackoverflow.com/questions/14814201/can-i-serve-multiple-clients-using-just-flask-app-run-as-standalone
    app.run(host='0.0.0.0', port=80, ssl_context=('fullchain.pem', 'privkey.pem'), threaded=True); print('__init__.py', 48, 'Done')
    # app.run(host='0.0.0.0', port=80)
