#!/usr/bin/env python
import os
from getpass import getpass

from flask_script import Manager
from werkzeug.security import generate_password_hash

from pasta import pasta
from pasta.database import Base, session
from pasta.models import User

manager = Manager(pasta)

R = lambda s: "\033[91m{}\033[0m".format(s)
G = lambda s: "\033[92m{}\033[0m".format(s)
Y = lambda s: "\033[93m{}\033[0m".format(s)

@manager.command
def test():
    """ Create test user """
    username, password = "testuser", "testpass"
    if session.query(User).filter_by(username=username).first():
        print Y("! Username already exists.")
        return
    user = User(username=username, password=generate_password_hash(password))
    session.add(user)
    session.commit()
    print G("+ User '{}' created.".format(username))

@manager.command
def user_create():
    """ Create user """
    username = raw_input("Username: ").strip()

    if session.query(User).filter_by(username=username).first():
        print Y("! Username already exists.")
        return

    password = getpass("Password: ").strip()
    if password != getpass("Confirm: ").strip():
        print Y("! Password does not match.")
        return

    user = User(
        username = username,
        password = generate_password_hash(password)
    )
    session.add(user)
    session.commit()
    print G("+ User '{}' created.".format(username))

@manager.command
def user_delete():
    """ Delete user """
    username = raw_input("Username: ").strip()
    if username:
        ans = read_input("Delete {}? [Y|y] ".format(username)).strip()
        if ans.lower() != "y":
            return

@manager.command
def start():
    """ ! Start application """
    port = int(os.environ.get('PORT', 8080))
    pasta.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    manager.run()
