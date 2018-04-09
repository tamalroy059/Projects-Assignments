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
    sqs_name= os.environ['sqs']
    sqs_amazon_attribute_name = os.environ['sqsattribute']

    s3_key_list=[]

    for x in  event['Records']:
         s3_key_list.append(x['s3']['object']['key'])

    BUCKET = "slstests4"

    client =session.client('s3')
    sqs = session.resource('sqs', region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName=sqs_name)
    queue_amazon_attribute=sqs.get_queue_by_name(QueueName=sqs_amazon_attribute_name)
    sns= session.client('sns')


    for s3_key in s3_key_list:
        result = client.get_object(Bucket=BUCKET, Key=s3_key)


        # Read the object (not compressed):
        text = result["Body"].read().decode()
        isbn_list = text.split('\r')
        isbn_list = list(set(isbn_list))
        length_isbn_list = len(isbn_list)

        # print 'length isbn list = ' + str(length_isbn_list)
        # length_isbn_list = 10



        if 'Daily_Ingestion' in s3_key:
            ingestion_schedule='Daily'
        else:
            ingestion_schedule='False'

        print 'ingestion_schedule' + ingestion_schedule

        for i in range(1,length_isbn_list):
            if len(isbn_list[i])>0:
                queue.send_message(MessageBody=isbn_list[i], MessageAttributes= {
                'process_date': {
                    'StringValue': process_date,
                    'DataType': 'String'
                },
                'file_name': {
                    'StringValue': s3_key,
                    'DataType': 'String'
                },
                'schedule': {
                    'StringValue': ingestion_schedule,
                    'DataType': 'String'
                }
                })


                # queue_amazon_attribute.send_message(MessageBody=isbn_list[i])



    message = {"Queue notification": "The new file has been uploaded"}

    sns.publish(TopicArn="arn:aws:sns:us-east-1:822605674378:dev-aws-python-trigger", Message=json.dumps({'default': json.dumps(message)}), MessageStructure='json')

    return message
