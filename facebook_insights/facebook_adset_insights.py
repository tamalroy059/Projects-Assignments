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

class facebook_adset_insights:

    def __init__(self):
        print "hello"
        self.directory = '/home/zhengdao/cronjob/facebook_insights/facebook_insights/facebook_data/facebook_adset_insights'
        self.directory_creatives ='/home/zhengdao/cronjob/facebook_insights/facebook_insights/facebook_data/facebook_creatives'
        self.__facebook_insight_data()
        self.__webhook()


    def __facebook_insight_data(self,date_to=None):

        conn,cursor=self.__connect_to_redshift()

        sql_string='''
        select max(date_start)
        from facebook_adset_insights
        '''

        cursor.execute(sql_string)
        result =cursor.fetchall()

        date_from=result[0][0]

        # date_from='2018-02-21'

        if date_from is not None:
            date_from=datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
            date_from=date_from - datetime.timedelta(days=1)
        date_to = datetime.datetime.now().date()
        #date_to = '2017-12-11'


        ad_data_target = ['adset_id','spend','unique_clicks', 'clicks','reach', 'impressions','date_start','date_stop']
        if date_from is None:
            ad_data_target_file_name = "adset_insights_update_"+str(date_to) + '.csv'
        else:
            ad_data_target_file_name = "adset_insights_" + str(date_from)+ '_' + str(date_to) + '.csv'
        f_ad_data_target = open("/home/zhengdao/cronjob/facebook_insights/facebook_insights/facebook_data/Insights/" + ad_data_target_file_name, "wb")
        c_ad_data_target = csv.writer(f_ad_data_target)
        c_ad_data_target.writerow(ad_data_target)

        access_token='EAAXLzipZCp7oBAC7bSixOBdmkbHDZBRxwuxULwlaZCrRHl9Auj60Haf8JPFHiAPBSH5TKSq9xfPGXApqyXcdeJw6ep34NZCs9QRFmURE23jIs7UMVzhIpPm0dPnSfiqe6LjlN2WTPTVEXZBhgl2TDpYaEX8w1xBtXkprs2Swerw0wKEE0ZBsl0jE5WFVkhjzYZD'
        access_token='EAAXLzipZCp7oBAK5rsXN8sZAwWMktuIpR59oYgvhzAIHHvjyZBg2kZAb8KZCQztQMZBg2ohtWixPTQiAEbDzDZBqfmaVu8mWLvJQhGCB3VeCfLD4BJZBEufUCVVLMgeYf0IM0uaPzsNGs70NAP86WLrf7dSdHG06PRIZD'

        if date_from is None:
            request_line = 'https://graph.facebook.com/v2.12/act_10153207729011812?access_token=%s&pretty=0&fields=adsets{insights.time_increment(1).date_preset(lifetime){spend,unique_clicks,clicks,impressions,reach,relevance_score,adset_id}}&limit=100'%(access_token)
        else:

            request_line = 'https://graph.facebook.com/v2.12/act_10153207729011812?access_token=%s&pretty=0&fields=adsets{insights.time_increment(1).time_range({"since":"%s","until":"%s"}){spend,unique_clicks,clicks,impressions,reach,relevance_score,adset_id}}&limit=100'%(access_token,str(date_from),str(date_to))



        result = requests.get(request_line).content
        result = json.loads(result, encoding='utf8')

        while 'error' in result and 'code' in result['error']:
            time.sleep(120)
            result = requests.get(request_line).content
            result = json.loads(result, encoding='UTF-8')


        if 'data' not in result['adsets']:
            print result

        for row in result['adsets']['data']:
            if 'insights' in row.keys():
                for row_r in row['insights']['data']:
                    ad_insights=self.__ad_insights()
                    ad_insights['adset_id'] = row_r['adset_id']
                    ad_insights['spend'] = row_r['spend']
                    ad_insights['unique_clicks'] = row_r['clicks']
                    ad_insights['clicks'] = row_r['unique_clicks']
                    ad_insights['reach'] = row_r['reach']
                    ad_insights['impressions'] = row_r['impressions']
                    ad_insights['date_start'] = row_r['date_start']
                    ad_insights['date_stop'] = row_r['date_stop']

                    write_list = [ad_insights['adset_id'],ad_insights['spend'],ad_insights['unique_clicks'], ad_insights['clicks'],
                                  ad_insights['reach'], ad_insights['impressions'],
                                  ad_insights['date_start'],ad_insights['date_stop']]
                    c_ad_data_target.writerow(write_list)



        loop = False

        if 'next' in result['adsets']['paging']:
            loop = True
            request_line = result['adsets']['paging']['next']
            result = requests.get(request_line).content
            result = json.loads(result, encoding='UTF-8')

        counter=0
        error_loop=0

        while loop:
            print counter
            counter+=1
            loop=False
            while 'error' in result and 'code' in result['error'] and error_loop!=5:
                error_loop+=1
                time.sleep(120)
                print 'sleeping'
                result = requests.get(request_line).content
                result = json.loads(result, encoding='UTF-8')

                if error_loop==5:
                    print result
                    break


            error_loop=0
            for row in result['data']:
                if 'insights' in row.keys():
                    for row_r in row['insights']['data']:
                        ad_insights = self.__ad_insights()
                        ad_insights['adset_id'] = row_r['adset_id']
                        ad_insights['spend'] = row_r['spend']
                        ad_insights['unique_clicks'] = row_r['unique_clicks']
                        ad_insights['clicks'] = row_r['clicks']
                        ad_insights['reach'] = row_r['reach']
                        ad_insights['impressions'] = row_r['impressions']
                        ad_insights['date_start'] = row_r['date_start']
                        ad_insights['date_stop'] = row_r['date_stop']

                        write_list = [ad_insights['adset_id'], ad_insights['spend'], ad_insights['unique_clicks'],
                                      ad_insights['clicks'],
                                      ad_insights['reach'], ad_insights['impressions'],
                                      ad_insights['date_start'], ad_insights['date_stop']]
                        c_ad_data_target.writerow(write_list)


            if 'paging' in result and 'next' in result['paging']:
                loop = True
                request_line = result['paging']['next']
                result = requests.get(request_line).content
                result = json.loads(result, encoding='UTF-8')

        f_ad_data_target.close()



        self.__move_to_s3(self.directory,[ad_data_target_file_name])





        table_name = 'facebook_adset_insights'

        s3_directory = self.directory + '/' + ad_data_target_file_name


        sql_string='''
        delete
        from facebook_adset_insights
        where date_start>='%s'
        '''%(date_from)

        cursor.execute(sql_string)


        sql_string = '''
                        copy %s
                                                FROM 's3://sailthru-data/%s'
                                                        CREDENTIALS 'aws_iam_role=arn:aws:iam::822605674378:role/DataPipelineRole'
                                                        DELIMITER ','
                                                        IGNOREHEADER 1
                                                        TIMEFORMAT 'YYYY/MM/DD HH24:MI:SS'
                                                        EMPTYASNULL QUOTE '"'
                                                        CSV REGION 'us-east-1'
                                                        ;
                        ''' % (table_name, s3_directory)

        cursor.execute(sql_string)

        conn.commit()
        conn.close()


        #### Remove the file
        os.remove(os.getcwd() + "/facebook_data/Insights/" + ad_data_target_file_name)







    def __move_to_s3(self, directory ,file_names):
        # S3 connection
        access_key_id = "AKIAJYWCN7X4U6DYFWAA"
        access_key = "BPGc2daOQ9vDc87FpRvXQU3t7q/PbXLeSmRMk/v7"
        bucket_name = "sailthru-data"

        key = boto.connect_s3(access_key_id, access_key)
        bucket = key.get_bucket(bucket_name, validate=False)

        k = Key(bucket)
        k.key = directory+'/' + file_names[0]
        k.set_contents_from_filename(
            os.getcwd()+"/facebook_data/Insights/"+file_names[0], num_cb=20)



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




    def __ad_insights(self):
        ad_insights=dict()
        ad_insights['adset_id']=None
        ad_insights['spend']=None
        ad_insights['unique_clicks']=None
        ad_insights['reach'] = None
        ad_insights['relevance_score']=None
        ad_insights['relevance_positive_feedback']=None
        ad_insights['relevance_negative_feedback'] = None
        ad_insights['status']=None
        ad_insights['data_start']=None
        ad_insights['date_stop']=None
        return ad_insights

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

    def __webhook(self):
        curl_string = '''
        curl -H "Content-Type: application/json" -X POST -d '{"orion_secret":"E97fTyw8Lr+4N667+KB/S46eag4QypdKuF9ieXlWUshyk5tbkCufRGPKPSz3rqUHgMCV8WKqUVOTyhqz53XbkXIEeaGNMia8gjivdR4JQrztdYa06DimJNHDsg92G7tmE0aHKr50PmHme87NuIXWn0JkzLiHVNOtuW7KMcIt2r0EsQfAFzn+AdEomAlcuG1fY18BS8R0UkwKpkTaVgkbFSh8/Jz/c7HdREGBbzEhx1tlQC6ZxydMncW0sksmCWYvDh0HD76oujeo/9QZgbW68fdSMdddW6Spi7lxc4ef0uwPqpK/FoqHaxGraCOiNKxCD9cvTuDrbQsk1Yz0I5n6ig=="}' https://tasks.openroadmedia.com/daily-adset-data-ingest
        '''
        os.system(curl_string)


