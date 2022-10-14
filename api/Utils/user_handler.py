import hashlib
import pandas as pd
import json

def register(user:dict):
    
    hpwd=hashlib.md5(user["pass"].encode()).hexdigest()
    user["pass"]=hpwd
    
    try:
        df=pd.DataFrame([user])
        #save to db
        return True,"Created"

    except Exception as e:
        return False,e