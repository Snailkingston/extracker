import streamlit as st
from database import create_tables
from auth import login_ui, signup_ui

# Initialize DB
create_tables()

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

# Page Navigation
st.set_page_config(page_title="Expense Tracker", layout="wide")

# Title for the app
st.title("📱 Mobile Expense Tracker")

# Only show the sidebar menu if the user is logged in
if st.session_state.logged_in:
    # When logged in, show full menu
    menu = ["Dashboard", "Add Transaction", "Summary", "Upload CSV", "Edit Transactions", "Logout"]
    choice = st.sidebar.selectbox("Navigation", menu)

    # Handle the page navigation based on the selected menu
    if choice == "Dashboard":
        from pages import Dashboard
        Dashboard.show()
    elif choice == "Add Transaction":
        from pages import Add_Transaction
        Add_Transaction.show()
    elif choice == "Upload CSV":
        from pages import Upload_CSV
        Upload_CSV.show()
    elif choice == "Summary":
        from pages import Summary
        Summary.show()
    elif choice == "Edit Transactions":
        from pages import Edit_Transactions
        Edit_Transactions.show()
    elif choice == "Logout":
        # Handle logout process
        st.session_state.logged_in = False
        st.session_state.user = None
        st.success("Logged out successfully")
else:
    # If not logged in, show login and sign up options only
    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Navigation", menu)

    # Show login and sign-up UI based on user's choice
    if choice == "Login":
        login_ui()
    elif choice == "Sign Up":
        signup_ui()

