import hashlib

import sys
import json
import pandas as pd
from sqlalchemy import text
from sqlalchemy import create_engine
host="melachallengedatabase.crlafpfc5g5y.us-east-1.rds.amazonaws.com"
db="changdb"
port="5432"
user="changuser"
passw = "changpass"

engine = create_engine(f'postgresql+psycopg2://{user}:{passw}@{host}:{port}/{db}')


def fetch_data(table_name:str,condition:str): # condition = "WHERE id=4": for example
    """
    condition format:
        WHERE col=value
    """
    
    sqlQuery = f"""SELECT * FROM {table_name} {condition};""" 
    
    try:
        # Execute the SQL command
        with engine.connect() as conn:
            
            a=conn.execute(sqlQuery)

        print("Successful!")
        return a.fetchall()

    except Exception as e:
            print("Error: ", e)



# pwd = "5f4dcc3b5aa765d61d8327deb882cf99"
def log_in(user:dict):
    email=user["email"]
    password=user["password"]
    hpwd=hashlib.md5(password.encode()).hexdigest()
    condition = f"WHERE password='{hpwd}' AND email='{email}'"
    res=fetch_data("users",condition)
    if res:
        return True
    else:
        return False
