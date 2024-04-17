from flask import Flask, render_template, request
import os
import time
import stat

app = Flask(__name__)


@app.route("/")
@app.route("/index.html")
def start_session():
    return render_template("index.html")

@app.route("/log-in.html")
def load_log_in():
    return render_template("log-in.html")


@app.route("/log-in", methods=["GET", "POST"])
def log_in():
    if request.method == "POST":
        username: str = request.form.get("username")
        password: str = request.form.get("password")
        return f"Username: {username}, Password: {password}"
    return render_template("ErrorTemplates/NotFound.html")

@app.route("/sign-up.html")
def load_sign_up():
    return render_template("sign-up.html")


@app.route("/events.html")
def load_events():
    return render_template("events.html")


if __name__ == "__main__":
    app.run(debug=True)
