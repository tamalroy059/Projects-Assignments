import boto
import boto3
import scrapy
from boto.s3.key import Key


class msg_queue_assistance:

    def __init__(self, avg_round=5):
        self._round=avg_round

    def change_round(self,avg_round):
        self._round=avg_round

    def extract_queue_5_round(self, sqs_name = "dev-aws-python-daily-scrape", attributes=['file_name', 'process_date', 'EISBN']):

        access_key_id = "AKIAJYWCN7X4U6DYFWAA"
        access_key = "BPGc2daOQ9vDc87FpRvXQU3t7q/PbXLeSmRMk/v7"
        session = boto3.Session(access_key_id, access_key)

        # sqs_name = "dev-aws-python-daily-scrape"

        sqs = session.resource('sqs', region_name='us-east-1')



        queue = sqs.get_queue_by_name(QueueName=sqs_name)

        asin_list = []

        empty = 0

        round=0

        while empty < 5 and round<self._round:

            response_asin = queue.receive_messages(VisibilityTimeout=100, MaxNumberOfMessages=10,
                                                   MessageAttributeNames=attributes)
            if len(response_asin) == 0:
                empty += 1
            else:
                empty = 0
                round +=1


            for i, queue_item in enumerate(response_asin):

                item_tuple=(queue_item.body,)
                for attribute in attributes:
                    if attribute=='process_date':
                        item_tuple=item_tuple+(queue_item.message_attributes.get(attribute).get('StringValue')[:10],)
                    else:
                        item_tuple = item_tuple + (queue_item.message_attributes.get(attribute).get('StringValue'),)

                asin_list.append(item_tuple)

                queue_item.delete()

        return asin_list

    def insert_msg_queue(self, asin_list):

        access_key_id = "AKIAJYWCN7X4U6DYFWAA"
        access_key = "BPGc2daOQ9vDc87FpRvXQU3t7q/PbXLeSmRMk/v7"
        session = boto3.Session(access_key_id, access_key)

        sqs_as = "dev-aws-python-already-scraped"
        sqs = session.resource('sqs', region_name='us-east-1')
        sqs_as_queue = sqs.get_queue_by_name(QueueName=sqs_as)


        for asin in asin_list:
            sqs_as_queue.send_message(MessageBody=asin[0],MessageAttributes= {
                'process_date': {
                    'StringValue': asin[2],
                    'DataType': 'String'
                },
                'eisbn': {
                    'StringValue': asin[3],
                    'DataType': 'String'
                }
                })


    def insert_daily_list_queue(self, asin_list):
        access_key_id = "AKIAJYWCN7X4U6DYFWAA"
        access_key = "BPGc2daOQ9vDc87FpRvXQU3t7q/PbXLeSmRMk/v7"
        session = boto3.Session(access_key_id, access_key)

        sqs_name = "dev-aws-python-daily-scrape"
        sqs = session.resource('sqs', region_name='us-east-1')
        sqs_queue = sqs.get_queue_by_name(QueueName=sqs_name)

        for asin in asin_list:
            sqs_queue.send_message(MessageBody=asin[0], MessageAttributes={
                'process_date': {
                    'StringValue': asin[2],
                    'DataType': 'String'
                },
                'EISBN': {
                    'StringValue': asin[3],
                    'DataType': 'String'
                },
                'file_name': {
                    'StringValue': asin[1],
                    'DataType': 'String'
                }
            })




