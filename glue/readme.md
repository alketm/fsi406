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
