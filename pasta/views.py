import os
import hashlib
import uuid
from flask import request, redirect, url_for, flash, render_template
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.security import check_password_hash,  generate_password_hash
from werkzeug.utils import secure_filename

import magic
from pasta import pasta
import database
import models

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

@pasta.route("/", methods=["GET"])
@pasta.route("/<int:page>", methods=["GET"])
@login_required
def index(page=1):
    """
    GET requests only.
    (login) landing page for the single-page application
    """
    images = (
        models.Image.query
        .filter_by(user_id=current_user.id)
        .paginate(page, pasta.config["PAGINATION"])
    )
    # the user has no images ; send to upload page
    if images.count() <= 0:
        return render_template("upload.html", user=current_user)

    return render_template("index.html", user=current_user, images=images)

@pasta.route("/image/<filehash>", methods=["GET", "POST"])
@login_required
def image(filehash):
    return filehash

@pasta.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    """
    GET and POST requests only.
    (login) upload images limited to the MAX_CONTENT_LENGTH config

    if an HTTP GET is received, then we display the signup page
    if an HTTP POST is received, then we process user input
    """
    if request.method == "POST":
        upload_file = request.files.get("fileToUpload")
        if upload_file:
            data = upload_file.read()
            mime = magic.Magic(mime=True).from_buffer(data)
            sha256 = hashlib.sha256(data).hexdigest()

            # filename used as initial caption (140-char limit)
            name = secure_filename(upload_file.filename[:140]).strip()

            # check if current user already has an image with same sha256
            has_item = database.session.query(models.Image).filter_by(
                user_id = current_user.id,
                sha256 = sha256
            ).first()
            if has_item:
                return render_template("upload.html", user=current_user)

            # check if the file content is actually an image
            valid_mimes = [ "image/jpeg", "image/png", "image/gif" ]
            if not mime in valid_mimes:
                return render_template("upload.html", user=current_user)

            image = models.Image(
                data = data,
                caption = name,
                sha256 = sha256,
                user_id = current_user.id
            )
            database.session.add(image)
            database.session.commit()
    return render_template("upload.html", user=current_user)

@pasta.route("/signup", methods=["GET", "POST"])
def signup():
    """
    GET and POST requests only.
    allow the user to sign up for an account

    if an HTTP GET is received, then we display the signup page
    if an HTTP POST is received, then we process user input
    """
    if request.method == "GET" and current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        has_user = database.session.query(models.User).filter_by(username=username).first()
        if has_user:
            flash("Username already exists.", "danger")
            return redirect(url_for("signup"))

        if password != confirm:
            flash("Password does not match.", "danger")
            return redirect(url_for("signup"))

        # unique username and password/confirm matches ; add to db
        user = models.User(
            username = username,
            password = generate_password_hash(password)
        )
        database.session.add(user)
        database.session.commit()
        flash("Account successfully created.", "info")
        return redirect(url_for("login"))
    else:
        return render_template("signup.html", user=current_user)

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
        user = database.session.query(models.User).filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash("Incorrect username or password.", "danger")
            return redirect(url_for("login"))
        login_user(user)
        return redirect(request.args.get('next') or url_for("index"))
    else:
        return render_template("login.html", user=current_user)
