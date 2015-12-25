'''
HOMEWORK 1
karol.kornecki@gmail.com
'''
# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def main():
    portfolio = ['C', 'GS', 'IBM', 'HNZ']
    start_date = dt.datetime(2010, 1, 1)
    end_date = dt.datetime(2010, 12, 31)

    result = simulate_optimized(start_date, end_date, portfolio)

    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", portfolio
    print "Optimal Allocations:", result[1]
    print "Sharpe Ratio:", result[0][0]
    print "Volatility (stdev of daily returns):", result[0][1]
    print "Average Daily Return:", result[0][2]
    print "Cumulative Return:", result[0][3]


def simulate(start_date, end_date, portfolio, allocation):
    yahoo_data_source = da.DataAccess('Yahoo')
    all_symbols = yahoo_data_source.get_all_symbols()

    bad_symbols = list(set(portfolio) - set(all_symbols))

    if len(bad_symbols) != 0:
        print "Portfolio contains bad symbols : ", bad_symbols

    for bad in bad_symbols:
        i = portfolio.index(bad)
        portfolio.pop(i)

    time_of_day = dt.timedelta(hours=16)
    time_stamps = du.getNYSEdays(start_date, end_date, time_of_day)
    label_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    data = yahoo_data_source.get_data(time_stamps, portfolio, label_keys)

    dict_data = dict(zip(label_keys, data))
    close_price_data = dict_data['close'].copy()

    # normalizing
    close_price = close_price_data.values
    normalized_price = close_price / close_price[0, :]

    portfolio_value = np.sum(normalized_price * allocation, axis=1)

    # daily return
    portfolio_return = portfolio_value.copy()
    tsu.returnize0(portfolio_return)

    # sharpe
    sharpe_ratio = tsu.get_sharpe_ratio(portfolio_return.copy())

    # stdev
    stdev = np.std(portfolio_return)

    # mean
    mean = np.mean(portfolio_return)

    # cumulative portfolio return
    cumulative_portfolio_return = np.prod(portfolio_return + 1)

    return sharpe_ratio, stdev, mean, cumulative_portfolio_return


def simulate_optimized(start_date, end_date, portfolio):
    alloc = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    best_allocation_result = [-1, -1, -1, -1]  # default init
    best_allocation = []

    # brute force searching for optimized allocations
    for i in alloc:
        for j in alloc:
            for m in alloc:
                for n in alloc:
                    if i + j + m + n == 1:
                        res = simulate(start_date, end_date, portfolio, [i, j, n, m])
                        if res[0] > best_allocation_result[0]:
                            best_allocation_result = res
                            best_allocation = [i, j, n, m]

    return best_allocation_result, best_allocation


if __name__ == '__main__':
    main()
