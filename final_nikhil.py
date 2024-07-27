# importing libraries

import mysql.connector
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import datetime

# connection banana

def database_connection():

    connection=mysql.connector.connect(host="localhost",user="root",password="12345678", database="expense_tracker")

    return connection

#1 expense add karna

def add_expense(date, category, amount, description):
    conn = database_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (%s, %s, %s, %s)",(date, category, amount, description))
    conn.commit()
    cursor.close()
    conn.close()
    
#2 view expenses

def view_expense():
    conn = database_connection()
    cur = conn.cursor()
    cur.execute("SELECT date, category, amount, description FROM expenses")
    rec = cur.fetchall()
    
    # Create a PrettyTable object
    table = PrettyTable()
    table.field_names = ["Date", "Category", "Amount ($)", "Description"]
    
    for row in rec:
        table.add_row([row[0], row[1], f"{float(row[2]):,.2f}", row[3]])
    
    # Close the database connection
    cur.close()
    conn.close()
    
    # Set table alignment and style
    table.align["Date"] = "l"
    table.align["Category"] = "l"
    table.align["Amount ($)"] = "r"
    table.align["Description"] = "l"
    table.horizontal_char = '*'
    table.vertical_char = '|'
    table.junction_char = '+'
    
    # Print the formatted table
    # print("\nHere are your expenses:")
    print(table)

#3 generate summary

def generate_summary():
    conn = database_connection()
    cur = conn.cursor()
    
    # Total expenses
    cur.execute("SELECT SUM(amount) FROM expenses")
    total_expense = cur.fetchone()[0]
    
    # Expenses by category
    cur.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    expense_by_category = cur.fetchall()
    
    # Maximum expense
    cur.execute("SELECT date, category, amount, description FROM expenses ORDER BY amount DESC LIMIT 1")
    max_expense = cur.fetchone()
    
    # Minimum expense
    cur.execute("SELECT date, category, amount, description FROM expenses ORDER BY amount ASC LIMIT 1")
    min_expense = cur.fetchone()
    
    cur.close()
    conn.close()
    
    # Display the summary in a readable format
    print("\n" + "="*40)
    print("   📊 Expense Summary Report 📊")
    print("="*40)
    
    # Total expenses
    print(f"Total Expenses: ${total_expense:,.2f}")
    
    # Expenses by category
    print("\nExpenses by Category:")
    table_category = PrettyTable()
    table_category.field_names = ["Category", "Amount ($)"]
    for category, amount in expense_by_category:
        table_category.add_row([category, f"{amount:,.2f}"])
    print(table_category)
    
    # Maximum expense
    print("\nMaximum Expense:")
    table_max = PrettyTable()
    table_max.field_names = ["Date", "Category", "Amount ($)", "Description"]
    table_max.add_row([max_expense[0], max_expense[1], f"{max_expense[2]:,.2f}", max_expense[3]])
    print(table_max)
    
    # Minimum expense
    print("\nMinimum Expense:")
    table_min = PrettyTable()
    table_min.field_names = ["Date", "Category", "Amount ($)", "Description"]
    table_min.add_row([min_expense[0], min_expense[1], f"{min_expense[2]:,.2f}", min_expense[3]])
    print(table_min)

#4 update expense

def update_expense(ide, date=None, category=None, amount=None, description=None):
    conn = database_connection()
    cur = conn.cursor()

    if date:
        cur.execute("UPDATE expenses SET date = %s WHERE id = %s", (date, ide))
    if category:
        cur.execute("UPDATE expenses SET category = %s WHERE id = %s", (category, ide))
    if amount:
        cur.execute("UPDATE expenses SET amount = %s WHERE id = %s", (amount, ide))
    if description:
        cur.execute("UPDATE expenses SET description = %s WHERE id = %s", (description, ide))

    conn.commit()
    cur.close()
    conn.close()
    
#5 delete expense

def delete_expense(expense_id):
    conn = database_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id=%s", (expense_id,))
    conn.commit()
    cur.close()
    conn.close()
    
#6 view expense by category

