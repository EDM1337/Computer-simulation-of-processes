import numpy as np
import matplotlib.pyplot as plt


class Pizzeria:
    def __init__(self):
        self.num_ovens = 10 # Кількість печей
        self.max_queue_length = 10 # Максимальна довжина черги
        self.oven_cost_per_hour = 2 
        self.standard_pizza_time = 10
        self.custom_pizza_time = 15  
        self.queue = []
        self.ovens_list = []

    # Метод для відображення статусу піцерії
    def display_status(self, ovens_list, queue, start_time_minutes):

        # Перетворюємо час з хвилин в години та хвилини
        hours = start_time_minutes // 60
        minutes = start_time_minutes % 60

        # Виводимо інформацію про чергу
        print(f"Queue for pizza in {hours:02}:{minutes:02}:")

        # Виводимо інформацію про кожне замовлення в черзі
        for que in queue:
            print()
            hours_order = que['Order Time'] // 60
            minutes_order = que['Order Time'] % 60
            pizza_time_minutes = que['Pizza Time']
            print(f"Time:  {hours_order:02}:{minutes_order:02}")
            print(f"Order Type: {que['Pizza Type']}")
            print(f"Order Time: {pizza_time_minutes:02} minutes")
            print(f"Order Price: {que['Pizza Price']} ")

        # Виводимо інформацію про піци в печах
        print()
        print(f"Pizzas in the Ovens:")
        for oven in ovens_list:
            print()
            hours_order = oven['Order Time'] // 60
            minutes_order = oven['Order Time'] % 60
            pizza_time_minutes = oven['Pizza Time']
            print(f"Time:  {hours_order:02}:{minutes_order:02}")
            print(f"Order Type: {oven['Pizza Type']}")
            print(f"Order Time: {pizza_time_minutes:02} minutes")
            print(f"Order Price: {oven['Pizza Price']} conditional units")

        # Рахуємо кількість зайнятих та вільних печей
        busy_oven_count = len(
            [oven for oven in ovens_list if start_time_minutes <= oven["Order Time"] + oven["Pizza Time"]])
        free_oven_count = self.num_ovens - busy_oven_count

        # Виводимо інформацію про зайняті та вільні печі
        print()
        print(f"Ovens status:")
        print(f"Ovens busy: {busy_oven_count}")
        print(f"Ovens free: {free_oven_count}")
        print("-" * 35)

    def simulate(self):
        # Встановлюємо тривалість симуляції та інтервал часу
        simulation_duration_minutes = 1325
        time_interval_minutes = 5
        np.random.seed(2) # Встановлюємо seed для відтворюваності результатів
        rs = np.random.RandomState(2)
 
        order_statistics = [0] * 24  
        hourly_profit = [0] * 24


        intervals = [(540, 660), (660, 900), (900, 1200), (1200, 1320)] # Інтервали часу
        probabilities = [0.3, 0.5, 0.9, 0.7]

        start_time_minutes = 540
        
        while start_time_minutes < simulation_duration_minutes: # Проводимо симуляцію протягом дня
            interval = None
            for i, (start, end) in enumerate(intervals):
                if start <= start_time_minutes < end:
                    interval = intervals[i]
                    break

            hourly_revenue = 0

            if interval:

                # Генеруємо кількість замовлень
                num_orders = rs.binomial(1, probabilities[i])
                for _ in range(num_orders):
                    # Визначаємо тип піци, час приготування та ціну
                    if rs.random() < 0.7:
                        pizza_type = "Standard"
                        pizza_time = self.standard_pizza_time
                        pizza_price = np.random.randint(10, 15)  # Генерируем цену здесь
                    else:
                        pizza_type = "Custom"
                        pizza_time = self.custom_pizza_time
                        pizza_price = np.random.randint(15, 30)  # Генерируем цену здесь

                    # Якщо є вільна піч, додаємо піцу до списку печей
                    if len(self.ovens_list) < self.num_ovens:
                        self.ovens_list.append({
                            "Order Time": start_time_minutes,
                            "Pizza Type": pizza_type,
                            "Pizza Time": pizza_time,
                            "Pizza Price": pizza_price,
                        })
                        hourly_revenue += pizza_price

                    # Якщо всі печі зайняті, але є місце в черзі
                    elif len(self.queue) < self.max_queue_length:
                        self.queue.append({
                            "Order Time": start_time_minutes,
                            "Pizza Type": pizza_type,
                            "Pizza Time": pizza_time,
                            "Pizza Price": pizza_price,
                        })

            # Перебираємо всі печі
            for oven in self.ovens_list:
                # Якщо час приготування піци в печі закінчився, видаляємо піцу з печі
                if start_time_minutes >= oven["Order Time"] + oven["Pizza Time"]:
                    self.ovens_list.remove(oven)

            # Перебираємо всі замовлення в черзі
            for order in self.queue:
                # Якщо є вільна піч, переносимо замовлення з черги до печі
                if len(self.ovens_list) < self.num_ovens:
                    self.ovens_list.append(order)
                    hourly_revenue += order["Pizza Price"]
                    # Видаляємо замовлення з черги
                    self.queue.remove(order)

            current_hour = start_time_minutes // 60
            # Додаємо кількість замовлень до статистики замовлень за поточну годину
            order_statistics[current_hour] += num_orders
            # Додаємо прибуток за годину до загального прибутку за поточну годину
            hourly_profit[current_hour] += hourly_revenue

            self.display_status(self.ovens_list, self.queue, start_time_minutes) # Виводимо статус піцерії
            start_time_minutes += time_interval_minutes # Збільшуємо поточний час на інтервал часу


        start_hour = 9
        end_hour = 22
        hours = range(start_hour, end_hour)

        # Графік кількості замовлень
        plt.figure(figsize=(12, 6))
        plt.bar(hours, order_statistics[start_hour:end_hour], tick_label=hours, color='green')
        plt.xlabel('Hour of the day') # час дня
        plt.ylabel('Number of orders') # кількість замовлень
        plt.title('Частота замовлень піц протягом дня') # частота замовлень піц протягом дня
        plt.xticks(hours)
        plt.grid(axis='y')
        plt.show()

        # Графік прибутку в кожну годину
        plt.figure(figsize=(10, 6))
        plt.bar(hours, hourly_profit[start_hour:end_hour], color='pink')
        plt.title('Profit of the pizzeria every hour') # прибуток піцерії в кожну годину
        plt.xlabel('Hour') # година
        plt.ylabel('Profit') # прибуток
        plt.xticks(hours)
        plt.grid(axis='y')
        plt.show()

        profit = 0
        for prof in hourly_profit:
            profit += prof
        print(f"Profit without oven payments: {profit}")
        total_profit = profit - self.num_ovens * self.oven_cost_per_hour * (end_hour - start_hour)
        print(f"Total profit: {total_profit}")



Pizzeria().simulate()