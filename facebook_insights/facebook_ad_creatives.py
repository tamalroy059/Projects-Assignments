import json
import requests
import simplejson as json
from datetime import datetime
import csv
from boto.s3.key import Key
import boto
import psycopg2
import os
import httplib
import urlparse
import time
import datetime
import boto3


class facebook_ad_creatives:
    def __init__(self):
        self.directory_creatives = 'facebook_data/facebook_creatives'

        access_key_id = "AKIAJYWCN7X4U6DYFWAA"
        access_key = "BPGc2daOQ9vDc87FpRvXQU3t7q/PbXLeSmRMk/v7"
        self._session = boto3.Session(access_key_id, access_key)
        self._process_date = str(datetime.datetime.now())[:19]
        self.__facebook_ad_creatives()


    def __facebook_ad_creatives(self):
        conn, cursor = self.__connect_to_redshift()


        sql_string = '''
                        select max(updated_time)
                        from facebook_ad_creatives;
                        '''

        cursor.execute(sql_string)
        result = cursor.fetchall()

        date_from = result[0][0]

        if date_from is not None:
            epoch = int(time.mktime(time.strptime(date_from[:-5], "%Y-%m-%dT%H:%M:%S")))
            date_from = datetime.datetime.strptime(date_from[:-5], "%Y-%m-%dT%H:%M:%S")

        date_to = datetime.datetime.now()

        ad_data_target = ['ad_id', 'asin', 'tag', 'url', 'created_time', 'updated_time']

        if date_from is None:
            ad_data_target_file_name = "ad_creatives_start_to" + str(date_to) + '.csv'
        else:
            ad_data_target_file_name = "ad_creatives_" + str(datetime.datetime.now())[:10] +'.csv'

        # ad_data_target_file_name = "ad_url" + '.csv'
        f_ad_data_target =open("facebook_data/Ad_creatives/" + ad_data_target_file_name, "wb")
        c_ad_data_target = csv.writer(f_ad_data_target)
        c_ad_data_target.writerow(ad_data_target)

        if date_from is None:
            request_line = 'https://graph.facebook.com/v2.11/act_10153207729011812/ads?access_token=EAAPgFcUCNeUBAFRFlApnBetFL5yyAeEui1NL38pGdwRHMuTV4D0JlO6L0wEqfsEgy762lgZBhONF1ugdVQZA4YxIVP5dOESQmIZC99hLkgsZBfCSFXRIjZBOYOmuncaRbp2x6UI0QMByEyYKjElzIBMbW05hok24ZD&pretty=0&fields=created_time,updated_time,adcreatives{object_story_spec}&limit=100'
        else:
            request_line = 'https://graph.facebook.com/v2.11/act_10153207729011812/ads?access_token=EAAPgFcUCNeUBAFRFlApnBetFL5yyAeEui1NL38pGdwRHMuTV4D0JlO6L0wEqfsEgy762lgZBhONF1ugdVQZA4YxIVP5dOESQmIZC99hLkgsZBfCSFXRIjZBOYOmuncaRbp2x6UI0QMByEyYKjElzIBMbW05hok24ZD&pretty=0&fields=created_time,updated_time,adcreatives{object_story_spec}&filtering=[{"field":"ad.created_time","operator":"GREATER_THAN","value":"%s"}]&limit=100' % (
            epoch)



        # result = requests.get(request_line).content
        # result = json.loads(result, encoding='utf8')

        sqs_queue = self.__initialize_queue()

        sqs_queue.send_message(MessageBody=request_line, MessageAttributes={
            'process_date': {
                'StringValue': self._process_date,
                'DataType': 'String'
            },
            'data_source': {
                'StringValue': 'facebook ad creatives',
                'DataType': 'String'
            },
            'data_type': {
                'StringValue': 'url',
                'DataType': 'String'
            }
        })





    def __initialize_queue(self):

        queue_name='facebook_api'

        sqs = self._session.resource('sqs', region_name='us-east-1')
        facebook_queue = sqs.get_queue_by_name(QueueName=queue_name)

        return facebook_queue






    def __connect_to_redshift(self):
        access_key_id = "AKIAJYWCN7X4U6DYFWAA"
        access_key = "BPGc2daOQ9vDc87FpRvXQU3t7q/PbXLeSmRMk/v7"
        bucket_name = "sailthru-data"
        folder = "facebook_marketing_data"
        k = boto.connect_s3(access_key_id, access_key)
        bucket = k.get_bucket(bucket_name, validate=False)

        # Set up variables for Redshift API
        dbname = "sailthrudata"
        host = "sailthru-data.cmpnfzedptft.us-east-1.redshift.amazonaws.com"
        user = "datateam"
        password = "datateamMaiden180"

        # Connect to RedShift
        conn_string = "dbname=%s port='5439' user=%s password=%s host=%s" % (dbname, user, password, host)
        print "Connecting to database\n        ->%s" % (conn_string)
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

        return (conn, cursor)

    def __ad_creatives(self):
        ad_creatives=dict()
        ad_creatives['adset_id']=None
        ad_creatives['name']=None
        ad_creatives['link']=None
        ad_creatives['asin']=None
        ad_creatives['tag']=None
        ad_creatives['created_time']=None
        ad_creatives['updated_time']=None
        return ad_creatives

    def __unshorten_url(self,url):
        parsed = urlparse.urlparse(url)
        h = httplib.HTTPConnection(parsed.netloc)
        h.request('HEAD', parsed.path)
        response = h.getresponse()
        if response.status / 100 == 3 and response.getheader('Location'):
            return response.getheader('Location')
        else:
            return url