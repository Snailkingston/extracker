import streamlit as st
from database import conn


def show():
    st.header("➕ Add Transaction")

    user = st.session_state.user
    if not user:
        st.warning("You must be logged in to add transactions.")
        return

    amount = st.number_input("Amount (FCFA)", min_value=0.0, step=100.0)
    category = st.text_input("Category (e.g., Food, Transport, Rent)")
    t_type = st.radio("Transaction Type", ("Expense", "Income"))
    date = st.date_input("Date")

    if st.button("Add Transaction"):
        if amount == 0 or not category:
            st.error("Please enter a valid amount and category.")
        else:
            c = conn.cursor()
            c.execute('''INSERT INTO transactions (user_id, amount, category, type, date)
                         VALUES (?, ?, ?, ?, ?)''',
                      (user["user_id"], amount, category, t_type.lower(), str(date)))
            conn.commit()
            st.success(f"{t_type} added successfully!")
