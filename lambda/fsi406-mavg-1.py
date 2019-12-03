from __future__ import print_function

import boto3
import base64
import json

cw = boto3.client('cloudwatch')

def lambda_handler(event, context):

    # print("Received event: " + json.dumps(event, indent=2))
    for record in event['records']:
        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record['data'])
        data = json.loads(payload)
        print("Decoded payload: " + str(payload))
        response = cw.put_metric_data(
            MetricData = [
                {
                    'MetricName': 'MAVG_1',
                    'Dimensions': [
                        {
                            'Name': 'ISIN',
                            'Value': data['ISIN']
                        }
                    ],
                    'Unit': 'None',
                    'Value': data['ENDPRICE'],
                    'StorageResolution': 1
                }
            ],
            Namespace = 'XETRA-TW'
        )
