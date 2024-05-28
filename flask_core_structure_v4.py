from aiohttp import web
import jinja2
import aiohttp_jinja2
import calendar
import datetime
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

app = web.Application()

# Load environment variables from .env file
load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

DATABASE_URL = f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST} port={DB_PORT}"

class Expense:
    def __init__(self, name, category, amount) -> None:
        self.name = name
        self.category = category
        self.amount = amount

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@aiohttp_jinja2.template('index.html')
def home(request):
    return {}

@aiohttp_jinja2.template('add_expense.html')
def add_expense(request):
    if request.method == 'POST':
        data = await request.post()
        expense_name = data['expense_name']
        expense_amount = float(data['expense_amount'])
        selected_category = data['category']

        new_expense = Expense(
            name=expense_name, category=selected_category, amount=expense_amount
        )
        save_expense_to_db(new_expense)
        raise web.HTTPFound(location='/summary')

    expense_categories = ['Food', 'Transport', 'Studies', 'Fun', 'Weird Stuff']
    context = {'categories': expense_categories}
    return context

@aiohttp_jinja2.template('summary.html')
def summary(request):
    summary_data = summarize_expenses()
    return {'summary': summary_data}

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

async def handle_500(request):
    return web.Response(text="Internal server error", status=500)

async def init_app():
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

    app.router.add_get('/', home)
    app.router.add_get('/add', add_expense)
    app.router.add_post('/add', add_expense)
    app.router.add_get('/summary', summary)

    app.middlewares.append(error_middleware)

    return app

async def error_middleware(app, handler):
    async def middleware_handler(request):
        try:
            response = await handler(request)
            if response.status == 404:
                return web.Response(text="Page not found", status=404)
            return response
        except web.HTTPException as ex:
            if ex.status == 500:
                return await handle_500(request)
            raise
    return middleware_handler

if __name__ == "__main__":
    app = asyncio.run(init_app())
    web.run_app(app, host='127.0.0.1', port=8080)
