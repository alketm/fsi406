import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import to_timestamp
from pyspark.sql.functions import udf
from pyspark.sql.functions import year, month, dayofmonth

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
mergeCols = udf(lambda date, time: "{} {}:00".format(date,time))
customSchema = StructType([
    StructField("ISIN", StringType(), True),
    StructField("Mnemonic", StringType(), True),
    StructField("SecurityDesc", StringType(), True),
    StructField("SecurityType", StringType(), True),
    StructField("Currency", StringType(), True),
    StructField("SecurityID", StringType(), True),
    StructField("Date", StringType(), True),
    StructField("Time", StringType(), True),
    StructField("StartPrice", DoubleType(), True),
    StructField("MaxPrice", DoubleType(), True),
    StructField("MinPrice", DoubleType(), True),
    StructField("EndPrice", DoubleType(), True),
    StructField("TradedVolume", IntegerType(), True),
    StructField("NumberOfTrades", IntegerType(), True)
])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

glueContext = GlueContext(SparkContext.getOrCreate())

df = spark.read.format(
    "com.databricks.spark.csv").schema(customSchema).option(
    "quote", '"').option(
    "header", "true").option(
    "delimiter", ',').load('s3://fsi406-xetra-${user}/*/*.csv')

df1 = df.withColumn("Timestamp",to_timestamp(mergeCols(("Date"),("Time"))))
df2 = df1.drop("Date","Time")
df3 = df2.withColumn("Year",year("Timestamp")).withColumn("Month",month("Timestamp")).withColumn("Day",dayofmonth("Timestamp"))

dynaframe = DynamicFrame.fromDF(df3,glueContext,"xetra")
glueContext.write_dynamic_frame.from_options(
    frame = dynaframe,
    connection_type = "s3",
    connection_options = {"path": "s3://fsi406-parquet-${user}/", "partitionKeys" : ["year", "month", "day"], "mode":"overwrite"},
    format = "parquet")
