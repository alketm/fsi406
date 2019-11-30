# FSI 406

In this session we will use the Deutsche Boerse Xetra dataset, at https://github.com/Deutsche-Boerse/dbg-pds, to demonstrate the capabilities of Kinesis, Glue, & Athena.

## Create Cloud9 Environment

1 - Go to the Cloud9 service

2 - Create environment - name it FSI406-${user} - click Next

3 - Select: Create a new instance for environment (EC2), choose a t2.micro instance type, platform Amazon Linux

4 - Leave the rest at default and click 'Next step'

5 - Review and click 'Create environment'

6 - Wait until environment is ready.

7 - Click on the green '+' icon and select 'New Terminal'


## Retrieve DB Xetra Dataset 

1 - We will first create a bucket to store a subset of the DB Xetra dataset:

Go to the AWS Console in your account, select the S3 service, and create a bucket with the default settings, give it a name in this format: fsi406-xetra-${username}, i.e. fsi406-xetra-johnd

2 - Copy the Nov 2019 records to your bucket:
```
$ aws s3 cp s3://deutsche-boerse-xetra-pds/ s3://fsi406-xetra-${username} --exclude "*" --include "2019-11*" --recursive
```
2 - Let's create a local copy of one day of data - i.e. Nov 22nd
```
$ aws s3 cp s3://deutsche-boerse-xetra-pds/ . --exclude "*" --include "2019-11-22*" --recursive
```
3 - Let's combine all the records on this day on a single file:
```
$ for file in `ls 2019-11-22/*.csv`; do grep -v ISIN $file >> transactions; done
```
At this point we have a whole month of records from Xetra in our bucket and we also have a file that contains all the records of a single day. We will use this file as the source of the data that we will be streaming into Kinesis for processing

## Upgrade pip and install boto3

1 - sudo pip install --upgrade pip

2 - pip install boto3
