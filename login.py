import streamlit as st
import sqlite3

# Function to create a database connection
def get_db_connection():
    conn = sqlite3.connect("users.db")
    return conn

# Function to check user credentials
def check_login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Function to register a new user
def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        st.success("✅ Registration successful! You can now log in.")
    except sqlite3.IntegrityError:
        st.error("❌ Username already exists! Try another.")
    finally:
        conn.close()

# Streamlit Login Page
def login():
    st.title("🔐 Login Page")

    # Initialize session state for login
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # Tabs for login and registration
    tab1, tab2 = st.tabs(["Login", "Register"])

    # Login Tab
    with tab1:
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")

        if st.button("Login"):
            if check_login(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username  # Store username in session
                st.success("✅ Logged in successfully!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials! Try again.")

    # Registration Tab
    with tab2:
        new_username = st.text_input("👤 Choose a Username")
        new_password = st.text_input("🔑 Choose a Password", type="password")

        if st.button("Register"):
            if new_username and new_password:
                register_user(new_username, new_password)
            else:
                st.error("❌ Please fill in both fields.")
