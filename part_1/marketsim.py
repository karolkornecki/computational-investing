import sys
import csv
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du


def read_orders_file():
    with open(orders_file, 'rU') as in_file:
        reader = csv.reader(in_file)
        for row in reader:
            orders.append([dt.datetime(int(row[0]), int(row[1]), int(row[2]), 16), row[3], row[4], int(row[5])])


def get_data_for_simulation():
    start_date = min(orders)[0]
    end_date = max(orders)[0]
    close_time = dt.timedelta(hours=16)
    trading_days = du.getNYSEdays(start_date, end_date, close_time)
    symbols = list(set([order[1] for order in orders]))
    data_obj = da.DataAccess('Yahoo')
    close_prices = data_obj.get_data(trading_days, symbols, "close")
    return trading_days, symbols, close_prices


def simulate():
    global value
    for today in trading_days:
        total_value = 0
        today_portfolio = [0] * len(symbols)
        for symbol in symbols:
            order_exist_this_day = False
            for order in orders:
                value = 0
                if today.date() == order[0].date() and symbol == order[1]:
                    order_exist_this_day = True
                    quantity = order[3]
                    price = close_prices[symbol][today]

                    if order[2] == "Buy":
                        value = quantity * price
                    if order[2] == "Sell":
                        value = quantity * price * (-1)

                    today_portfolio[symbols.index(symbol)] = today_portfolio[symbols.index(symbol)] + value
                    total_value = total_value + value

            # update portfolio
            if len(portfolio) >= 1:
                previous_portfolio_value = portfolio[len(portfolio) - 1][symbols.index(symbol)]
                today_return = close_prices[symbol][today] / close_prices[symbol][yesterday]
                if order_exist_this_day:
                    today_portfolio[symbols.index(symbol)] = today_portfolio[symbols.index(
                            symbol)] + previous_portfolio_value * today_return
                else:
                    today_portfolio[symbols.index(symbol)] = previous_portfolio_value * today_return

        portfolio.append(today_portfolio)
        if today == trading_days[0]:
            amount[0] -= total_value
        else:
            amount.append(amount[len(amount) - 1] - total_value)
        yesterday = today


def calculate_total_portfolio_return():
    for i in range(len(trading_days)):
        total.append(sum(portfolio[i]) + amount[i])


def write_values_file():
    i = 0
    with open(values_file, 'wb') as out_file:
        line = csv.writer(out_file, delimiter=',')
        for day in trading_days:
            line.writerow([day.year, day.month, day.day, total[i]])
            i += 1


# simulation
start_amount = float(1000000)
orders_file = 'orders2.csv'
values_file = 'values2.csv'

orders = []
amount = [start_amount]
portfolio = []
value = []
total = []

read_orders_file()
data = get_data_for_simulation()
trading_days = data[0]
symbols = data[1]
close_prices = data[2]

simulate()

calculate_total_portfolio_return()
write_values_file()
