# FSI 406

In this session we will use the Deutsche Boerse Xetra dataset, at https://github.com/Deutsche-Boerse/dbg-pds, to demonstrate the capabilities of Kinesis, Glue, & Athena.

## Create your S3 buckets

1 - Create a bucket to hold your copy of data from Xetra, name it: fsi406-xetra-${user}

2 - Create a bucket to hold an optimized copy of data from Xetra, name it: fsi406-parquet-${user}

3 - If you've not used Athena before, create a bucket to hold Athena results, name it: s3://fsi406-athena-results-${user}

## Create Cloud9 Environment

1 - Go to the Cloud9 service

2 - Create environment - name it FSI406-${user} - click Next

3 - Select: Create a new instance for environment (EC2), choose a t2.micro instance type, platform Amazon Linux

4 - Set 'Cost Saving setting' to 1 hour

5 - Leave the rest at default and click 'Next step'

6 - Review and click 'Create environment'

7 - Wait until environment is ready.

8 - Click on the green '+' icon and select 'New Terminal'


## Retrieve DB Xetra Dataset

1 - We will first create a bucket to store a subset of the DB Xetra dataset:

Go to the AWS Console in your account, select the S3 service, and create a bucket with the default settings, give it a name in this format: fsi406-xetra-${username}, i.e. fsi406-xetra-johnd

2 - Copy the Nov 2019 records to your bucket:
```
$ aws s3 cp s3://deutsche-boerse-xetra-pds/ s3://fsi406-xetra-${username} --exclude "*" --include "2019-11*" --recursive
```

At this point we have a whole month of records from Xetra in our bucket.

## Upgrade pip and install boto3

1 - sudo pip install --upgrade pip

2 - pip install boto3

## Go to the Glue section
