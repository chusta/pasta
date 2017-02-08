from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, EqualTo

class SignupForm(FlaskForm):
    username = StringField("Username", [ Length(min=4, max=32) ])
    password = PasswordField("Input Password",
        [ DataRequired(), EqualTo("confirm", message="Password mismatch") ])
    confirm = PasswordField("Confirm Password")

class CommentForm(FlaskForm):
    comment = StringField("Comment", [ Length(min=2, max=140) ])
