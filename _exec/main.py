import bcrypt
import sqlite3 as sq
from flask import Flask, render_template, request, redirect, session
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_urlsafe(16)

# TABLE AND DB
def get_cursor():
    connection = sq.connect("user_data.db")
    cursor = connection.cursor()
    return connection, cursor

def clear_user_data(cursor, password) -> None:
    if password == 'Gliderport':
        cursor.execute("DELETE FROM user_credentials")
        cursor.connection.commit()

def create_table(cursor):
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS user_credentials (first_name TEXT, last_name TEXT, email TEXT, password TEXT, university TEXT, major TEXT, pid TEXT, year TEXT, ethnicity TEXT)")
    except sq.OperationalError:
        pass

def add_data(cursor, first_name: str, last_name: str, email: str, password: bytes, university: str, major: str, pid: bytes, year: str, ethnicity: str) -> int:

    cursor.execute("SELECT * FROM user_credentials WHERE email = ?", (email,))
    if cursor.fetchone() is not None:
        return 1

    cursor.execute("INSERT INTO user_credentials VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, email, password, university, major, pid, year, ethnicity))
    cursor.connection.commit()
    return 0

def read_data(cursor, identifier: str, is_email: bool = False) -> list[tuple]:
    if is_email:
        cursor.execute("SELECT password FROM user_credentials WHERE email = ?", (identifier,))

    rows = cursor.fetchall()
    return rows

# WEBPAGE HANDLING
@app.route("/")
@app.route("/index.html")
def start_session():
    return render_template("index.html")


@app.route("/log-in.html")
def load_log_in():
    return render_template("log-in.html")


@app.route("/log-in", methods=["POST"])
def log_in():
    if request.method == "POST":
        email: str = request.form.get("email")
        password: str = request.form.get("password")
        connection, cursor = get_cursor()

        hashed_password = read_data(cursor, email, is_email=True)
        connection.close()

        if hashed_password:
            hashed_password = hashed_password[0][0]
            password_in_bytes = password.encode("utf-8")

            if bcrypt.checkpw(password_in_bytes, hashed_password):
                session['email'] = email
                return render_template("events.html")
            else:
                return render_template("log-in.html", msg="Incorrect password")
        else:
            return render_template("log-in.html", msg="This email id is not registered")

    return render_template("ErrorTemplates/NotFound.html")

@app.route("/log-out")
def log_out():
    session.pop('email', default=None)
    return render_template('index.html')

@app.route("/profile.html")
def load_profile():
    if 'email' in session:
        email = session['email']
        connection, cursor = get_cursor()
        cursor.execute("SELECT * FROM user_credentials WHERE email = ?", (email,))
        user_data = cursor.fetchone()
        connection.close()

        if user_data:
            # Convert the user_data tuple to a dictionary with field names as keys
            user_dict = {
                'first_name': user_data[0],
                'last_name': user_data[1],
                'email': user_data[2],
                'university': user_data[4],
                'major': user_data[5],
                'pid': user_data[6],
                'year': user_data[7],
                'ethnicity': user_data[8]
            }

            # Pass user_dict to the profile template
            return render_template('profile.html', user_data=user_dict)
        else:
            return render_template('ErrorTemplates/NotFound.html', error="User data not found")
    else:
        return render_template('ErrorTemplates/NotFound.html', error="User not logged in")



@app.route("/sign-up.html")
def load_sign_up(msg=''):
    return render_template("sign-up.html", msg=msg)


@app.route("/sign-up", methods=["POST"])
def sign_up():
    if request.method == "POST":
        first_name: str = request.form.get("first_name")
        last_name: str = request.form.get("last_name")
        email: str = request.form.get("email")
        password: str = request.form.get("password")
        confirm_password: str = request.form.get("confirm_password")
        university: str = request.form.get("university")
        major: str = request.form.get("major")
        pid: str = request.form.get("pid")
        year: str = request.form.get("year")
        ethnicity: str = request.form.get("ethnicity")

        if password != confirm_password:
            return load_sign_up(msg="Password mismatched")

        connection, cursor = get_cursor()
        create_table(cursor)
        enc_password: bytes = encrypt(password)
        enc_pid: bytes = encrypt(pid)
        add_response: int = add_data(cursor, first_name, last_name, email, enc_password, university, major, enc_pid, year, ethnicity)

        if add_response == 0:
            connection.close()
            return redirect("/log-in.html")
        else:
            # Close the connection after using the cursor
            connection.close()
            return load_sign_up(msg="This email ID is already registered")

    return render_template("ErrorTemplates/NotFound.html")

@app.route("/search", methods=["POST"])
def search():
    if request.method == "POST":
        search_query: str = request.form.get("searchQuery")
        return search_query

    return render_template("ErrorTemplates/NotFound.html")


@app.route("/events.html")
def load_events():
    return render_template("events.html")


@app.route("/event-description.html")
def load_event_description():
    return render_template("event-description.html")


# ENCRYPTION EVENTS
def encrypt(password: str) -> bytes:
    password_in_bytes: bytes = password.encode("utf-8")
    salt: bytes = bcrypt.gensalt()
    hashed_password: bytes = bcrypt.hashpw(password_in_bytes, salt)
    return hashed_password


if __name__ == "__main__":
    app.run(debug=True)
