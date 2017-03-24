import os
import json

BASEPATH = os.path.abspath(os.path.dirname(__file__))
APP_PATH = os.path.dirname(BASEPATH)
DB_LOGIN = os.path.join(APP_PATH, "db_login")

# load json file with db credentials
with open(DB_LOGIN, "rb") as f:
    j = json.load(f)
    username = j["username"]
    password = j["password"]

class TestConfig(object):
    """
    test configuration
    """
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@127.0.0.1:5432/pasta-test".format(username, password)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY", "")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024 # 5MB
    PAGINATION = 10


class PastaConfig(object):
    """
    pasta configuration
    """
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@127.0.0.1:5432/pasta".format(username, password)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024 # 5MB
    PAGINATION = 10
