import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Клас Pizzeria, який представляє піцерію
class Pizzeria:
    def __init__(self):
        # Час приготування стандартної та індивідуальної піци
        self.standard_pizza_time = 10
        self.custom_pizza_time = 15

    def get_standard_pizza_price(self):
        return np.random.randint(10, 15)

    def get_custom_pizza_price(self):
        return np.random.randint(15, 20)

    # Метод для відображення замовлень
    def display_orders(self, orders_df):
        print("Замовлення на піцу:")
        print("-" * 50)
        for index, row in orders_df.iterrows():
            # Перетворення часу з хвилин в години та хвилини
            hours = row['Time'] // 60
            minutes = row['Time'] % 60

            order_time_hours = row['Order Time'] // 60
            order_time_minutes = row['Order Time'] % 60

            # Вивід інформації про замовлення
            print(f"Time:  {hours:02}:{minutes:02}")
            print(f"Order type: {row['Order Type']}")
            print(f"Making time: {order_time_hours:02}:{order_time_minutes:02}")
            print(f"Order price: {row['Order Price']} conventional units")
            print("-" * 35)

# Функція для симуляції замовлень
def simulate_orders(pizzeria):
    # Інтервал часу між замовленнями
    time_interval_minutes = 5
    # Встановлення seed для відтворюваності результатів
    np.random.seed(0)
    rs = np.random.RandomState(0)

    intervals = [(540, 660), (660, 900), (900, 1200), (1200, 1320)]
    probabilities = [0.3, 0.5, 0.9, 0.7]

    start_time_minutes = 0
    orders = []

    # Проводимо симуляцію протягом дня
    while start_time_minutes < 1440:
        interval = None

        # Визначаємо часовий інтервал для поточного часу
        for i, (start, end) in enumerate(intervals):
            if start <= start_time_minutes < end:
                interval = intervals[i]
                break

        # Якщо інтервал визначено, генеруємо замовлення
        if interval:
            num_orders = rs.binomial(1, probabilities[i])
            for _ in range(num_orders):
                # Визначаємо тип замовлення, час приготування та ціну
                if rs.random() < 0.5:
                    order_type = "Standard"
                    order_time_minutes = pizzeria.standard_pizza_time
                    order_price = pizzeria.get_standard_pizza_price()
                else:
                    order_type = "Custom"
                    order_time_minutes = pizzeria.custom_pizza_time
                    order_price = pizzeria.get_custom_pizza_price()

                # Додаємо замовлення до списку
                orders.append({
                    "Time": start_time_minutes,
                    "Order Type": order_type,
                    "Order Time": order_time_minutes,
                    "Order Price": order_price,
                })

        # Переходимо до наступного часового інтервалу
        start_time_minutes += time_interval_minutes

    # Повертаємо замовлення як DataFrame
    return pd.DataFrame(orders)

# Створюємо об'єкт піцерії та симулюємо замовлення
pizzeria = Pizzeria()
orders_df = simulate_orders(pizzeria)
pizzeria.display_orders(orders_df)

# Рахуємо кількість замовлень на годину
orders_per_hour = orders_df.groupby(orders_df['Time'] // 60).size()

# Створюємо графік замовлень по годинах
plt.figure(figsize=(12, 6), )
plt.bar(orders_per_hour.index, orders_per_hour.values, tick_label=orders_per_hour.index)
plt.xlabel('Hour')
plt.ylabel('Number of orders')
plt.title('Frequency of pizza orders during the day')
plt.xticks(range(24))
plt.show()

# Рахуємо прибуток по годинах
hourly_profit = []
for hour in range(24):
    hour_orders = orders_df[(orders_df["Time"] >= hour * 60) & (orders_df["Time"] < (hour + 1) * 60)]
    profit = sum(hour_orders["Order Price"])
    hourly_profit.append(profit)


# Створюємо графік прибутку по годинах
hours = range(24)
plt.figure(figsize=(12, 6))
plt.bar(hours, hourly_profit, tick_label=hours, color='green')
plt.xlabel("Hour")
plt.ylabel("Profit")
plt.title("The profit of the pizzeria at every hour of the day")
plt.show()

# Рахуємо загальний прибуток
profits = []
time_intervals = list(range(0, 1440, 10))
def calculate_daily_profit(orders_df):
    return orders_df["Order Price"].sum()

for interval in time_intervals:
    profit = calculate_daily_profit(orders_df[orders_df["Time"] <= interval])
    profits.append(profit)

# Створюємо графік загального прибутку
plt.plot(time_intervals, profits, color='red')
plt.xlabel("Time (minutes)")
plt.ylabel("Total profit")
plt.title("Total profit for the day at the pizzeria")
plt.grid(True)
plt.show()