from __future__ import (absolute_import, division, print_function,unicode_literals)
from unittest import result

import yfinance as yf
import pandas as pd
import backtrader as bt
from datetime import datetime
import os
import sys
import json
import mlflow

from backtrader.analyzers import Returns,DrawDown,SharpeRatio,TradeAnalyzer

class backtester:

    def prepare_cerebro(self,asset,strategy,start_date:str,data_path:str=None,end_date:str=None,cash:int=100,commission:float=0)->bt.Cerebro:
        if end_date == None:
            end_date= datetime.strftime(datetime.now(),"%Y-%m-%d")
        if data_path == None:
            data_path=f"./data/{asset}.csv"
        
        mlflow.end_run()
        mlflow.set_tracking_uri('http://localhost:5000')
        mlflow.set_experiment(strategy.__name__)
        mlflow.start_run()
        mlflow.log_param('asset',asset)
        mlflow.log_param('strategy',strategy.__name__)
        mlflow.log_param('startDate',start_date)
        mlflow.log_param('endDate',end_date)
        mlflow.log_param('commssion',commission)
        mlflow.log_param('initialCash',cash)

        cerebro = bt.Cerebro()
        cerebro.broker.setcash(cash)
        cerebro.broker.setcommission(commission=commission)
        cerebro.addstrategy(strategy)

        cerebro.addanalyzer(SharpeRatio, _name='sharpe')
        cerebro.addanalyzer(Returns, _name='returns')
        cerebro.addanalyzer(DrawDown, _name='draw')
        cerebro.addanalyzer(TradeAnalyzer, _name='trade')
        
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
        return cerebro

    def run_test(self,cerebro:bt.Cerebro):

        result={}

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
        try:
            mlflow.log_metric('sharpe_ratio',result['sharpe_ratio'])
        except:
            mlflow.log_param('sharpe_ratio',"undefined")
        mlflow.log_metric('return',result['return'])
        mlflow.log_metric('max_drawdown',result['max_drawdown'])
        try:
            mlflow.log_metric('win_trade',result['win_trade'])
            mlflow.log_metric('loss_trade',result['loss_trade'])
        except:
            pass
        mlflow.log_metric('total_trade',result['total_trade'])
        mlflow.log_metric('start_portfolio',result['start_portfolio'])
        mlflow.log_metric('final_portfolio',result['final_portfolio'])
        mlflow.end_run()

        return result

    def automated_test(self,asset=None,strategy_name=None,start_date=None,end_date=None,cash=100):
        sys.path.append(f"{os.getcwd()}/strategies")
        sys.path.append(f"../strategies/")

        from  Test_strategy import TestStrategy
        from sma import SMA
        from sma_rsi import SMA_RSI
        
        strategies ={
            "test":TestStrategy,
            "sma" : SMA,
            "sma_rsi":SMA_RSI
        } 
        
        f = open("./appsetting.json")
        
        args = json.load(f)
        print(os.getcwd())
        args = {}
        if strategy_name == None:
            strategy_name = args["indicator"]
        strategy = strategies[strategy_name]
        
        if asset == None:    
            asset= args["asset"]
        
        if start_date==None:
            start_date = args["dateRange"]["startDate"]

        if end_date==None:
            end_date = args["dateRange"]["endDate"]


        f.close()
        cerebro = self.prepare_cerebro(asset=asset,strategy=strategy,start_date=start_date,end_date=end_date,cash=cash) 
        result = self.run_test(cerebro)

        return result


    