#!/usr/bin/python3
import json
import time
import random
import uuid
import boto3
import signal

def sigint_handler(signum, frame):
    print('')
    print('CTRL-C detected. Exiting...')
    time.sleep(1)
    exit(1)

signal.signal(signal.SIGINT, sigint_handler)

if __name__ == "__main__":
    print("Replaying transactions")
    kns = boto3.client('kinesis')
    print("Connecting to kinesis")
    with open('transactions') as f:
        for line in f:
            time.sleep(0.05)
            request = {
                'StreamName': 'fixgateway',
                'Data': line,
                'PartitionKey': str(uuid.uuid4())
            }
            response = kns.put_record(**request)
            print("uploading {}: {}".format(line, response['ResponseMetadata']['HTTPStatusCode']))
