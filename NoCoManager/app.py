import subprocess
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import os
import yaml
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object("config.Config")
app.secret_key = os.environ["SECRET_KEY"]
db = SQLAlchemy(app)


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
            return redirect(url_for("dashboard"))

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def dashboard():
    services = []
    for file in os.listdir("services"):
        if file.endswith(".yml"):
            with open(os.path.join("services", file), "r") as f:
                services.append(yaml.safe_load(f))
    return render_template("dashboard.html", services=services)


@app.route("/manage_service", methods=["POST"])
@login_required
def manage_service():
    if request.method == "POST":
        service_path = request.form.get("service_path")
        action = request.form.get("action")

        # Load the corresponding service file
        with open(f"services/{service_path}", "r") as f:
            service = yaml.safe_load(f)

        # Execute the command
        try:
            command = service["service_commands"][action]
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing {command}: {str(e)}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
