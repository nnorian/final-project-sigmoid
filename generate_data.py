import csv
import random

# Define the ranges for each category
budget_range = (2000, 4000)
food_range = (200, 900)
transport_range = (160, 640)
studies_range = (20, 300)
fun_range = (50, 1000)
weird_stuff_range = (0, 1000)

# Number of months (3 years)
num_months = 12 * 3

# Function to generate random expense data
def generate_expense_data():
    data = []
    for _ in range(num_months):
        budget = random.randint(*budget_range)
        while True:
            food = random.randint(*food_range)
            transport = random.randint(*transport_range)
            studies = random.randint(*studies_range)
            fun = random.randint(*fun_range)
            weird_stuff = random.randint(*weird_stuff_range)
            total = food + transport + studies + fun + weird_stuff
            if total <= budget:
                break

        data.append([budget, food, transport, studies, fun, weird_stuff])

    return data

# Function to save data to CSV
def save_expense_data(file_path='expense_data.csv'):
    expense_data = generate_expense_data()
    with open(file_path, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Budget', 'Food', 'Transport', 'Studies', 'Fun', 'Weird Stuff'])
        writer.writerows(expense_data)
    return file_path