from flask import Flask, request, render_template, redirect, url_for, flash
import calendar
import datetime
import csv
import os

class Expense:
    def __init__(self, name, category, amount) -> None:
        self.name = name
        self.category = category
        self.amount = amount

    def __repr__(self):
        return f'<Expense: {self.name}, {self.category}, {self.amount:.2f}>'

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Ensure the expenses.csv file is in the same directory as the script
EXPENSE_FILE_PATH = os.path.join(os.path.dirname(__file__), 'expenses.csv')
DEFAULT_BUDGET = 1000000000

# This will hold the user-set budget
current_budget = {'budget': DEFAULT_BUDGET}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/set_budget', methods=['GET', 'POST'])
def set_budget():
    if request.method == 'POST':
        try:
            budget = float(request.form['budget'])
            if budget <= 0:
                flash('Budget must be a positive number', 'error')
                return redirect(url_for('set_budget'))
            current_budget['budget'] = budget
            flash('Budget set successfully!', 'success')
            return redirect(url_for('home'))
        except ValueError:
            flash('Invalid budget. Please enter a number', 'error')
            return redirect(url_for('set_budget'))
    return render_template('set_budget.html')

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        expense_name = request.form['expense_name']
        try:
            expense_amount = float(request.form['expense_amount'])
            if expense_amount <= 0:
                flash('Expense amount must be a positive number', 'error')
                return redirect(url_for('add_expense'))
        except ValueError:
            flash('Invalid amount. Please enter a number', 'error')
            return redirect(url_for('add_expense'))

        selected_category = request.form['category']
        expense_categories = ['Food', 'Transport', 'Studies', 'Fun', 'Weird Stuff']
        if selected_category not in expense_categories:
            flash('Invalid category', 'error')
            return redirect(url_for('add_expense'))

        new_expense = Expense(
            name=expense_name, category=selected_category, amount=expense_amount
        )
        save_expense_to_a_file(new_expense, EXPENSE_FILE_PATH)
        flash('Expense added successfully!', 'success')
        return redirect(url_for('summary'))

    expense_categories = ['Food', 'Transport', 'Studies', 'Fun', 'Weird Stuff']
    return render_template('add_expense.html', categories=expense_categories)

@app.route('/summary')
def summary():
    summary_data = summarize_expenses(EXPENSE_FILE_PATH, current_budget['budget'])
    return render_template('summary.html', summary=summary_data)

def save_expense_to_a_file(expense: Expense, expense_file_path):
    try:
        with open(expense_file_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([expense.name, expense.amount, expense.category])
    except Exception as e:
        flash(f'Error saving expense: {e}', 'error')

def summarize_expenses(expense_file_path, budget):
    expenses = []
    try:
        with open(expense_file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) != 3:
                    continue
                expense_name, expense_amount, expense_category = row
                try:
                    line_expense = Expense(
                        name=expense_name, amount=float(expense_amount), category=expense_category
                    )
                    expenses.append(line_expense)
                except ValueError:
                    continue
    except FileNotFoundError:
        flash('Expense file not found. Please add an expense first.', 'error')
        return {
            'amount_by_category': {},
            'total_spent': 0,
            'remaining_budget': budget,
            'remaining_days': 0,
            'daily_budget': 0
        }

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    total_spent = sum([x.amount for x in expenses])
    remaining_budget = budget - total_spent

    if remaining_budget <= 0:
        print("Sigmoid recommends you to learn Python and Machine Learning :)")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    daily_budget = remaining_budget / remaining_days if remaining_days > 0 else 0

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
