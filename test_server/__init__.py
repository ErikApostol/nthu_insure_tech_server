from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager

db = SQLAlchemy()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'nthu_insure_tech_server'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
