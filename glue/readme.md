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

5 - Leave 'Type' as Spark

6 - Leave 'Glue version' as 'Spark 2.4, Python 3'

7 - Select 'A new script to be authored by you'

8 - Give the script a name, i.e. convert-to-parquet

9 - Accept the default paths.

10 - Click on 'Next', then 'Save Job and Edit Script'

11 - Paste the code from the glue file in this repo and save the job

12 - Select job and then click 'Action' and click 'Run job'

## Create table 

1 - Open the Athena service

2 - Select the xetra database

3 - In the new query window copy the sql below - replacing the bucket name with your bucket.

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
4 - Once the table has been created, let's load the data partitions

```
MSCK REPAIR TABLE fsi406;
```

5 - Run a test query, let's see how many transactions we have

```
select count(*) from fsi406;
```
