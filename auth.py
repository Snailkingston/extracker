import streamlit as st
import bcrypt
from database import insert_user, fetch_user


# Hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


# Verify password
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())


# Signup UI
def signup_ui():
    st.subheader("Create an Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password != confirm:
            st.error("Passwords do not match.")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters.")
        else:
            hashed_pw = hash_password(password)
            try:
                insert_user(email, hashed_pw)
                st.success("Account created successfully! Please log in.")
            except:
                st.error("Email already exists. Try logging in.")


# Login UI
def login_ui():
    st.subheader("Login to Your Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = fetch_user(email)
        if user and verify_password(password, user[2]):
            st.session_state.logged_in = True
            st.session_state.user = {
                "user_id": user[0],
                "email": user[1]
            }
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid email or password.")
