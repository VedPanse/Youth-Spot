from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Importing the database functions defined above

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
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = get_user(username)
        if user and user[2] == password:  # Check if user exists and passwords match
            return f"Welcome, {username}!"
        else:
            return "Invalid username or password."
    
    return return_error()

@app.route("/sign-up.html")
def load_sign_up(msg=''):
    return render_template("sign-up.html", msg=msg)

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            return load_sign_up(msg="Password mismatched")
        else:
            add_user(username, password)  # Add the user to the database
            return redirect("/events.html")
    
    return return_error()

# The rest of your Flask routes...

if __name__ == "__main__":
    app.debug = True
    app.run()
