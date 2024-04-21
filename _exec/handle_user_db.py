import sqlite3 as sq

# Parameters required for sign up form
# SIGN_UP_PARAMS = ['username', 'password', 'email_id']

connection: sq.Connection = sq.connect("user_data.db")
cursor = connection.cursor()

def create_table() -> None:
    try:
        cursor.execute("CREATE TABLE user_credentials (username TEXT, password TEXT, email_id TEXT)")
    except sq.OperationalError:
        pass

def add_data(username: str, password: str, email_id: str) -> int:
    # Adds data to the table user_credentials
    # If username already exists, it returns -1
    # If email_id already exists, it returns 1
    # Else, it returns 0

    cursor.execute("SELECT * FROM user_credentials WHERE username = ?", (username,))

    if cursor.fetchone() is not None:
        # Username already exists
        return -1

    cursor.execute("SELECT * FROM user_credentials WHERE email_id = ?", (email_id,))

    if cursor.fetchone() is not None:
        return 1

    cursor.execute("INSERT INTO user_credentials VALUES (?, ?, ?)", (username, password, email_id))
    connection.commit()
    return 0

def print_db() -> list[tuple]:
    rows = cursor.execute("SELECT username, password, email_id FROM user_credentials").fetchall()
    return rows

def read_data(username: str) -> list[tuple]:
    cursor.execute("SELECT password FROM user_credentials WHERE username = ?", (username,))
    rows = cursor.fetchall()
    return rows

# create_table()
# add_data("Ved_Panse", "jlk", "ved@example.com")
# add_data("Test", "test_p", "test@example.com")
# add_data("Other_user", "jlk", "ved@example.com")
# add_data("Ved_Panse", "jlk", "some@example.com")
#
# print(print_db())
# print(read_data("Test"))
