from flask import Flask, render_template, request, session, redirect, url_for
import secrets

# Create the Flask application
app = Flask(__name__)

# Details on the Secret Key: https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY
# NOTE: The secret key is used to cryptographically-sign the cookies used for storing
#       the session data.
app.secret_key = secrets.token_urlsafe(16)

@app.route("/")
def say_hello():
    return render_template('index.html')

@app.route("/login.html")
def load_login():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def set_email():
    if request.method == 'POST':
        # Save the form data to the session object
        session['email'] = request.form['email']
        return say_hello()

    return say_hello()


@app.route('/log_out')
def log_out():
    # Clear the email stored in the session object
    session.pop('email', default=None)
    return '<h1>Session deleted!</h1>'


if __name__ == '__main__':
    app.run()
