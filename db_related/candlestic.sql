-- https://towardsdatascience.com/how-to-store-financial-market-data-for-backtesting-84b95fc016fc

CREATE TABLE candlestick (
 “id” INTEGER PRIMARY KEY AUTOINCREMENT,
 “timezone” TEXT NOT NULL,
 “timestamp” DATETIME NOT NULL,
 “open” DECIMAL(12, 6) NOT NULL,
 “high” DECIMAL(12, 6) NOT NULL,
 “low” DECIMAL(12, 6) NOT NULL,
 “close” DECIMAL(12, 6) NOT NULL,
 “volume” DECIMAL(12, 6) NOT NULL
);

select * from candlestick where date(timestamp)='2018-01-12' limit 10;

create index idx_timestamp on candlestick(timestamp);

ls -ltr dax*

