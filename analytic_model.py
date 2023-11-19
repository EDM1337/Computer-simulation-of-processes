import math
import numpy as np
from prettytable import PrettyTable


def simulate(num_ovens, interval):
        intervals = [(540, 660), (660, 900), (900, 1200), (1200, 1320)]
        probabilities = [0.3, 0.5, 0.9, 0.7]
        max_queue_length = 10
        standard_pizza_time = 10
        custom_pizza_time = 15
        queue = []
        ovens_list = []
        order_statistics = [0] * 24
        hourly_profit = [0] * 24
        interval_minute_start = interval * 60
        interval_minute_end = interval * 60 + 60
        time_interval_minutes = 5
        np.random.seed(0)
        rs = np.random.RandomState(0)

        while interval_minute_start < interval_minute_end:
            interval = None
            for i, (start, end) in enumerate(intervals):
                if start <= interval_minute_start < end:
                    interval = intervals[i]
                    break

            hourly_revenue = 0

            if interval:
                num_orders = rs.binomial(1, probabilities[i])
                for _ in range(num_orders):
                    if rs.random() < 0.7:
                        pizza_type = "Standard"
                        pizza_time = standard_pizza_time
                        pizza_price = np.random.randint(10, 15)  
                        pizza_type = "Custom"
                        pizza_time = custom_pizza_time
                        pizza_price = np.random.randint(15, 30)  

                    if len(ovens_list) < num_ovens:
                        ovens_list.append({
                            "Order Time": interval_minute_start,
                            "Pizza Type": pizza_type,
                            "Pizza Time": pizza_time,
                            "Pizza Price": pizza_price,
                        })
                        hourly_revenue += pizza_price

                    elif len(queue) < max_queue_length:
                        queue.append({
                            "Order Time": interval_minute_start,
                            "Pizza Type": pizza_type,
                            "Pizza Time": pizza_time,
                            "Pizza Price": pizza_price,
                        })

            for oven in ovens_list:
                if interval_minute_start >= oven["Order Time"] + oven["Pizza Time"]:
                    ovens_list.remove(oven)

            for order in queue:
                if len(ovens_list) < num_ovens:
                    ovens_list.append(order)
                    hourly_revenue += order["Pizza Price"]
                queue.remove(order)

            current_hour = interval_minute_start // 60
            order_statistics[current_hour] += num_orders
            hourly_profit[current_hour] += hourly_revenue

            interval_minute_start += time_interval_minutes

        return order_statistics, hourly_profit

def analytical():
        time_intervals = range(9, 22)
        oven_counts = [2, 3, 4, 5, 6, 7, 8, 9, 10]

        for time_interval in time_intervals:
            table = PrettyTable()
            table.field_names = ["Кількість включених печей", *[f"c = {c}" for c in oven_counts]]

            for characteristic in  ["Інтенсивність вхідного потоку (lambda)", "Середній час обслуговування одного клієнта (t_obslug)",
                                    "Інтенсивність обслуговування (mu)", "Завантаженість системи (ρ)",
                                    "Граничні ймовірності (q0)", "Ймовірність того, що вимога потрапить у чергу (pq)", "Ймовірність відмови (p_vidmovy)",
                                    "Відносна пропускна здатність (Q)", "Абсолютна пропускна здатність (A)",
                                    "Середня кількість зайнятих каналів (k̅ зайнятих)",
                                    "Середня кількість вимог в черзі (Lq)", "Середня кількість вимог в системі (Ls)",
                                    "Середній час перебування вимог у черзі (Wq)",
                                    "Середній час перебування вимог у системі (Ws)", "Виручка (D)"]:
                row_data = [characteristic]
                for oven_count in oven_counts:
                    q0, p_vidmovy, pq, Q, A, k_occupied, Lq, Ls, Wq, Ws, D, p, lambda_value, mu, t_service = calculate_system_characteristics_for_period(time_interval, oven_count)

                    if characteristic == "Інтенсивність вхідного потоку (lambda)":
                        row_data.append(f"{lambda_value:.2f}")
                    elif characteristic == "Середній час обслуговування одного клієнта (t_obslug)":
                        row_data.append(f"{t_service:.2f}")
                    elif characteristic == "Інтенсивність обслуговування (mu)":
                        row_data.append(f"{mu:.2f}")
                    elif characteristic == "Завантаженість системи (ρ)":
                        row_data.append(f"{p:.2f}")
                    elif characteristic == "Граничні ймовірності (q0)":
                        row_data.append(f"{q0:.2f}")
                    elif characteristic == "Ймовірність того, що вимога потрапить у чергу (pq)":
                        row_data.append(f"{pq:.2f}")
                    elif characteristic == "Ймовірність відмови (p_vidmovy)":
                        row_data.append(f"{p_vidmovy:.2f}")
                    elif characteristic == "Відносна пропускна здатність (Q)":
                        row_data.append(f"{Q:.2f}")
                    elif characteristic == "Абсолютна пропускна здатність (A)":
                        row_data.append(f"{A:.2f}")
                    elif characteristic == "Середня кількість зайнятих каналів (k̅ зайнятих)":
                        row_data.append(f"{k_occupied:.2f}")
                    elif characteristic == "Середня кількість вимог в черзі (Lq)":
                        row_data.append(f"{Lq:.2f}")
                    elif characteristic == "Середня кількість вимог в системі (Ls)":
                        row_data.append(f"{Ls:.2f}")
                    elif characteristic == "Середній час перебування вимог у черзі (Wq)":
                        row_data.append(f"{Wq:.2f}")
                    elif characteristic == "Середній час перебування вимог у системі (Ws)":
                        row_data.append(f"{Ws:.2f}")
                    elif characteristic == "Виручка (D)":
                        row_data.append(f"{D:.2f}")

                table.add_row(row_data)

            print(f"Результати аналізу в {time_interval}:00")
            print(table)
            print("\n")

def calculate_system_characteristics_for_period(time_interval, oven_count):
        order_statistics, hourly_profit = simulate(oven_count, time_interval)
        lambda_value = order_statistics[time_interval]

        t_service = 12 / 60

        mu = 1 / t_service

        p = lambda_value / mu

        c = oven_count

        m = lambda_value - c

        q0 = 1.0
        for i in range(c):
            q0 += (p ** i) / math.factorial(i)

        q0 += (m * (p ** (c + 1))) / (c * math.factorial(c))
        q0 = 1.0 / q0

        probabilities = [0] * (c + 1)
        for i in range(c):
            probabilities[i] = ((p ** i) / math.factorial(i)) * q0
        probabilities[c] = (p ** c) / math.factorial(c) * q0

        if p != c:
            pq = (((p ** (c)) * (1 - ((p ** (m)) / (c ** (m))))) / (math.factorial(c) * (1 - (p / c)))) * q0
        else:
            pq = ((p ** (c))/math.factorial(c)) * m * q0

        p_vidmovy = ((p ** (c + m)) / ((c ** (m)) * math.factorial(c))) * q0

        Q = 1 - p_vidmovy

        A = lambda_value * Q

        k_occupied = p * Q

        Lq = (((p ** (c + 1)) * m * (m + 1)) / (math.factorial(c) * c * 2)) * q0
        Ls = Lq + k_occupied
        Wq = Lq / lambda_value
        Ws = Ls / lambda_value

        #hourly_profit[time_interval]

        D = 15.5 * A - 20 * c


        return q0, p_vidmovy, pq, Q, A, k_occupied, Lq, Ls, Wq, Ws, D, p, lambda_value, mu, t_service


if __name__ == '__main__':
    analytical()