import boto3
import os
import bottlenose
import xml.etree.ElementTree as ET
import urllib2
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import re



access_key_id = "AKIAJYWCN7X4U6DYFWAA"
access_key = "BPGc2daOQ9vDc87FpRvXQU3t7q/PbXLeSmRMk/v7"

session = boto3.Session(access_key_id, access_key)

class amazon_api:

    def __init__(self):
        self._amazon=None
        # self._amazon_list=self.__amazon_product_advertising_api_extract(self._itemid)
        # self._goodreads_list = []
        # for item in self._amazon_list:
        #     self._goodreads_list.append(self.__goodread_data(item['EISBN']))


    def initialize_amazon(self):
        key_access = 'AKIAIO6ZO7NXRZIL2M4A'
        key_secret = '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'
        associate_tag = 'httpwwwopen01 - 20'

        self._amazon = bottlenose.Amazon(key_access, key_secret, associate_tag, Region='US')

    def amazon_product_advertising_api_extract(self,itemid):
        amazon=self._amazon

        # BrowseNodes,EditorialReview,Similarities,ItemAttributes
        xml_response = amazon.ItemLookup(ItemId=itemid, IdType='ASIN',
                                         ResponseGroup='Offers,OfferFull,SalesRank,ItemAttributes')
        # xml_response = amazon.ItemLookup(ItemId=itemid, ResponseGroup='BrowseNodes,EditorialReview,Similarities,ItemAttributes')
        root = ET.fromstring(xml_response)

        for items in root:
            if items.tag.split('}')[1] == 'Items':
                items_list = []
                for item in items:
                    if item.tag.split('}')[1] == 'Item':
                        # item_des = self.__initialize_item_amazon()
                        item_des = {}
                        for attr in item:
                            if attr.tag.split('}')[1] == 'ASIN':
                                item_des[attr.tag.split('}')[1]] = attr.text
                            if attr.tag.split('}')[1] == 'EditorialReviews':
                                editorialReviews = []
                                for editorialReview in attr:
                                    if editorialReview.tag.split('}')[1] == 'EditorialReview':
                                        editorialReviewAttr_d = dict()
                                        for editorialReviewAttr in editorialReview:
                                            editorialReviewAttr_d[
                                                editorialReviewAttr.tag.split('}')[1]] = editorialReviewAttr.text
                                        editorialReviews.append(editorialReviewAttr_d)
                                item_des[attr.tag.split('}')[1]] = editorialReviews

                            if attr.tag.split('}')[1] == 'SalesRank':
                                item_des[attr.tag.split('}')[1]] = attr.text

                            if attr.tag.split('}')[1] == 'OfferSummary':
                                for offer in attr:
                                    if offer.tag.split('}')[-1] == 'LowestNewPrice':
                                        item_des['LowestNewPrice'] = offer[0].text

                                    if offer.tag.split('}')[-1] == 'LowestUsedPrice':
                                        item_des['LowestUsedPrice'] = offer[0].text

                            if attr.tag.split('}')[1] == 'ItemAttributes':
                                for itemAttributes in attr:
                                    if itemAttributes.tag.split('}')[-1] == 'Binding':
                                        item_des['Binding'] = itemAttributes.text

                                    if itemAttributes.tag.split('}')[-1] == 'Publisher':
                                        item_des['Publisher'] = itemAttributes.text
                                    if itemAttributes.tag.split('}')[-1] == 'Title':
                                        item_des['Title'] = itemAttributes.text
                                    if itemAttributes.tag.split('}')[-1] == 'Author':
                                        item_des['Author'] = itemAttributes.text
                                    if itemAttributes.tag.split('}')[-1] == 'PublicationDate':
                                        item_des['PublicationDate'] = itemAttributes.text
                                    if itemAttributes.tag.split('}')[-1] == 'NumberOfPages':
                                        item_des['NumberOfPages'] = itemAttributes.text
                                    if itemAttributes.tag.split('}')[-1] == 'ReleaseDate':
                                        item_des['ReleaseDate'] = itemAttributes.text
                                    if itemAttributes.tag.split('}')[-1] == 'EISBN':
                                        item_des['EISBN'] = itemAttributes.text
                                    if itemAttributes.tag.split('}')[-1] == 'PackageDimensions':
                                        for packageDimensions in itemAttributes:
                                            if packageDimensions.tag.split('}')[-1] == 'Weight':
                                                item_des['Weight'] = packageDimensions.text
                                                break

                        items_list.append(item_des)

                return items_list

        return None


    ####
    def goodread_data(self, eisbn):
        ID = eisbn
        # dictionary = self.__initialize_item_goodreads()
        dictionary = {}
        try:
            response = urllib2.urlopen('https://www.goodreads.com/book/isbn/%s?key=aTGB9VRWJxpCzfqykxUlA' % ID)
            xml = response.read()

            try:
                dictionary['parsed_isbn'] = ID

                try:
                    temp = self.goodreadsParser(xml, '<isbn13>').replace('<![CDATA[', '').replace(
                        ']]>', '')
                    if len(temp)>0:
                        dictionary['primaryisbn13'] = temp
                except:
                    pass

                try:
                    temp = self.goodreadsParser(xml, '<publication_year>') + '-' + self.goodreadsParser(
                        xml, '<publication_month>') + '-' + self.goodreadsParser(xml, '<publication_day>')
                    if len(temp)>0:
                        dictionary['pub_date'] = temp
                except:
                    pass

                try:
                    temp = self.goodreadsParser(xml, '<title>').replace('<![CDATA[', '').replace(']]>', '')
                    if len(temp)>0:
                        dictionary['title'] = temp
                except:
                    pass

                try:
                    temp = self.goodreadsParser(xml, '<ratings_sum type="integer">')
                    if len(temp)>0:
                        dictionary['ratings_sum'] = temp
                except:
                    pass
                try:
                    temp = self.goodreadsParser(xml, '<ratings_count type="integer">')
                    if len(temp)>0:
                        dictionary['ratings_count'] = temp
                except:
                    pass
                try:
                    temp = self.goodreadsParser(xml, '<rating_dist>')
                    if len(temp)>0:
                        dictionary['rating_dist'] = temp
                except:
                    pass

                try:
                    temp = self.goodreadsParser(xml, '<average_rating>')
                    if len(temp)>0:
                        dictionary['avg_rating']=temp
                except:
                    pass
                try:
                    temp = self.goodreadsParser(xml, '<reviews_count type="integer">')
                    if len(temp)>0:
                        dictionary['reviews_count'] = temp
                except:
                    pass
                try:
                    temp = self.goodreadsParser(xml, '<text_reviews_count type="integer">')
                    if len(temp)>0:
                        dictionary['text_reviews_count'] = temp
                except:
                    pass
                try:
                    temp = self.goodreadsParser(xml, '<num_pages>').replace('<![CDATA[', '').replace(
                    ']]>', '')
                    if len(temp)>0:
                        dictionary['num_pages']= temp
                except:
                    pass
                try:
                    temp = self.goodreadsParser(xml, 'shelf name="to-read" count="')
                    if len(temp)>0:
                        dictionary['to-read'] = temp
                except:
                    pass
                try:
                    temp = self.goodreadsParser(xml, 'shelf name="currently-reading" count="')
                    if len(temp)>0:
                        dictionary['currently-reading']=temp
                except:
                    pass

                try:
                    temp = self.goodreadsParser(xml, '<authors>\n<author>\n<id>')
                    if len(temp)>0:
                        dictionary['author_id']=temp
                except:
                    pass

                author_response = urllib2.urlopen(
                    'https://www.goodreads.com/author/show/%s?key=aTGB9VRWJxpCzfqykxUlA' % dictionary['author_id'])
                xml_author = author_response.read()

                try:
                    temp = self.goodreadsParser(xml_author, '<fans_count type="integer">')
                    if len(temp)>0:
                        dictionary['author_fans_count']=temp
                except:
                    pass
            except:
                dictionary['error_code'] = 'data not found'
        except urllib2.HTTPError as err:
                dictionary['error_code'] = err.code

        return dictionary

    def goodreadsParser(self,string, variable):
        try:
            if (variable != 'shelf name="to-read" count="' and variable != 'shelf name="currently-reading" count="' and variable != '<authors>\n<author>\n<id>' and variable != '<fans_count type="integer">'):
                start = string.index(variable) + len(variable)
                last = variable.replace('<', '</').replace(' type="integer"', '')
                end = string.index(last, start)
                return string[start:end]
            else:
                regex = variable + '([0-9]*)'
                return re.findall(regex, string)[0]
        except IndexError:
            return ''

    def cleanhtml(self,raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        cleanr = re.compile('html {(.|\n)*}')
        cleantext=re.sub(cleanr, '', cleantext)
        cleantext=re.sub(re.compile('\n*'), '', cleantext)
        return cleantext

    def __initialize_item_amazon(self):
        item_des=dict()
        item_des['id'] = None
        item_des['ASIN'] = None
        item_des['LowestUsedPrice'] = None
        item_des['LowestNewPrice'] = None
        item_des['SalesRank'] = None
        item_des['Binding'] = None
        item_des['Merchant'] = None
        item_des['Price'] = None
        item_des['Condition'] = None
        item_des['Weight'] = None
        item_des['EditorialReviews'] = None
        item_des['Publisher'] = None
        item_des['Title'] = None
        item_des['Author'] = None
        item_des['PublicationDate'] = None
        item_des['NumberOfPages'] = None
        item_des['ReleaseDate'] = None
        item_des['Digital List Price Scrape'] = None
        item_des['Print List Price Scrape'] = None
        item_des['Kindle Price Scrape'] = None
        item_des['SalesRank Scrape'] = None
        item_des['NumberOfReviews'] = None
        item_des['Rating'] = None
        item_des['EISBN'] = None
        item_des['NumberOfReviews'] = None
        item_des['Rating'] =None
        item_des['PageDescription']=None
        item_des['DescriptionScrape']=None
        item_des['EditorialReviewsScrape']=None
        return item_des

    def __initialize_item_goodreads(self):
        dictionary = dict()
        dictionary['parsed_isbn'] = None
        dictionary['primaryisbn13'] = None

        dictionary['pub_date'] = None
        dictionary['title'] = None
        dictionary['ratings_sum'] = None
        dictionary['ratings_count'] = None
        dictionary['rating_dist'] = None
        dictionary['avg_rating'] = None
        dictionary['reviews_count'] = None
        dictionary['text_reviews_count'] = None
        dictionary['num_pages'] = None
        dictionary['to-read'] = None
        dictionary['currently-reading'] = None
        dictionary['author_id'] = None
        dictionary['author_fans_count'] = None
        dictionary['error_code']=None

        return dictionary



def hello(event, context):

    # user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36")
    #
    # dcap = dict(DesiredCapabilities.PHANTOMJS)
    # dcap["phantomjs.page.settings.userAgent"] = user_agent
    # dcap["phantomjs.page.settings.javascriptEnabled"] = True
    #
    # browser = webdriver.Chrome(service_log_path=os.path.devnull, executable_path="/var/task/chromedriver", service_args=['--ignore-ssl-errors=true'], desired_capabilities=dcap)
    # browser.get('https://en.wikipedia.org/wiki/Special:Random')
    # line = browser.find_element_by_class_name('firstHeading').text
    # print(line)

    #######################
    print "function here"


    region_name= os.environ['region']
    sqs_name= os.environ['sqs']
    sqs_for_scrape = os.environ['sqsattribute']
    sqs_for_review = os.environ['sqsreview']
    sqs_for_daily_scrape = os.environ['sqsdaily']

    sqs = session.resource('sqs', region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName=sqs_name)
    queue_scrape = sqs.get_queue_by_name(QueueName=sqs_for_scrape)
    queue_review = sqs.get_queue_by_name(QueueName=sqs_for_review)
    queue_daily_scrape = sqs.get_queue_by_name(QueueName=sqs_for_daily_scrape)

    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    goodread_table = dynamodb.Table(os.environ['GOODREADS_TABLE'])
    daily_title_list_table = dynamodb.Table(os.environ['AMAZON_DAILY_TITLE_LIST_TABLE'])

    response = queue.receive_messages(VisibilityTimeout=30, MaxNumberOfMessages=10, MessageAttributeNames=['file_name', 'process_date', 'schedule'])
    if len(response)==0:
        print "No Message Processed"
    else:
        api_call=amazon_api()
        api_call.initialize_amazon()
        for queue_item in response:
            print "asin = "+queue_item.body
            write_items= api_call.amazon_product_advertising_api_extract(queue_item.body)
            print write_items
            item_counter=0

            for item in write_items:

                item['process_date'] = queue_item.message_attributes.get('process_date').get('StringValue')
                item['file_name'] = queue_item.message_attributes.get('file_name').get('StringValue')
                item['schedule'] = queue_item.message_attributes.get('schedule').get('StringValue')
                item['id'] = item['ASIN']+'-'+item['process_date']

                # if its daily scrape
                if item['schedule']=='Daily':

                    daily_item={}
                    daily_item['id']= item['id']
                    daily_item['ASIN']= item['ASIN']
                    daily_item['file_name']=item['file_name']
                    daily_item['process_date']=item['process_date']
                    daily_item['EISBN']= item['EISBN']

                    daily_title_list_table.put_item(Item=daily_item)

                else:

                    # if its not daily scrape
                    goodread_flag=False

                    goodread_item = api_call.goodread_data(item['EISBN'])

                    if 'error_code' in goodread_item and goodread_item['error_code']=='data not found':
                        goodread_flag=False
                    else:
                        goodread_flag=True

                    if goodread_flag == False:
                        goodread_item = api_call.goodread_data(item['ASIN'])
                        if 'error_code' in goodread_item and str(goodread_item['error_code'])=='404':
                            goodread_flag=False
                        else:
                            goodread_flag=True

                    if goodread_flag:
                        goodread_item['ASIN']= item['ASIN']
                        goodread_item['id'] = item['EISBN']+'-'+item['process_date']
                        goodread_item['file_name']= item['file_name']
                        goodread_item['process_date'] = item['process_date']


                    queue_scrape.send_message(MessageBody=str(item['ASIN']), MessageAttributes= {
                    'process_date': {
                        'StringValue': str(item['process_date']),
                        'DataType': 'String'
                    },
                    'file_name': {
                        'StringValue': str(item['file_name']),
                        'DataType': 'String'
                    },
                    'EISBN': {
                        'StringValue': str(item['EISBN']),
                        'DataType': 'String'
                    }
                    })


                    queue_review.send_message(MessageBody=str(item['ASIN']), MessageAttributes= {
                    'process_date': {
                        'StringValue': str(item['process_date']),
                        'DataType': 'String'
                    },
                    'file_name': {
                        'StringValue': str(item['file_name']),
                        'DataType': 'String'
                    },
                    'EISBN': {
                        'StringValue': str(item['EISBN']),
                        'DataType': 'String'
                    }
                    })

                    # write items in table

                    table.put_item(Item=item)
                    goodread_table.put_item(Item=goodread_item)




            time.sleep(1)
            if len(write_items)>0:
                queue_item.delete()

    #
    # response = client.invoke(
    #     FunctionName: process.env.daily_queue,
	# 	InvocationType: 'Event',
	# 	LogType: 'None'
    # )
    #
    # print "new lambda executed"
