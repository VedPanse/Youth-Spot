import sqlite3 as sq

connection: sq.Connection = sq.connect("user_data.db")

# Adding data
cursor = connection.cursor()

def create_table():
    global cursor
    cursor.execute("CREATE TABLE user_credentials (username TEXT, password TEXT)")

def add_data(username: str, password: str):
    cursor.execute(f"INSERT INTO user_credentials VALUES ('{username}', '{password}')")

# Read data
def print_db():
    rows = cursor.execute("SELECT username, password FROM user_credentials").fetchall()
    return rows

def read_data(username: str):
    # Use parameterized query to avoid SQL injection
    cursor.execute("SELECT password FROM user_credentials WHERE username = ?", (username,))
    # Fetch the result
    rows = cursor.fetchall()
    return rows


# Make it work
# create_table()
add_data("Ved_Panse", "jlk")
add_data("Test", 'test_p')

print(print_db())

print(read_data("Test"))
