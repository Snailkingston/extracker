import streamlit as st
import sqlite3
import time

# Connect to DB
conn = sqlite3.connect('data/app.db', check_same_thread=False)
c = conn.cursor()

def get_user_transactions(user_id):
    c.execute("SELECT id, amount, category, type, date FROM transactions WHERE user_id = ?", (user_id,))
    return c.fetchall()

def delete_transaction(id):
    c.execute("DELETE FROM transactions WHERE id = ?", (id,))
    conn.commit()
    print(f"Transaction {id} deleted successfully")  # Debugging log

def show():
    st.title("✏️ Edit or 🗑️ Delete Transactions")

    user = st.session_state.user
    transactions = get_user_transactions(user["user_id"])

    if not transactions:
        st.info("No transactions available to delete.")
        return

    for tx in transactions:
        tx_id, amount, category, tx_type, date = tx
        with st.expander(f"Transaction #{tx_id}"):
            # Display transaction details
            st.write(f"**Amount:** {amount} FCFA")
            st.write(f"**Category:** {category}")
            st.write(f"**Type:** {tx_type.capitalize()}")
            st.write(f"**Date:** {date}")

            # Delete button layout
            col1 = st.columns(1)
            if st.button(f"Delete Transaction #{tx_id}", key=f"delete_{tx_id}"):
                # Call delete function
                delete_transaction(tx_id)
                st.warning(f"Transaction #{tx_id} deleted.")
                time.sleep(1)  # Optional delay to ensure UI refresh
                st.rerun()  # Trigger a page reload to reflect deleted transaction
