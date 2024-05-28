from flask import Flask, request, render_template, redirect, url_for
import calendar
import datetime
import csv



class Expense:
    def __init__(self, name, category, amount) -> None:
        self.name = name
        self.category = category
        self.amount = amount

    def __repr__(self):
        return f'<Expense: {self.name}, {self.category}, greens{self.amount:.2f}>'


app = Flask(__name__)




EXPENSE_FILE_PATH = 'expenses.csv'
BUDGET = 1000000000



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
        save_expense_to_a_file(new_expense, EXPENSE_FILE_PATH)
        return redirect(url_for('summary'))

    expense_categories = ['food', 'graduation', 'studies', 'fun', 'weird stuff']
    return render_template('add_expense.html', categories=expense_categories)



@app.route('/summary')
def summary():
    summary_data = summarize_expenses(EXPENSE_FILE_PATH, BUDGET)
    return render_template('summary.html', summary=summary_data)

def save_expense_to_a_file(expense: Expense, expense_file_path):
    with open(expense_file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([expense.name, expense.amount, expense.category])

def summarize_expenses(expense_file_path, budget):
    expenses = []
    with open(expense_file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            expense_name, expense_amount, expense_category = row
            line_expense = Expense(
                name=expense_name, amount=float(expense_amount), category=expense_category
            )
            expenses.append(line_expense)

    
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    total_spent = sum([x.amount for x in expenses])
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
