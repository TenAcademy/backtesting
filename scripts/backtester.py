from __future__ import (absolute_import, division, print_function,unicode_literals)

import yfinance as yf
import pandas as pd
import backtrader as bt
from datetime import datetime
import os
import sys
import json
from backtrader.analyzers import Returns,DrawDown,SharpeRatio,TradeAnalyzer

class backtester:

    def prepare_cerebro(self,asset,strategy,start_date:str,data_path:str=None,end_date:str=None,cash:int=100,commission:float=0)->bt.Cerebro:
        if end_date ==None:
            end_date= datetime.strftime(datetime.now(),"%Y-%m-%d")
        if data_path == None:
            data_path=f"../data/{asset}.csv"
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(cash)
        cerebro.broker.setcommission(commission=commission)
        cerebro.addstrategy(strategy)
        
        isExist = os.path.exists(data_path)
        if not isExist:
            data= yf.download(asset,start_date,end=end_date)
            data.to_csv(data_path)
        
        data = bt.feeds.YahooFinanceCSVData(
            dataname=data_path,
            fromdate=datetime.strptime(start_date,"%Y-%m-%d"),
            todate=datetime.strptime(end_date,"%Y-%m-%d"),
            reverse=False
        )

        cerebro.adddata(data)
        # cerebro.addanalyzer(AnnualReturn)
        cerebro.addanalyzer(TradeAnalyzer)
        return cerebro

    def run_test(cerebro:bt.Cerebro):

        result={}

        cerebro.addanalyzer(SharpeRatio, _name='sharpe')
        cerebro.addanalyzer(Returns, _name='returns')
        cerebro.addanalyzer(DrawDown, _name='draw')
        cerebro.addanalyzer(TradeAnalyzer, _name='trade')
        
        starting = cerebro.broker.getvalue()
        res=cerebro.run()
        final=cerebro.broker.getvalue()

        thestrat = res[0]

        sharpe=thestrat.analyzers.sharpe.get_analysis()
        return_val=thestrat.analyzers.returns.get_analysis()
        drawdown=thestrat.analyzers.draw.get_analysis()
        trade=thestrat.analyzers.trade.get_analysis()

        result["sharpe_ratio"]=sharpe['sharperatio']
        result["return"]=return_val['rtot']
        result['max_drawdown'] = drawdown['max']['drawdown']
        
        try:
            result['win_trade']=trade['won']['total']
        except:
            result['win_trade']="Undefined"
        
        try:
            result['loss_trade']=trade['lost']['total']
        except:
            result['loss_trade']="Undefined"

        try:
            result['total_trade']=trade['total']['total']
        except:
            result['total_trade']="Undefined"

        result['start_portfolio']=starting
        result['final_portfolio']=final

        return result