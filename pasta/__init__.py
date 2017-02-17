import os
from flask import Flask

config_path = os.environ.get("CONFIG_PATH", "pasta.config.PastaConfig")

pasta = Flask(__name__)
pasta.config.from_object(config_path)
pasta.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024 # 5MB upload limit
pasta.config["PAGINATION"] = 10

from . import views
from . import login
