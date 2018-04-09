import os

import boto
import boto3
import scrapy
from boto.s3.key import Key
import amazon_title_extract

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    access_key_id = "AKIAJYWCN7X4U6DYFWAA"
    access_key = "BPGc2daOQ9vDc87FpRvXQU3t7q/PbXLeSmRMk/v7"
    session = boto3.Session(access_key_id, access_key)

    sqs_name = "dev-aws-python-daily-scrape"
    sqs_as = "dev-aws-python-already-scraped"
    sqs = session.resource('sqs', region_name='us-east-1')
    dynamodb = session.resource('dynamodb', region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName=sqs_name)
    sqs_as_queue = sqs.get_queue_by_name(QueueName=sqs_as)

    amazon_title_scrape_table = dynamodb.Table('amazon-daily-title-scrape-result')

    # s3 credentials
    access_key_id = "AKIAJYWCN7X4U6DYFWAA"
    access_key = "BPGc2daOQ9vDc87FpRvXQU3t7q/PbXLeSmRMk/v7"
    bucket_name = "slstests4"
    key = boto.connect_s3(access_key_id, access_key)
    bucket = key.get_bucket(bucket_name, validate=False)
    k = Key(bucket)


    #phantom js call to extract values
    amazon_extract = amazon_title_extract.amazon_title_extract()

    def start_requests(self):

        empty=0
        queue = self.sqs.get_queue_by_name(QueueName=self.sqs_name)

        while empty<5:

            response_asin = queue.receive_messages(VisibilityTimeout=100, MaxNumberOfMessages=10,
                                                   MessageAttributeNames=['file_name', 'process_date', 'EISBN'])

            if len(response_asin)==0:
                empty+=1
            else:
                empty=0

            for i, queue_item in enumerate(response_asin):
                eisbn = queue_item.message_attributes.get('EISBN').get('StringValue')
                file_name = queue_item.message_attributes.get('file_name').get('StringValue')

                request_url ='https://www.amazon.com/dp/%s'%(queue_item.body)
                process_date = queue_item.message_attributes.get('process_date').get('StringValue')[:10]
                yield scrapy.Request(url=request_url, meta={'process date': process_date, 'file_name': file_name, 'eisbn': eisbn, 'item': queue_item, 'insert_queue':self.sqs_as_queue , 'dont_merge_cookies': True, 'cookiejar': i}, callback=self.parse)


    def parse(self, response):


        page = response.url.split("/")[-1]
        filename = '/home/ec2-user/python_projects/scrapy_project/scrapy_project/amz_bot/scraped/%s.html' % (page)
        with open(filename, 'wb') as f:
            f.write(response.body)


        if os.path.getsize(filename) > 300000:
            queue_item = response.meta['item']
            response.meta['insert_queue'].send_message(MessageBody=page,MessageAttributes= {
                'process_date': {
                    'StringValue': response.meta['process date'],
                    'DataType': 'String'
                },
                'file_name': {
                    'StringValue': response.meta['file_name'],
                    'DataType': 'String'
                },
                'eisbn': {
                    'StringValue': response.meta['eisbn'],
                    'DataType': 'String'
                }
                }
                                                       )

            self.k.key = 'ScrapedPages/%s/' % (response.meta['process date']) + page + '.html'
            self.k.set_contents_from_filename(filename=filename, num_cb=20)

            queue_item.delete()
            self.log('Saved file %s' % filename)
            os.remove(filename)
        else:
            os.remove(filename)



    def response_is_ban(self, request, response):
        print "ban response here = "+ str(response)
        return b'banned' in response.body

    def exception_is_ban(self, request, exception):
        print "exception response here = " + str(exception)
        return None












