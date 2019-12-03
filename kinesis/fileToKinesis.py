import json
import time
import random
import uuid
import boto3
import signal
import csv

def txToDict(msg):
    txDict = {}
    txDict["ISIN"] = msg[0]
    txDict["Mnemonic"] = msg[1]
    txDict["SecurityDesc"] = msg[2]
    txDict["SecurityType"] = msg[3]
    txDict["Currency"] = msg[4]
    txDict["SecurityID"] = msg[5]
    txDict["Date"] = msg[6]
    txDict["Time"] = msg[7]
    txDict["StartPrice"] = msg[8]
    txDict["MaxPrice"] = msg[9]
    txDict["MinPrice"] = msg[10]
    txDict["EndPrice"] = msg[11]
    txDict["TradedVolume"] = msg[12]
    txDict["NumberOfTrades"] = msg[13]
    return txDict

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
        csv_reader = csv.reader(f)
        for line in csv_reader:
            time.sleep(1)
            data = txToDict(line)
            request = {
                'StreamName': 'fsi406',
                'Data': json.dumps(data),
                'PartitionKey': str(uuid.uuid4())
            }
            response = kns.put_record(**request)
            print("uploading transaction {} {}".format(str(data),response['ResponseMetadata']['HTTPStatusCode']))
