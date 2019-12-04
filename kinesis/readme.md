# Kinesis Configuration

## Create Kinesis Data Stream

1 - Go to the Kinesis service

2 - Create new Data Stream

3 - name it 'fsi406' and type 1 for number of shards

4 - Click on 'Create'

# Script to write data to Kinesis

1 - Create fileToKinesis.py file in Cloud9 and copy code from github (or run git clone)

2 - Upload the 'transactions' file to the Cloud9 environment (Click on File -> Upload local file)

3 - Open a 'New Terminal' on the Cloud9 interface

4 - run the script "python2 fileToKinesis.py"

5 - let the script run as it will now put data into the stream we just created

## Create Kinesis Data Analytics application

1 - Go to the Data Analytics link (on the left)

2 - Click on 'Create application'

3 - Name your application 'fsi406' and leave Runtime selection as SQL

4 - Click on 'Create application'

5 - On the next screen, click on Connect streaming data

6 - On the next screen, leave the default selection of 'Kinesis data stream' and choose fsi406 in the drop down box

7 - Leave all other options as default

8 - Click on discover schema - we should now see our schema in the console

9 - Click on 'Save and Continue'

10 - Click on "Go to SQL editor"

11 - Paste the application code below then click on 'Save and run SQL'

```
CREATE OR REPLACE STREAM "MAVG_1_SQL_STREAM" (ISIN VARCHAR(16), Volume INTEGER, Trades INTEGER, EndPrice REAL);
CREATE OR REPLACE STREAM "MAVG_5_SQL_STREAM" (ISIN VARCHAR(16), Volume INTEGER, Trades INTEGER, EndPrice REAL);

CREATE OR REPLACE PUMP "STREAM_1_PUMP" AS INSERT INTO "MAVG_1_SQL_STREAM"
SELECT STREAM ISIN, SUM("TradedVolume") AS Volume, SUM("NumberOfTrades") as Trades, Max("EndPrice")
FROM "SOURCE_SQL_STREAM_001"
GROUP BY ISIN, STEP("SOURCE_SQL_STREAM_001".ROWTIME BY INTERVAL '60' SECOND);

CREATE OR REPLACE PUMP "STREAM_5_PUMP" AS INSERT INTO "MAVG_5_SQL_STREAM"
SELECT STREAM ISIN, SUM("TradedVolume") AS Volume, SUM("NumberOfTrades") as Trades, Max("EndPrice")
FROM "SOURCE_SQL_STREAM_001"
GROUP BY ISIN, STEP("SOURCE_SQL_STREAM_001".ROWTIME BY INTERVAL '5' MINUTE);
```

12 - Let's go to Athena to run a moving average on the historical data

13 - Now we will connect our KDA data streams to the lambda functions that will send this data to CloudWatch
