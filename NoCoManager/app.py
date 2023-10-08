import subprocess
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import os
import yaml
from dotenv import load_dotenv


from routers import default_bp, ticket_router, SERVICES

load_dotenv()

app = Flask(__name__)
app.config.from_object("config.Config")
app.secret_key = os.environ["SECRET_KEY"]


# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Replace with actual username and password check
        if (
            username == os.environ["ADMIN_USER"]
            and password == os.environ["ADMIN_PASSWORD"]
        ):
            user = User()
            user.id = username
            login_user(user)
            return redirect(url_for("admin.dashboard"))

    return render_template("admin/login.jinja2", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/")
def home():
    return render_template("index.jinja2", services=SERVICES)


app.register_blueprint(default_bp)
app.register_blueprint(ticket_router)

if __name__ == "__main__":
    app.run(host="192.168.42.254", ssl_context="adhoc", port=443, debug=True)