def view_expense_by_category(category):
    conn = database_connection()
    cur = conn.cursor()
    cur.execute("SELECT date, category, amount, description FROM expenses WHERE category=%s", (category,))
    expense_by_category = cur.fetchall()
    
    # Create a PrettyTable object
    table = PrettyTable()
    table.field_names = ["Date", "Category", "Amount ($)", "Description"]
    
    for row in expense_by_category:
        table.add_row([row[0], row[1], f"{float(row[2]):,.2f}", row[3]])
    
    # Close the database connection
    cur.close()
    conn.close()
    
    # Print the table
    print("\n" + "="*40)
    print(f"   📂 Expenses for Category: {category} 📂")
    print("="*40)
    print(table)
    
#7 view expense by date

def view_expense_by_date(start, end):
    conn = database_connection()
    cur = conn.cursor()
    cur.execute("SELECT date, category, amount, description FROM expenses WHERE date BETWEEN %s AND %s", (start, end))
    expenses_by_date = cur.fetchall()
    
    # Create a PrettyTable object
    table = PrettyTable()
    table.field_names = ["Date", "Category", "Amount ($)", "Description"]
    
    for row in expenses_by_date:
        table.add_row([row[0], row[1], f"{float(row[2]):,.2f}", row[3]])
    
    # Close the database connection
    cur.close()
    conn.close()
    
    # Print the table
    print("\n" + "="*40)
    print(f"   🗓️ Expenses from {start} to {end} 🗓️")
    print("="*40)
    print(table)

#8 monthly expense

def monthly_expense():
    conn = database_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(amount) AS total_amount FROM expenses GROUP BY year, month ORDER BY year, month")
    monthly_expenses = cur.fetchall()
    
    # Calculate total and average monthly expenses
    total_expense = sum(row[2] for row in monthly_expenses)
    average_expense = total_expense / len(monthly_expenses) if monthly_expenses else 0
    
    # Create a PrettyTable object
    table = PrettyTable()
    table.field_names = ["Month", "Year", "Total Amount ($)"]
    
    for row in monthly_expenses:
        table.add_row([f"{row[1]:02d}", row[0], f"{float(row[2]):,.2f}"])
    
    # Close the database connection
    cur.close()
    conn.close()
    
    # Print the table and average expense
    print("\n" + "="*40)
    print("   📅 Monthly Expense Summary 📅")
    print("="*40)
    print(table)
    print(f"\nTotal Expense: ${total_expense:,.2f}")
    print(f"Average Monthly Expense: ${average_expense:.2f}")

# dataframe load

def load_expenses_to_dataframe():
    conn = database_connection()
    query = "SELECT id, date, category, amount, description FROM expenses"
    df = pd.read_sql(query, conn)
    conn.close()
    return df
 
#9 visualize expense

