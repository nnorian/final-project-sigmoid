from flask import Flask, request, render_template, redirect, url_for
import calendar
import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)

# Load database configuration from environment variables
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

DATABASE_URL = f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST} port={DB_PORT}"

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        expense_name = request.form['expense_name']
        expense_amount = float(request.form['expense_amount'])
        selected_category = request.form['category']

        new_expense = Expense(
            name=expense_name, category=selected_category, amount=expense_amount
        )
        save_expense_to_db(new_expense)
        return redirect(url_for('summary'))

    expense_categories = ['food', 'graduation', 'studies', 'fun', 'weird stuff']
    return render_template('add_expense.html', categories=expense_categories)

@app.route('/summary')
def summary():
    summary_data = summarize_expenses()
    return render_template('summary.html', summary=summary_data)

def save_expense_to_db(expense):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (name, category, amount) VALUES (%s, %s, %s)",
        (expense.name, expense.category, expense.amount)
    )
    conn.commit()
    cursor.close()
    conn.close()

def summarize_expenses():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    cursor.close()
    conn.close()

    amount_by_category = {}
    total_spent = 0
    for expense in expenses:
        key = expense['category']
        if key in amount_by_category:
            amount_by_category[key] += expense['amount']
        else:
            amount_by_category[key] = expense['amount']
        total_spent += expense['amount']

    budget = 1000000000
    remaining_budget = budget - total_spent

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    daily_budget = remaining_budget / remaining_days

    summary_data = {
        'amount_by_category': amount_by_category,
        'total_spent': total_spent,
        'remaining_budget': remaining_budget,
        'remaining_days': remaining_days,
        'daily_budget': daily_budget
    }
    return summary_data

if __name__ == "__main__":
    app.run(debug=True)
