import streamlit as st
import pandas as pd
from database import conn


def show():
    st.header("📤 Upload CSV Transactions")

    user = st.session_state.user
    if not user:
        st.warning("You must be logged in to upload transactions.")
        return

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)

            required_columns = {"amount", "category", "type", "date"}
            if not required_columns.issubset(df.columns):
                st.error(f"CSV must contain these columns: {', '.join(required_columns)}")
                return

            df = df.dropna(subset=["amount", "category", "type", "date"])
            df["type"] = df["type"].str.lower()

            if not df["type"].isin(["income", "expense"]).all():
                st.error("Column 'type' must only contain 'income' or 'expense'.")
                return

            preview = st.dataframe(df.head(), use_container_width=True)

            if st.button("📥 Import Transactions"):
                c = conn.cursor()
                for _, row in df.iterrows():
                    c.execute('''INSERT INTO transactions (user_id, amount, category, type, date)
                                 VALUES (?, ?, ?, ?, ?)''',
                              (user["user_id"], row["amount"], row["category"], row["type"], row["date"]))
                conn.commit()
                st.success(f"{len(df)} transactions imported successfully!")

        except Exception as e:
            st.error(f"Error reading file: {e}")
