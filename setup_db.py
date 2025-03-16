import sqlite3
import bcrypt

# Connect to SQLite database (or create it)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create users table (if not exists)
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Create messages table (includes support for global messages)
cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT NOT NULL,
    recipient TEXT,  -- Can be NULL for broadcast messages
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Save and close the connection
conn.commit()
conn.close()

print("✅ Database setup completed! Users and messages tables updated.")
