# Glue Configuration

## Create the Xetra database

1 - Open the Glue Service

2 - Click on Databases, then 'Add database'

3 - Type 'xetra' in the box and click 'Create'

## Create Glue job to convert xetra files to parquet

1 - Open the Glue Service

2 - Click on Jobs, then 'Add job'

3 - Give a name to your job, i.e. convert-xetra-to-parquet

4 - Create IAM Role
  - Select AWS service
  - Select Glue in the list of services
  - Click Next
  - Select the 'AWSGlueServiceRole' policy
  - Click on "Create policy"
  - Paste the policy below:
  ```
  {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "*",
            "Resource": [
                "arn:aws:s3:::fsi406*"
            ]
        }
    ]
  }
  ```
  - Name it - 'GlueBucketAccessPolicy'
  - Finish creating the policy, got back to the IAM Role creation table
  - Name the role 'FSI406-GlueRole' and click on CREATE

5 - Refresh the list of roles and select the role we just created

6 - Leave 'Type' as Spark

7 - Leave 'Glue version' as 'Spark 2.4, Python 3'

8 - Select 'A new script to be authored by you'

9 - Give the script a name, i.e. convert-to-parquet

10 - Accept the default paths.

11 - Click on 'Next', then 'Save Job and Edit Script'

12 - Paste the code from the glue file in this repo
  - Please change the bucket name in the load function (line 46)
  - Please change the bucket name in the write function (line 56)

13 - Select job and then click 'Action', then click 'Run job'

While the Glue job is running, let's complete our Athena configuration.

## Create table

1 - Open the Athena service

2 - Select the xetra database

3 - If this is the first time you're using Athena, you have to set up a bucket for results
  - click on the link and type the bucket we created earlier: s3://fsi406-athena-results-${user}

4 - In the new query window copy the sql below - replacing the bucket name with your bucket.

```
CREATE EXTERNAL TABLE `fsi406`(
  `isin` string,
  `mnemonic` string,
  `securitydesc` string,
  `securitytype` string,
  `currency` string,
  `securityid` string,
  `startprice` double,
  `maxprice` double,
  `minprice` double,
  `endprice` double,
  `tradedvolume` integer,
  `numberoftrades` integer,
  `timestamp` timestamp)
PARTITIONED BY (
  `year` string,
  `month` string,
  `day` string)
ROW FORMAT SERDE
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION
  's3://fsi406-parquet-${username}/'

```

Once the table has been created, let's check whether the Glue job has finished.

5 - Let's load the data partitions created by glue

```
MSCK REPAIR TABLE fsi406;
```

6 - Run a test query, let's see how many transactions we have

```
select count(*) from fsi406;
```

7 - Run a moving average query for two of the stocks:

```
SELECT ISIN, TIMESTAMP, MAXPRICE,
       avg(maxprice) OVER (PARTITION BY isin
                             ORDER BY timestamp ROWS between 60 preceding and 1 preceding ) AS MAVG_60
FROM fsi406
where ISIN = 'DE0006231004' OR ISIN = 'DE0007236101'
ORDER BY ISIN, TIMESTAMP
```
