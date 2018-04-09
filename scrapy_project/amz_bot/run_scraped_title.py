import amazon_title_extract
import boto3
import os

def main():
    access_key_id = "AKIAJYWCN7X4U6DYFWAA"
    access_key = "BPGc2daOQ9vDc87FpRvXQU3t7q/PbXLeSmRMk/v7"
    session = boto3.Session(access_key_id, access_key)
    sqs = session.resource('sqs', region_name='us-east-1')
    dynamodb = session.resource('dynamodb', region_name='us-east-1')
    sqs_as = "dev-aws-python-already-scraped"
    sqs_as_queue = sqs.get_queue_by_name(QueueName=sqs_as)

    empty=0

    amz_obj=amazon_title_extract.amazon_title_extract()

    amazon_title_scrape_table = dynamodb.Table('amazon-daily-title-scrape-result')

    while (empty<5):

        response = sqs_as_queue.receive_messages(VisibilityTimeout=30, MaxNumberOfMessages=10,
                                             MessageAttributeNames=['process_date','eisbn','file_name'])

        if len(response)==0:
            empty+=1
        else:
            empty=0

        for queue_item in response:
            filename = '/home/ec2-user/python_projects/scrapy_project/scrapy_project/amz_bot/scraped/%s.html' % (queue_item.body)
            amz_data_point={}
            amz_data_point = amz_obj.extract_title_info(queue_item.body)

            amz_data_point['EISBN'] = queue_item.message_attributes.get('eisbn').get('StringValue')
            amz_data_point['file_name'] = queue_item.message_attributes.get('file_name').get('StringValue')
            amz_data_point['process_date'] = queue_item.message_attributes.get('process_date').get('StringValue')
            amz_data_point['id'] = amz_data_point['ASIN'] + '-' + amz_data_point['process_date']
            # insert into dynamodb
            amazon_title_scrape_table.put_item(Item=amz_data_point)

            os.remove(filename)
            queue_item.delete()



if __name__ == "__main__":
    main()