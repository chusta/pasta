import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

pasta = Flask(__name__)
pasta.config.from_object("pasta.config.PastaConfig")
database = SQLAlchemy(pasta)

from . import views
from .models import User

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(pasta)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
