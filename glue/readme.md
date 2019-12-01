# Glue Configuration

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
11 - Paste the code from the glue file in this repo and save
12 - #
