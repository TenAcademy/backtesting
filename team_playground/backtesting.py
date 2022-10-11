from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from datetime import datetime
import yfinance as yf
import backtrader as bt
import sys

sys.path.append('..')

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    data = yf.download(tickers='MSFT')
    data.to_csv('data/MSFT.csv')
    print(data, type(data), data.shape)
    cerebro.adddata(data)
    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
