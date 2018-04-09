from bs4 import BeautifulSoup
import re
import pandas as pd
from boto.s3.key import Key
import boto3
import boto
import os



root_file="/home/ec2-user/python_projects/scraper_z/scraper_z/"


class amazon_parser:

    def __init__(self):
        self._daily_table=self.__initialize_dynamodb()


    def __initialize_dynamodb(self):
        access_key_id = "AKIAJYWCN7X4U6DYFWAA"
        access_key = "BPGc2daOQ9vDc87FpRvXQU3t7q/PbXLeSmRMk/v7"
        session = boto3.Session(access_key_id, access_key)
        sqs = session.resource('sqs', region_name='us-east-1')
        dynamodb = session.resource('dynamodb', region_name='us-east-1')
        amazon_title_scrape_table = dynamodb.Table('amazon-daily-title-scrape-result')
        return amazon_title_scrape_table

    def move_from_s3_to_local(self,process_date,filename):
        try:
            # s3 credentials
            access_key_id = "AKIAJYWCN7X4U6DYFWAA"
            access_key = "BPGc2daOQ9vDc87FpRvXQU3t7q/PbXLeSmRMk/v7"
            bucket_name = "slstests4"
            key = boto.connect_s3(access_key_id, access_key)
            bucket = key.get_bucket(bucket_name, validate=False)
            k = Key(bucket,"ScrapedPages/%s/%s"%(process_date,filename))
            k.get_contents_to_filename(root_file+"data/output/%s"%filename)
            return root_file+"data/output/%s"%filename
        except:
            return None

    def parser(self, filename, asin):
        temp=dict()
        with open(filename, 'r') as file:
            data = file.read().replace('\n', '')
            soup = BeautifulSoup(data, 'html.parser')
            try:
                title_author = soup.title.string.replace(' - Amazon.com', '')
            except:
                title_author = None
            try:
                avg_rating = get_rating(soup.find(attrs={"data-hook": "average-star-rating"}))
            except:
                avg_rating = None
            try:
                reviews = get_review(soup.find(attrs={"id": "dp-summary-see-all-reviews"}))
            except:
                reviews = None
            try:
                ranks = get_ranks(soup.find(attrs={"id": "SalesRank"}))
            except:
                ranks = None
            try:
                sims = get_sim(soup.find("div", {"id": "purchase-sims-feature"}))
            except:
                sims = None
            temp['title_author'] = title_author
            temp['avg_rating'] = avg_rating
            temp['reviews'] = reviews
            temp['ranks'] = ranks
            temp['sims'] = sims
            temp['asin'] = asin[0]
            temp['process_date'] =asin[1]
            temp['eisbn'] = asin[2]
            temp['id'] = asin[0]+'_' + asin[1]
        try:
            self._daily_table.put_item(Item=temp)
        except:
            print "error in loading to database"

        os.remove(filename)






def get_rating(soup):
    variable = ' out of'
    #string = soup.find(attrs={"data-hook":"average-star-rating"}).contents[0].string
    string = soup.contents[0].string
    end = string.index(variable)
    return string[0:end]


def get_review(soup):
    variable = ' customer reviews'
    #string = soup.find(attrs={"data-hook":"average-star-rating"}).contents[0].string
    string = soup.contents[0].string
    end = string.index(variable)
    return string[8:end]

def get_ranks(soup):
    ranks = soup
    ranks = ranks.get_text().encode('ascii','ignore')
    ranks = re.sub("[\(\[].*?[\)\]]", "", ranks)
    ranks = re.sub("[\{\[].*?[\}\]]", "", ranks)
    ranks = ranks.replace(".zg_hrsr .zg_hrsr_item .zg_hrsr_rank ", "")
    return ranks


def get_sim(soup):
    sim = soup
    sim = str(sim.contents[1])
    start = sim.index('id_list')
    end = sim.index('url')
    sim = sim[start+9:end]
    return sim


