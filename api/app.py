from flask import Flask
from flask import request
from producer import produce
import json
import os
import sys

cwd=os.getcwd()
sys.path.append(f"{cwd}/Utils/")
sys.path.append(f"{cwd}/../scripts/")

from session import log_in
from user_handler import *
from backtester import backtester

tester=backtester()
app = Flask(__name__)

@app.route("/check")
def check():
    return "your API is up!"


@app.route("/userSession",methods=["POST"])
def login():
    content=request.json
    
    result = log_in(content)
    return {"Success":result}

@app.route("/register",methods=["POST"])
def user_handler():
    content = request.json
    
    result = register(content)
    return {"Success":result[0],"Msg":str(result[1])}

@app.route("/backtest",methods=["POST"])
def backtest():
    content = request.json

    asset = content["asset"]
    strategy = content["strategy"]
    start_date = content["start_date"]
    end_date=content["end_date"]
    cash = content["cash"]

    produce("g1-SCENES_TOPIC",json.dumps(content))
    result=tester.automated_test(asset,strategy,start_date,end_date,cash)
    produce("g1-RESULTS_TOPIC",json.dumps(result))

    return result




    
   
        

    

app.run(port=5001,debug=True)