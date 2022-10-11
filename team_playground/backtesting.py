from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import yfinance as yf
import backtrader as bt
import sys

sys.path.append('..')

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # fetch data from yahoo finance
    data = yf.download(tickers='MSFT')
    # save the data
    # data.to_csv('data/MSFT.csv')
    print(data, type(data), data.shape)
    feed = bt.feeds.PandasData(dataname=data)

    cerebro.adddata(feed)
    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
