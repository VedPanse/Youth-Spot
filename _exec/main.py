from flask import Flask, render_template, request, redirect
import sqlite3 as sq
import bcrypt

app = Flask(__name__)

# TABLE AND DB
def get_cursor():
    # Create a new SQLite connection and cursor for each request
    connection = sq.connect("user_data.db")
    cursor = connection.cursor()
    return connection, cursor

def clear_database(cursor, PIN) -> None:
    if PIN == 'Gliderport':
        cursor.execute("DELETE FROM user_credentials")
        cursor.connection.commit()

def create_table(cursor):
    try:
        cursor.execute("CREATE TABLE user_credentials (username TEXT, password TEXT, email_id TEXT)")
    except sq.OperationalError:
        pass


def add_data(cursor, username: str, password: str, email_id: str) -> int:
    cursor.execute("SELECT * FROM user_credentials WHERE username = ?", (username,))
    if cursor.fetchone() is not None:
        return -1

    cursor.execute("SELECT * FROM user_credentials WHERE email_id = ?", (email_id,))
    if cursor.fetchone() is not None:
        return 1

    cursor.execute("INSERT INTO user_credentials VALUES (?, ?, ?)", (username, password, email_id))
    cursor.connection.commit()
    return 0


def print_db(cursor) -> list[tuple]:
    rows = cursor.execute("SELECT username, password, email_id FROM user_credentials").fetchall()
    return rows


def read_data(cursor, username: str) -> list[tuple]:
    cursor.execute("SELECT password FROM user_credentials WHERE username = ?", (username,))
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
        username: str = request.form.get("username")
        password: str = request.form.get("password")
        return f"Username: {username}, Password: {password}"
    return render_template("ErrorTemplates/NotFound.html")


@app.route("/sign-up.html")
def load_sign_up(msg=''):
    return render_template("sign-up.html", msg=msg)


@app.route("/sign-up", methods=["POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            return load_sign_up(msg="Password mismatched")

        connection, cursor = get_cursor()
        create_table(cursor)
        add_response: int = add_data(cursor, username, password, email)

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
