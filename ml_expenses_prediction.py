import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# загрузка данных

data = pd.read_csv('expense_data.csv')

# Define features and target

X = data[['Food', 'Transport', 'Studies', 'Fun', 'Weird Stuff']]
y = data['Budget']




# разделение датасетов 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# рандомный лес)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# проверка потенциальной ошибки

predictions = model.predict(X_test)
error = mean_absolute_error(y_test, predictions)
print(f'Mean Absolute Error: {error}')


current_month_data = {'Food': 500, 'Transport': 300, 'Studies': 100, 'Fun': 600, 'Weird Stuff': 200}
current_month_df = pd.DataFrame([current_month_data])
predicted_budget = model.predict(current_month_df)
print(f' предположительный бюджет на следующий месяц: {predicted_budget[0]}')
