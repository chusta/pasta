import os
from flask import request, redirect, url_for, flash, render_template
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.security import check_password_hash

from pasta import pasta
from .database import session
from .models import User

@pasta.context_processor
def override_url_for():
    """
    hand-off to dated_url_for in order to perform browser
    cache busting for css files when modified
    """
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    """
    wraps url_for() for static files by appending a GET param of
    "?q={modifytime}" ; if non-static then stock url_for() is used
    """
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(pasta.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@pasta.route("/logout", methods=["GET"])
@login_required
def logout():
    """
    GET requests only.
    (login) logs out the user and redirects back to landing page
    """
    logout_user()
    return redirect(url_for("index"))

@pasta.route("/", methods=["GET", "POST"])
@login_required
def index():
    """
    GET and POST requests only.
    (login) landing page for the single-page application

    if an HTTP GET is received, then we display user images/captions
    if an HTTP POST is received, then we upload user images/captions
    """
    if request.method == "POST":
        return render_template("index.html", user=current_user)
    else:
        return render_template("index.html", user=current_user)

@pasta.route("/signup", methods=["GET", "POST"])
def signup():
    """
    GET and POST requests only.
    allow the user to sign up for an account

    if an HTTP GET is received, then we display the signup page
    if an HTTP POST is received, then we process user input
    """

@pasta.route("/login", methods=["GET", "POST"])
def login():
    """
    GET and POST requests only.
    views with the login_required decorator should go here

    if an HTTP GET is received, then we display the login page
    if an HTTP POST is received, then we process user input
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = session.query(User).filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash("Incorrect username or password", "danger")
            return redirect(url_for("login"))
        login_user(user)
        return redirect(request.args.get('next') or url_for("index"))
    else:
        return render_template("login.html", user=current_user)
