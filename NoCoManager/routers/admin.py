import subprocess
from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask_login import login_required

import os
import yaml

default_bp = Blueprint('admin', __name__,url_prefix='/admin')

@default_bp.route("/dashboard")
@default_bp.route("/")
@login_required
def dashboard():
    services = []
    for file in os.listdir("services"):
        if file.endswith(".yml"):
            with open(os.path.join("services", file), "r") as f:
                services.append(yaml.safe_load(f))
    return render_template("admin/dashboard.jinja2", services=services)


@default_bp.route("/manage_service", methods=["POST"])
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