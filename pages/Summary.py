import streamlit as st
import sqlite3
import pandas as pd

def show():
    st.image("static/logo.png", width=150)  # adjust path/size as needed
    st.title("📊 Transaction Summary")

    user = st.session_state.get("user")
    if not user:
        st.error("Please log in to view your summary.")
        return

    # Filter by date range
    with st.expander("📅 Filter by Date Range"):
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")

    # Connect to DB and fetch data
    conn = sqlite3.connect("data/app.db")
    query = "SELECT category, type, amount, date FROM transactions WHERE user_id = ? AND date BETWEEN ? AND ?"
    df = pd.read_sql(query, conn, params=(user["user_id"], str(start_date), str(end_date)))
    conn.close()

    if df.empty:
        st.warning("No transactions found.")
        return

    df["amount"] = df["amount"].astype(float)

    # Group by category and type
    summary = (
        df.groupby(["category", "type"])
        .agg(Total_Amount=("amount", "sum"), Count=("amount", "count"))
        .reset_index()
    )

    # Show summary table
    st.markdown("### 📌 Summary by Category and Type")
    st.dataframe(summary, use_container_width=True)

    # Optional bar chart
    st.markdown("### 📈 Total Amount per Category")
    bar_data = summary.groupby("category")["Total_Amount"].sum().reset_index()
    st.bar_chart(bar_data.set_index("category"))
