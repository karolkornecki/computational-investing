import numpy as np
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkstudy.EventProfiler as ep


def find_events(symbols, d_data, dollar):
    actual_close = d_data['actual_close']

    events = copy.deepcopy(actual_close)
    events = events * np.NAN

    timestamps = actual_close.index

    for symbol in symbols:
        for i in range(1, len(timestamps)):
            price_today = actual_close[symbol].ix[timestamps[i]]
            price_yesterday = actual_close[symbol].ix[timestamps[i - 1]]

            if price_yesterday >= dollar > price_today:
                events[symbol].ix[timestamps[i]] = 1

    return events


def calculate_events(start_date, end_date, year, dollar, file_name):
    timestamps = du.getNYSEdays(start_date, end_date, dt.timedelta(hours=16))

    data = da.DataAccess('Yahoo')
    symbols = data.get_symbols_from_list(year)
    symbols.append('SPY')

    label_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    symbol_data = data.get_data(timestamps, symbols, label_keys)
    dict_symbol_data = dict(zip(label_keys, symbol_data))

    for key in label_keys:
        dict_symbol_data[key] = dict_symbol_data[key].fillna(method='ffill')
        dict_symbol_data[key] = dict_symbol_data[key].fillna(method='bfill')
        dict_symbol_data[key] = dict_symbol_data[key].fillna(1.0)

    events = find_events(symbols, dict_symbol_data, dollar)
    print "Creating Study"
    ep.eventprofiler(events, dict_symbol_data, i_lookback=20, i_lookforward=20,
                     s_filename=file_name, b_market_neutral=True, b_errorbars=True,
                     s_market_sym='SPY')


if __name__ == '__main__':
    calculate_events(dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31), 'sp5002012', 6.0, '6_2012.pdf')
    calculate_events(dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31), 'sp5002012', 7.0, '7_2012.pdf')
    calculate_events(dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31), 'sp5002012', 8.0, '8_2012.pdf')
    calculate_events(dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31), 'sp5002012', 9.0, '9_2012.pdf')
    calculate_events(dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31), 'sp5002012', 10.0, '10_2012.pdf')
    calculate_events(dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31), 'sp5002008', 6.0, '6_2008.pdf')
    calculate_events(dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31), 'sp5002008', 7.0, '7_2008.pdf')
    calculate_events(dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31), 'sp5002008', 8.0, '8_2008.pdf')
    calculate_events(dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31), 'sp5002008', 9.0, '9_2008.pdf')
    calculate_events(dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31), 'sp5002008', 10.0, '10_2008.pdf')
