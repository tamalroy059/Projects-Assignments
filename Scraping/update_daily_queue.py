
import boto3
import os
import json
import datetime


class update_daily_queue:

    def __init__(self):
        access_key_id = "AKIAJYWCN7X4U6DYFWAA"
        access_key = "BPGc2daOQ9vDc87FpRvXQU3t7q/PbXLeSmRMk/v7"

        session = boto3.Session(access_key_id, access_key)

        process_date = str(datetime.datetime.now())[:19]

        region_name = 'us-east-1'

        sqs_for_daily_scrape = "dev-aws-python-daily-scrape"

        sqs = session.resource('sqs', region_name='us-east-1')
        queue_daily_scrape = sqs.get_queue_by_name(QueueName=sqs_for_daily_scrape)

        dynamodb = session.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table("amazon-daily-title-list")

        response = table.scan(
            AttributesToGet=[
                'ASIN',
                'EISBN',
                'file_name'
            ]
        )

        print "total count = " + str(len(response['Items']))


        for item in response['Items']:
            queue_daily_scrape.send_message(MessageBody=item['ASIN'], MessageAttributes={
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

def main():
    update_daily_queue()

if __name__ == "__main__":
    main()