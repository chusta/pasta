#!/usr/bin/env python
import os
from flask_script import Manager
from pasta import pasta

manager = Manager(pasta)

R = lambda s: "\033[91m{}\033[0m".format(s)
G = lambda s: "\033[92m{}\033[0m".format(s)
Y = lambda s: "\033[93m{}\033[0m".format(s)

@manager.command
def run():
    """ ! Run application """
    port = int(os.environ.get('PORT', 8080))
    pasta.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    manager.run()
