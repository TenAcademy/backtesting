### Queries

### Show tables

```SQL
SELECT *
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

### Create table

```SQL
CREATE TABLE t1(
   id INT GENERATED ALWAYS AS IDENTITY,
   c2 VARCHAR(255) NOT NULL,
   PRIMARY KEY(id)
);
```
### Reference Table

```SQL
CREATE TABLE t2(
   id INT GENERATED ALWAYS AS IDENTITY,
   t1_id INT,
   c3 VARCHAR(255) NOT NULL,
   c4 VARCHAR(15),
   PRIMARY KEY(id),
   CONSTRAINT fk_t1
      FOREIGN KEY(t1_id) 
	  REFERENCES t1(id)
);
```

### select values

```SQL
SELECT select_list
FROM table_name
WHERE condition
ORDER BY sort_expression
```

### insert values

```SQL
INSERT INTO table_name(column1, column2, …)
VALUES (value1, value2, …);
```


// database schema
// contains three tables 
Table trading.strategy as st{
  id int [pk, increment]
  name varchar
  created_at timestamp
  
}
Table trading.bt_result{
  id int [pk, increment] // auto-increment
  return varchar
  total_trade int
  Winning_trades float4
  Losing_trades float4
  Max_drawdown  float4
  Sharpe_ratio float4
  start_portfolio float4
  final_portfolio float4
  strategy_id int [ref: > st.id]
  param_id int [ref: > pr.id]
}

Table trading.parameter as pr {
  id int [pk, increment]
  asset varchar
  indicator varchar
  start_date timestamp
  end_date timestamp
 }


# refactor 
assent and strategy from params table
