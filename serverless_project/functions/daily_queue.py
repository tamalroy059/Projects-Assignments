import boto3
import os
import json
import datetime

access_key_id = "AKIAJYWCN7X4U6DYFWAA"
access_key = "BPGc2daOQ9vDc87FpRvXQU3t7q/PbXLeSmRMk/v7"

session = boto3.Session(access_key_id, access_key)


def Queue_handler(event, context):

    process_date = str(datetime.datetime.now())[:19]

    region_name= os.environ['region']


    sqs_for_daily_scrape = os.environ['sqsdaily']

    sqs = session.resource('sqs', region_name='us-east-1')
    queue_daily_scrape = sqs.get_queue_by_name(QueueName=sqs_for_daily_scrape)

    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(os.environ['AMAZON_DAILY_TITLE_LIST_TABLE'])

    response = table.scan(
            AttributesToGet=[
                'ASIN',
                'EISBN',
                'file_name'
            ]
        )

    print "response here"

    print response

    for item in response['Items']:
        queue_daily_scrape.send_message(MessageBody=item['ASIN'], MessageAttributes= {
        'process_date': {
            'StringValue': process_date,
            'DataType': 'String'
            },
        'EISBN': {
            'StringValue': item['EISBN'],
            'DataType': 'String'
            },
        'file_name': {
            'StringValue': item['file_name'],
            'DataType': 'String'
            }
        })


    # region_name= os.environ['region']
    # sqs_name= os.environ['sqs']
    #
    # sqs_amazon_attribute_name = os.environ['sqsattribute']
