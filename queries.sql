# Kinesis Application

CREATE OR REPLACE STREAM "DESTINATION_SQL_STREAM" (ISIN VARCHAR(16), Volume INTEGER, Trades INTEGER, EndPrice REAL);
CREATE OR REPLACE PUMP "STREAM_PUMP" AS INSERT INTO "DESTINATION_SQL_STREAM"
SELECT STREAM ISIN, SUM("TradedVolume") AS Volume, SUM("NumberOfTrades") as Trades, Max("EndPrice")
FROM "SOURCE_SQL_STREAM_001"
GROUP BY ISIN, STEP("SOURCE_SQL_STREAM_001".ROWTIME BY INTERVAL '60' SECOND);

# Athena T-SQL

SELECT ISIN, MAX(MAVG_20) from (SELECT ISIN, TIMESTAMP, MAXPRICE,
       avg(maxprice) OVER (PARTITION BY isin
                             ORDER BY timestamp ROWS between 20 preceding and 1 preceding ) AS MAVG_20
FROM fsi406
ORDER BY ISIN, TIMESTAMP)
WHERE date(TIMESTAMP) = date('2019-11-22')
GROUP BY ISIN
ORDER BY ISIN

# Athena Moving Average

SELECT ISIN, TIMESTAMP, MAXPRICE,
       avg(maxprice) OVER (PARTITION BY isin
                             ORDER BY timestamp ROWS between 20 preceding and 1 preceding ) AS MAVG_20
FROM fsi406
ORDER BY ISIN, TIMESTAMP
