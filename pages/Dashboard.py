import streamlit as st
import pandas as pd
import plotly.express as px
from database import conn

def show():
    st.header("📊 Dashboard Overview")

    user = st.session_state.user
    if not user:
        st.warning("You must be logged in to view the dashboard.")
        return

    # Fetch the most recent transactions
    c = conn.cursor()
    c.execute("SELECT amount, category, type, date FROM transactions WHERE user_id = ?", (user["user_id"],))
    data = c.fetchall()

    if not data:
        st.info("No transactions to show. Add some first.")
        return

    # Display fetched data for debugging
    print("Fetched Data for Dashboard:", data)

    df = pd.DataFrame(data, columns=["Amount", "Category", "Type", "Date"])
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=False, infer_datetime_format=True, errors='coerce')
    df = df.dropna(subset=["Date"])

    # Calculate totals
    total_income = df[df["Type"] == "income"]["Amount"].sum()
    total_expense = df[df["Type"] == "expense"]["Amount"].sum()
    balance = total_income - total_expense

    # Debugging the totals
    print(f"Total Income: {total_income}, Total Expense: {total_expense}, Balance: {balance}")

    # Summary cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"{total_income:,.0f} FCFA", delta=None)
    col2.metric("Total Expenses", f"{total_expense:,.0f} FCFA", delta=None)
    col3.metric("Balance", f"{balance:,.0f} FCFA", delta=None)

    st.markdown("---")

    # Pie Chart - Expense Breakdown by Category
    st.subheader("💸 Expenses by Category")
    expense_df = df[df["Type"] == "expense"]
    if not expense_df.empty:
        pie_chart = px.pie(expense_df, names='Category', values='Amount', title='Expense Distribution')
        st.plotly_chart(pie_chart, use_container_width=True)
    else:
        st.info("No expenses to show pie chart.")

    # Line Chart - Income and Expense Over Time
    st.subheader("📅 Income & Expense Over Time")
    df_grouped = df.groupby(["Date", "Type"])["Amount"].sum().reset_index()
    line_chart = px.line(df_grouped, x="Date", y="Amount", color="Type", markers=True)
    st.plotly_chart(line_chart, use_container_width=True)
