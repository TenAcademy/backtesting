import sys
import pandas as pd
from sqlalchemy import text
from sqlalchemy import create_engine
host="melachallengedatabase.crlafpfc5g5y.us-east-1.rds.amazonaws.com"
db="changdb"
port="5432"
user="changuser"
passw = "changpass"

engine = create_engine(f'postgresql+psycopg2://{user}:{passw}@{host}:{port}/{db}')

#  create tables using schema.sql file
def create_table():
    try:
        with engine.connect() as conn:    
            with open(f'/opt/database/schema.sql', "r") as file:
                    query = text(file.read())
                    conn.execute(query)
        print("Table created Successfull")
    except Exception as e:
        print("Error creating table",e)
        sys.exit(e)
# create_table()

#  use this if you want to accept the query as well then
def insert_to_table(table_name:str,df:pd.DataFrame, sqlQuery:str):
# def insert_to_table(table_name:str,df:pd.DataFrame):
    """
    sqlQuery format:
        INSERT INTO {table_name} (col1, col2, col3, col4, col5) VALUES(%s,%s,%s,%s,%s);
    """
        
    for _, row in df.iterrows():

        data = (row[0], row[1], row[2], row[3],row[4])

        try:
            # Execute the SQL command
            with engine.connect() as conn:
                
                a=conn.execute(sqlQuery,data)

            print("Successful!")

        except Exception as e:
            print("Error: ", e)
            
def delete_data(table_name:str,condition:str): # condition = "WHERE id=4": for example
    """
    condition format:
        WHERE col=value
    """

    # notice that the number of %s is equal to the number of columns
    sqlQuery = f"""DELETE FROM {table_name} {condition};""" 
    
    try:
        # Execute the SQL command
        with engine.connect() as conn:
            
            a=conn.execute(sqlQuery)

        print("Successful!")

    except Exception as e:
            print("Error: ", e)
            
def fetch_data(table_name:str,condition:str): # condition = "WHERE id=4": for example
    """
    condition format:
        WHERE col=value
    """

    # notice that the number of %s is equal to the number of columns
    sqlQuery = f"""SELECT * FROM {table_name} {condition};""" 
    
    try:
        # Execute the SQL command
        with engine.connect() as conn:
            
            a=conn.execute(sqlQuery)

        print("Successful!")
        return a.fetchall()

    except Exception as e:
            print("Error: ", e)