import os
from flask import Flask

pasta = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "pasta.config.DevelopmentConfig")
pasta.config.from_object(config_path)

from . import views
from . import login
