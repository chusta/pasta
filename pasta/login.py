from flask_login import LoginManager

from pasta import pasta
from .database import session
from .models import User

login_manager = LoginManager()
login_manager.init_app(pasta)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))
