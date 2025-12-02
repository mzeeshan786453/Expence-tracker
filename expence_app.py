import streamlit as st
import sqlite3
import pandas as pd
import datetime

# --- Database Connection ---
def get_connection():
    return sqlite3.connect("expence.db")

# --- Create Table ---
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Expence_data(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            Date TEXT,
            Category TEXT,
            Amount REAL,
            Description TEXT,
            task_time TEXT
        )
    """)
    conn.commit()
    conn.close()

# --- Insert Data ---
def add_data(customer_name, Date, Category, Amount, Description, task_time):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Expence_data (customer_name, Date, Category, Amount, Description, task_time) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (customer_name, Date, Category, Amount, Description, task_time))
    conn.commit()
    conn.close()

# --- Get All Data ---
def get_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Expence_data")
    rows = cursor.fetchall()
    conn.close()
    return rows

# --- Update Data ---
def update_data(row_id, customer_name, Date, Category, Amount, Description, task_time):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Expence_data
        SET customer_name=?, Date=?, Category=?, Amount=?, Description=?, task_time=?
        WHERE id=?
    """, (customer_name, Date, Category, Amount, Description, task_time, row_id))
    conn.commit()
    conn.close()

# --- Delete Data ---
def delete_data(row_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Expence_data WHERE id=?", (row_id,))
    conn.commit()
    conn.close()

# --- Main App ---
def main():
    create_table()
    st.header("📊 Expense Tracker App (Streamlit + Power BI)")

    menu = ["Add Expense", "View & Edit", "Delete"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Expense":
        with st.form("form"):
            name = st.text_input("Enter Your Name")
            date = st.date_input("Date", value=datetime.date.today())
            category = st.multiselect("Category", ("Food", "Transport", "Shopping", "Grocery", "Other"))
            amount = st.number_input("Amount", min_value=0.0, format="%.2f")
            description = st.text_area("Description", height=100)
            time = st.time_input("Task Time")
            submit_btn = st.form_submit_button("Add Expense")

        if submit_btn:
            add_data(name, str(date), ",".join(category), amount, description, str(time))
            st.success("✅ Expense added successfully")

    elif choice == "View & Edit":
        expence_data = get_data()
        if expence_data:
            df = pd.DataFrame(expence_data, columns=["ID", "Name", "Date", "Category", "Amount", "Description", "Time"])
            st.dataframe(df)

            selected_id = st.selectbox("Select ID to Edit", df["ID"])
            row = df[df["ID"] == selected_id].iloc[0]

            with st.form("edit_form"):
                name = st.text_input("Edit Name", value=row["Name"])
                date = st.date_input("Edit Date", value=datetime.datetime.strptime(row["Date"], "%Y-%m-%d").date())
                category = st.text_input("Edit Category", value=row["Category"])
                amount = st.number_input("Edit Amount", value=row["Amount"], format="%.2f")
                description = st.text_area("Edit Description", value=row["Description"])
                time = st.text_input("Edit Time", value=row["Time"])
                save_btn = st.form_submit_button("Save Changes")

            if save_btn:
                update_data(selected_id, name, str(date), category, amount, description, time)
                st.success(f"✅ Record ID {selected_id} updated successfully")

        else:
            st.info("No expense data found.")

    elif choice == "Delete":
        expence_data = get_data()
        if expence_data:
            df = pd.DataFrame(expence_data, columns=["ID", "Name", "Date", "Category", "Amount", "Description", "Time"])
            st.dataframe(df)

            selected_id = st.selectbox("Select ID to Delete", df["ID"])
            if st.button("Delete"):
                delete_data(selected_id)
                st.warning(f"🗑️ Record ID {selected_id} deleted successfully")
        else:
            st.info("No expense data found.")

if __name__ == "__main__":
    main()
