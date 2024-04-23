import bcrypt
import sqlite3 as sq
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

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
        cursor.execute("CREATE TABLE IF NOT EXISTS user_credentials (full_name TEXT, email TEXT, password TEXT, university TEXT, major TEXT, pid TEXT, year TEXT)")
    except sq.OperationalError:
        pass

def add_data(cursor, full_name: str, email: str, password: bytes, university: str, major: str, pid: bytes, year: str) -> int:
    cursor.execute("SELECT * FROM user_credentials WHERE full_name = ?", (full_name,))
    if cursor.fetchone() is not None:
        return -1

    cursor.execute("SELECT * FROM user_credentials WHERE email = ?", (email,))
    if cursor.fetchone() is not None:
        return 1

    cursor.execute("INSERT INTO user_credentials VALUES (?, ?, ?, ?, ?, ?, ?)", (full_name, email, password, university, major, pid, year))
    cursor.connection.commit()
    return 0

def read_data(cursor, identifier: str, is_email: bool = False) -> list[tuple]:
    if is_email:
        cursor.execute("SELECT password FROM user_credentials WHERE email = ?", (identifier,))
    else:
        cursor.execute("SELECT password FROM user_credentials WHERE full_name = ?", (identifier,))
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
                return "Login successful"
            else:
                return render_template("log-in.html", msg="Incorrect password")
        else:
            return render_template("log-in.html", msg="Incorrect username / email")

    return render_template("ErrorTemplates/NotFound.html")



@app.route("/sign-up.html")
def load_sign_up(msg=''):
    return render_template("sign-up.html", msg=msg)


@app.route("/sign-up", methods=["POST"])
def sign_up():
    if request.method == "POST":
        full_name: str = request.form.get("full_name")
        email: str = request.form.get("email")
        password: str = request.form.get("password")
        confirm_password: str = request.form.get("confirm_password")
        university: str = request.form.get("university")
        major: str = request.form.get("major")
        pid: str = request.form.get("pid")
        year: str = request.form.get("year")

        if password != confirm_password:
            return load_sign_up(msg="Password mismatched")

        connection, cursor = get_cursor()
        create_table(cursor)
        enc_password: bytes = encrypt(password)
        enc_pid: bytes = encrypt(pid)
        add_response: int = add_data(cursor, full_name, email, enc_password, university, major, enc_pid, year)

        if add_response == 0:
            connection.close()
            return redirect("/events.html")
        elif add_response == -1:
            connection.close()
            return load_sign_up(msg="This username already exists")
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
