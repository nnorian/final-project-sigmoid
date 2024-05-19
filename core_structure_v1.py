from expense_v1 import Expense
from typing import List
import calendar
import datetime

def main():
    expense_file_path = 'expenses.csv'
    budget = 1000000000
    #get user to input their expense
    expense = get_user_expense()

    #add the expenses to a file
    save_expense_to_a_file(expense, expense_file_path)

    #read file and summarize expenses
    summarize_expenses(expense_file_path, budget)



def get_user_expense():
    expense_name = input('what did u spent your money money for? ')
    expense_amount = float(input('enter expense amount: '))
    

    expense_categories = [

    'food', 'graduation', 'studies', 'fun', 'weird stuff'
    ]
    while True:
        print('select a category: ')
        for i, category_name in enumerate(expense_categories):
            print(f'{i + 1}. {category_name}')

        value_range = f'[1 - {len(expense_categories)}]'
        selected_index = int(input(f'enter category number:  {value_range}  ')) - 1

        if selected_index in range(len(expense_categories)):
            selected_category  = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
                  )
            return new_expense
        else:
            print("invalid category, please try again")  
            

def save_expense_to_a_file(expense: Expense, expense_file_path):
    with open(expense_file_path, 'a') as f:
        f.write(f'{expense.name}, {expense.amount}, {expense.category}\n')

def summarize_expenses(expense_file_path, budget):
    expenses = []
    with open(expense_file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            stripped_line = line.strip()
            expense_name, expense_amount, expense_category = line.strip().split(',')
            line_expense = Expense(
                name = expense_name, amount = float(expense_amount), category = expense_category
                )
            expenses.append(line_expense)
    amount_by_category = {} 
    for expense in expenses:
        key =  expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount
    for key, amount in amount_by_category.items():
        print(f'   {key}: {amount:.2f} of money money ')


    total_spent = sum([x.amount for x in expenses])
    print(f"you've spent {total_spent:.2f} of money money this month")

    remaining_budget = budget - total_spent
    print(f"remaining {remaining_budget:.2f} of money money this month")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    print('remaining days in the current month:  ', remaining_days)

    daily_budget = remaining_budget / remaining_days
    print(f'budget per day:  {daily_budget:.2f}')


if __name__ == "__main__":
    main()
