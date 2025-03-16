import streamlit as st
import sqlite3
from datetime import datetime

# Function to get database connection
def get_db_connection():
    return sqlite3.connect("users.db", check_same_thread=False)

# Function to fetch registered users (excluding the current user)
def get_registered_users(current_user):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username != ?", (current_user,))
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users

# Function to send a direct or broadcast message
def send_message(sender, recipient, message):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # If recipient is "Everyone", store NULL (indicating a broadcast message)
    if recipient == "Everyone":
        cursor.execute("INSERT INTO messages (sender, recipient, message, timestamp) VALUES (?, NULL, ?, ?)", 
                       (sender, message, datetime.now()))
    else:
        cursor.execute("INSERT INTO messages (sender, recipient, message, timestamp) VALUES (?, ?, ?, ?)", 
                       (sender, recipient, message, datetime.now()))

    conn.commit()
    conn.close()

# Function to fetch messages (for a user or globally)
def get_messages(user):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sender, recipient, message, timestamp FROM messages
        WHERE recipient IS NULL OR recipient = ? OR sender = ?
        ORDER BY timestamp ASC
    """, (user, user))
    
    messages = cursor.fetchall()
    conn.close()
    return messages

# Streamlit Chat UI for Direct & Broadcast Messaging
def chat():
    """Private chat system with a broadcast option"""
    st.title("💬 Farmer Chat")

    if "username" not in st.session_state:
        st.warning("⚠️ You must be logged in to chat.")
        return

    username = st.session_state["username"]

    # Get list of registered users (excluding the logged-in user)
    registered_users = get_registered_users(username)

    # Add "Everyone" as an option to broadcast messages
    registered_users.insert(0, "Everyone")

    # User selects a recipient (or Everyone)
    recipient = st.selectbox("📩 Select a recipient:", registered_users)

    if recipient:
        chat_title = "🌍 Public Chat" if recipient == "Everyone" else f"📩 Chat with {recipient}"
        st.subheader(chat_title)

        # Display previous messages (including global messages)
        messages = get_messages(username)
        for sender, recp, message, timestamp in messages:
            if recp is None:  # Global message
                with st.chat_message("assistant"):
                    st.write(f"🌍 **{sender}** (Broadcast): {message} ({timestamp})")
            elif sender == username or recp == username:
                with st.chat_message("user" if sender == username else "assistant"):
                    st.write(f"**{sender}**: {message} ({timestamp})")

        # Input for new message
        message_input = st.text_input("💬 Type your message:", key="chat_input")

        if st.button("Send"):
            if message_input.strip():
                send_message(username, recipient, message_input)
                st.rerun()  # Refresh chat to show the new message
            else:
                st.error("❌ Message cannot be empty.")
