#!/usr/bin/env python
import os
from flask_script import Manager
from pasta import pasta

manager = Manager(pasta)

@manager.command
def test():
    """ ? Test application """
    print "test"

@manager.command
def run():
    """ ! Run application """
    port = int(os.environ.get('PORT', 8080))
    pasta.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    manager.run()
