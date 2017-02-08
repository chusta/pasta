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


class DevelopmentConfig(object):
    """
    postgresql development configuration
    """
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@127.0.0.1:5432/dev".format(username, password)
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY", "")


class ProductionConfig(object):
    """
    postgresql production configuration
    """
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@127.0.0.1:5432/prod".format(username, password)
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "")


class TestConfig(object):
    """
    postgresql test configuration
    """
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@127.0.0.1:5432/test".format(username, password)
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "")
