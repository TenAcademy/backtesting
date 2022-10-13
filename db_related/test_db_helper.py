import sys
from sqlalchemy import text
import json
from sqlalchemy import create_engine


host="melachallengedatabase.crlafpfc5g5y.us-east-1.rds.amazonaws.com"
db="changdb"
port="5432"
user="changuser"
passw = "changpass"

# engine = create_engine(f'postgresql://{user}@{host}/{db}')
engine = create_engine(f'postgresql+psycopg2://{user}:{passw}@{host}:{port}/{db}')

create_schema = """
    CREATE SCHEMA g1;
"""

select_parameters_query = """
    SELECT *
    FROM g1.parameters
    ORDER BY parameters.id;
"""

select_backtests_results_query = """
    SELECT *
    FROM g1.backtests_results
    ORDER BY backtests_results.id;
"""

select_users_query = """
    SELECT *
    FROM g1.users
    ORDER BY users.id;
"""

insert_parameters_query = """
    INSERT INTO g1.parameters(asset, starting_money, strategy, start_date, end_date)
    VALUES ('TSLA', 1000000, 'test strategy', '1980-01-01','2005-01-01');
"""

insert_users_query = """
    INSERT INTO g1.users(user_name, password)
    VALUES ('Nati', 'password II');
"""

insert_backtests_results_query = """
    INSERT INTO g1.backtests_results(starting_portfolio, final_portfolio, loss_trade, win_trade, total_trade, return, sharp_ratio)
    VALUES (1000000, 100000000, 'loss trade', 'win trade', 'total trade', 100, 0.268);
"""

create_query = """
DROP TABLE IF EXISTS g1.users;
CREATE TABLE g1.users(
    id INT GENERATED ALWAYS AS IDENTITY,
    user_name VARCHAR(15) NOT NULL,
    password VARCHAR(15) NOT NULL,
    posting_date DATE NOT NULL DEFAULT CURRENT_DATE,
    posting_time TIME NOT NULL DEFAULT CURRENT_TIME
);

DROP TABLE IF EXISTS g1.parameters;
CREATE TABLE g1.parameters(
    id INT GENERATED ALWAYS AS IDENTITY,
    asset VARCHAR(255) NOT NULL,
    starting_money FLOAT NOT NULL,
    strategy VARCHAR(20) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    posting_date DATE NOT NULL DEFAULT CURRENT_DATE,
    posting_time TIME NOT NULL DEFAULT CURRENT_TIME
);

DROP TABLE IF EXISTS g1.strategy;
CREATE TABLE g1.strategy(
    id INT GENERATED ALWAYS AS IDENTITY,
    strategy_name VARCHAR(15) NOT NULL,
    posting_date DATE NOT NULL DEFAULT CURRENT_DATE,
    posting_time TIME NOT NULL DEFAULT CURRENT_TIME
);

DROP TABLE IF EXISTS g1.asset;
CREATE TABLE g1.asset(
    id INT GENERATED ALWAYS AS IDENTITY,
    asset_name VARCHAR(15) NOT NULL,
    posting_date DATE NOT NULL DEFAULT CURRENT_DATE,
    posting_time TIME NOT NULL DEFAULT CURRENT_TIME
);

DROP TABLE IF EXISTS g1.backtests_results;
CREATE TABLE g1.backtests_results(
    id INT GENERATED ALWAYS AS IDENTITY,
    strategy_id INT,
    parameter_id INT,
    starting_portfolio FLOAT NOT NULL,
    final_portfolio FLOAT NOT NULL,
    loss_trade INT NOT NULL,
    win_trade INT NOT NULL,
    total_trade INT NOT NULL,
    return FLOAT NOT NULL,
    sharpe_ratio FLOAT NOT NULL,
    max_drawdown FLOAT NOT NULL,
    posting_date DATE NOT NULL DEFAULT CURRENT_DATE,
    posting_time TIME NOT NULL DEFAULT CURRENT_TIME

    CONSTRAINT fk_parameters_1
    FOREIGN KEY(strategy_id),
    REFERENCES g1.strategy(id)

    CONSTRAINT fk_parameters_2
    FOREIGN KEY(parameter_id),
    REFERENCES g1.parameter(id)
);
"""
# https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-date/


with engine.connect() as conn:
    # query = text("Show table")
    a = conn.execute(select_users_query)
    print(a.fetchall())
