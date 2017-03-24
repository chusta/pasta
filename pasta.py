#!/usr/bin/env python
import os
from flask_script import Manager
from pasta import pasta

from werkzeug.serving import make_ssl_devcert, run_simple

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

manager = Manager(pasta)
port = int(os.environ.get('PORT', 8080))

@manager.command
def http():
    """ ! Run application (HTTP) """
    pasta.run(host="0.0.0.0", port=port)

@manager.command
def https():
    """ ! Run application (HTTPS) """
    cert_path = os.path.join(BASE_PATH, "app")
    if not os.path.exists(cert_path + ".key"):
        make_ssl_devcert(cert_path)

    run_simple("0.0.0.0", port, pasta,
        ssl_context=(cert_path + ".crt", cert_path + ".key")
    )

if __name__ == "__main__":
    manager.run()
