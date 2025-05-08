

import sqlite3

# Initialize database connection
conn = sqlite3.connect('data/app.db', check_same_thread=False)
c = conn.cursor()

# Create tables
def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 email TEXT UNIQUE,
                 password TEXT
                 )''')

    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        category TEXT,
        type TEXT,
        date TEXT
    )''')

    conn.commit()

create_tables()  # Make sure the tables are created correctly


def insert_user(email, password):
    c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
    conn.commit()

def fetch_user(email):
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    return c.fetchone()

def insert_transaction(user_id, amount, category, type, date):
    c.execute('''INSERT INTO transactions (user_id, amount, category, type, date)
                 VALUES (?, ?, ?, ?, ?)''',
                 (user_id, amount, category, type, date))
    conn.commit()

def fetch_transactions(user_id):
    c.execute("SELECT id, amount, category, type, date FROM transactions WHERE user_id = ?", (user_id,))
    return c.fetchall()
