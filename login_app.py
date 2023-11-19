import streamlit as st
import subprocess

# Replace these credentials with your own
USERNAME = 'your_username'
PASSWORD = 'your_password'

def login():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login") and username == USERNAME and password == PASSWORD:
        st.success("Logged in successfully!")
        return True
    return False

def main():
    st.title("Login Page")
    if login():
        st.text("Redirecting to Graph Page...")
        subprocess.run(["streamlit", "run", "graph_app.py"])

if __name__ == "__main__":
    main()
