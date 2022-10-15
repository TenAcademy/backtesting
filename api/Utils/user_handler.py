import hashlib
import pandas as pd

import sys
import json
import pandas as pd
from sqlalchemy import text
from sqlalchemy import create_engine
from datetime import datetime, date

host="melachallengedatabase.crlafpfc5g5y.us-east-1.rds.amazonaws.com"
db="changdb"
port="5432"
user="changuser"
passw = "changpass"

engine = create_engine(f'postgresql+psycopg2://{user}:{passw}@{host}:{port}/{db}')

def insert_to_table(df:pd.DataFrame, sqlQuery:str):
# def insert_to_table(table_name:str,df:pd.DataFrame):
    """
    sqlQuery format:
        INSERT INTO {table_name} (col1, col2, col3, col4, col5) VALUES(%s,%s,%s,%s,%s);
    """
    now=datetime.now()
    created_on=date.strftime(now,"%Y/%m/%d")
        
    for _, row in df.iterrows():

        data = (row[0], row[1],row[2], created_on )

        # try:
            # Execute the SQL command
        with engine.connect() as conn:
            
            a=conn.execute(sqlQuery,data)

        print("Successful!")

        # except Exception as e:
        #     return False,e




def register(user:dict):
    
    hpwd=hashlib.md5(user["password"].encode()).hexdigest()
    user["password"]=hpwd
    
    try:
        df=pd.DataFrame([user])
        #save to db
        query="INSERT INTO users (full_name,email, password, created_time) VALUES(%s,%s,%s,%s)"
        insert_to_table(df,query)
        return True,"Created"

    except Exception as e:
        return False,e