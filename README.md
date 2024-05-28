# final-project-sigmoid

Installation
Clone the Repository

bash
git clone <repository_url>
Navigate to Project Directory

bash
cd expense-tracker-ml
Install Dependencies

bash
pip install -r requirements.txt
Generate Random Expense Data

To generate random expense data, run the following command:

bash
python generate_data.py
Train the Machine Learning Model

The machine learning model needs to be trained before making predictions. Run the following command:

bash
python train_model.py
Start the Flask App

python app.py
Access the App

Open your web browser and go to http://localhost:5000 to access the Expense Tracker application.

Description

The Expense Tracker with Machine Learning Predictions is a Flask web application designed to help users track their expenses. In addition to basic expense tracking functionality, it leverages machine learning to predict the budget for the next month based on past spending patterns.

Features

Add Expenses: Users can add new expenses by providing the name, amount, and category.
View Summary: Users can view a summary of their expenses, including the total spent, remaining budget, and daily budget.
Expense Categories: Expenses can be categorized into predefined categories such as food, studies, fun, etc.
Machine Learning Predictions: The application utilizes a machine learning model to predict the budget for the next month based on past spending data.

File Structure

app.py: Contains the Flask application code.
templates/: Directory containing HTML templates for rendering pages.
index.html: Home page template.
add_expense.html: Template for adding expenses.
summary.html: Template for displaying expense summary.
predict_budget.html: Template for displaying predicted budget.
expenses.csv: CSV file to store expense data.
generate_data.py: Python script to generate random expense data.
train_model.py: Python script to train the machine learning model.
ml_model.py: Python script containing the machine learning model.
README.md: Documentation file providing instructions on installation and usage.

Dependencies

Flask: Web framework for building the application.
Pandas: Data manipulation library used for handling data.
Scikit-learn: Machine learning library used for building and training the model.
Python 3.12: Programming language used to develop the application.
License
This project is licensed under the MIT License - see the LICENSE file for details.