def visualize_expenses():
    df = load_expenses_to_dataframe()
    way = input("Choose 'A' for Category or 'B' for Month: ").strip().upper()
    
    # Group by category and plot    
    if(way=="A"): 
        expenses_by_category = df.groupby('category')['amount'].sum()
        plt.figure(figsize=(10, 6))
        expenses_by_category.plot(kind='bar', title='Expenses by Category', rot=45)
        plt.xlabel('Category')
        plt.ylabel('Total Amount ($)')
        plt.tight_layout()
        plt.show()
    
    # Group by month and plot
    elif(way=="B"):
        df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
        expenses_by_month = df.groupby('month')['amount'].sum()
        plt.figure(figsize=(10, 6))
        expenses_by_month.plot(kind='line', title='Expenses Over Time')
        plt.xlabel('Month')
        plt.ylabel('Total Amount ($)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("❗ Invalid option. Please enter 'A' or 'B'.")

#10 analyse expense

def analyze_expenses():
    df = load_expenses_to_dataframe()
    
    # Calculate statistics
    total_expenses = df['amount'].sum()
    mean_expense = df['amount'].mean()
    median_expense = df['amount'].median()

    # Display statistics
    print("\n" + "="*40)
    print(" 📊 Expense Analysis Report 📊 ")
    print("="*40)
    print(f"🟢 Total Expenses: ${total_expenses:,.2f}")
    print(f"🔵 Mean Expense: ${mean_expense:,.2f}")
    print(f"🟠 Median Expense: ${median_expense:,.2f}")
    print("="*40)

    # Group by category
    expenses_by_category = df.groupby('category')['amount'].sum().sort_values(ascending=False)
    print("\nExpenses by Category:")
    for category, amount in expenses_by_category.items():
        print(f"  {category.capitalize():<10}: ${amount:,.2f}")

    # Group by month
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
    expenses_by_month = df.groupby('month')['amount'].sum().sort_index()
    print("\nExpenses by Month:")
    for month, amount in expenses_by_month.items():
        print(f"  {month}: ${amount:,.2f}")

    print("="*40)

# main function


def main():
    while True:
        print("\n" + "="*40)
        print("   🌟 Personal Expense Tracker 🌟")
        print("="*40)
        print("1. ➕ Add an Expense")
        print("2. 👀 View Expenses")
        print("3. 📄 Generate Summary Report")
        print("4. ✏️ Update an Expense")
        print("5. ❌ Delete an Expense")
        print("6. 📂 View Expenses by Category")
        print("7. 🗓️ View Expenses by Date Range")
        print("8. 📈 Calculate Average Monthly Expense")
        print("9. 📊 Visualize Expenses")
        print("10. 📊 Analyze Expenses")
        print("11. 🚪 Exit")
        print("="*40)

        choice = input("Choose an option (1-11): ")
        
        if choice == '1':
            print("\n" + "="*40)
            print("   🟢 Add an Expense 🟢")
            print("="*40)
            date = input("Enter date (YYYY-MM-DD): ")
            if not validate_date(date):
                print("\n❗ Invalid date format. Please enter a valid date in YYYY-MM-DD format.")
                continue
            category = input("Enter category: ")
            amount = input("Enter amount: ")
            if not amount.isdigit():
                print("\n❗ Invalid amount. Please enter a numeric value.")
                continue
            name = input("Enter Name: ")
            description = input("Enter Description: ")
            add_expense(date, category, amount, description)
            print("\n✅ Expense added successfully!")

            
        elif choice == '2':
            view_expense()
            print("✅ Here are your expenses.")
            
        elif choice == '3':
            generate_summary()
            print("✅ Summary report generated.")
            
        elif choice == '4':
            expense_id = input("Enter the expense ID to update: ")
            date = input("Enter new date (YYYY-MM-DD) or leave blank: ")
            if date and not validate_date(date):
                print("❗ Invalid date format. Please try again.")
                continue
            category = input("Enter new category or leave blank: ")
            amount = input("Enter new amount or leave blank: ")
            if amount and not amount.isdigit():
                print("❗ Invalid amount. Please enter a numeric value.")
                continue
            description = input("Enter new description or leave blank: ")
    
            update_expense(expense_id, date or None, category or None, amount or None, description or None)
            print("✅ Expense updated successfully!")
            
        elif choice == '5':
            expense_id = input("Enter the expense ID to delete: ")
            delete_expense(expense_id)
            print("✅ Expense deleted successfully!")
            
        elif choice == '6':
            category = input("Enter category to view: ")
            view_expense_by_category(category)
            print(f"✅ Here are your expenses for the category '{category}'.")
            
        elif choice == '7':
            start_date = input("Enter start date (YYYY-MM-DD): ")
            if not validate_date(start_date):
                print("❗ Invalid start date format. Please try again.")
                continue
            end_date = input("Enter end date (YYYY-MM-DD): ")
            if not validate_date(end_date):
                print("❗ Invalid end date format. Please try again.")
                continue
            view_expense_by_date(start_date, end_date)
            print(f"✅ Here are your expenses from {start_date} to {end_date}.")
            
        elif choice == '8':
            monthly_expense()
            print("✅ Average monthly expense calculated.")
            
        elif choice == '9':
            visualize_expenses()
            print("✅ Expenses visualized.")
            
        elif choice == '10':
            analyze_expenses()
            print("✅ Expenses analyzed.")
            
        elif choice == '11':
            print("👋 Goodbye!")
            break
            
        else:
            print("❗ Invalid option, please try again.")

# date valid ha ya nahi

def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    main()

