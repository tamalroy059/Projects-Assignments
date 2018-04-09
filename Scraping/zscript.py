#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 13:43:20 2018
@author: zhengdaosong
"""



import requests
from bs4 import BeautifulSoup
import ast
import json
import datetime
import time
import pandas as pd
import random
from random import choice
import os
from boto.s3.key import Key
import boto3
import boto
import xml.etree.ElementTree as ET





root_file="/home/ec2-user/python_projects/scraper_z/scraper_z/"
# root_file="/Users/tamalroy/Documents/python_projects/scraper_z/"

chromedriver_type='chromedriver_linux'




user_agent_dict=dict()
user_agent_dict_fail=dict()

class zscript:

    access_key_id = "AKIAJYWCN7X4U6DYFWAA"
    access_key = "BPGc2daOQ9vDc87FpRvXQU3t7q/PbXLeSmRMk/v7"
    bucket_name = "slstests4"
    key = boto.connect_s3(access_key_id, access_key)
    bucket = key.get_bucket(bucket_name, validate=False)
    k = Key(bucket)


    def __init__(self):
        self._useragent=self.__desktop_agent()
        xml_agent=self.parse_user_agent_xml_file("user_agent_file/useragentswitcher.xml")
        self._useragent = self._useragent+xml_agent


    def __desktop_agent(self):

        desktop_agents = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0',
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Googlebot/2.1 (+http://www.googlebot.com/bot.html)',
            'Googlebot/2.1 (+http://www.google.com/bot.html)',
            'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
            'Mozilla/5.0 (compatible; bingbot/2.0 +http://www.bing.com/bingbot.htm)']

        desktop_agents = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/28.0.1469.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/28.0.1469.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:35.0) Gecko/20100101 Firefox/35.0",
            "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Maxthon 2.0)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML like Gecko) Maxthon/4.0.0.2000 Chrome/22.0.1229.79 Safari/537.1",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.7.62 Version/11.01",
            "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
            "Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.16",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.12 Safari/537.36 OPR/14.0.1116.4",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.29 Safari/537.36 OPR/15.0.1147.24 (Edition Next)",
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36 OPR/18.0.1284.49",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36 OPR/19.0.1326.56",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36 OPR/20.0.1387.91",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
            "Mozilla/5.0 (Windows; U; Windows NT 6.2; es-US ) AppleWebKit/540.0 (KHTML like Gecko) Version/6.0 Safari/8900.00",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.71 (KHTML like Gecko) WebVideo/1.0.1.10 Version/7.0 Safari/537.71"
        ]



        return desktop_agents

    def parse_user_agent_xml_file(self,input_file_path):
        user_agent_list = []

        tree = ET.parse(input_file_path)
        root = tree.getroot()
        for child in root:
            for child_1 in child:
                if child_1.tag == 'useragent':
                    user_agent_list.append(child_1.attrib)
        return user_agent_list


    def run_scrape(self, asin_list):
        asin_scraped=[]
        scraped=0
        asin_not_scraped=[]
        notscraped=0
        timestamp = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")
        result = []
        for index, row in enumerate(asin_list):
            # for index, row in asins_rescrape.iterrows():
            # print index, row
            if index >= 0:
                asin = row[0]

                # while datetime.datetime.now() < datetime.datetime(2018, 3, 9, 6, 0, 0, 395484):
                temp = {}

                user_agent=random_headers(self._useragent)['User-Agent']



                headers = {
                    'Host': 'www.amazon.com',
                    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Referer': 'https://www.amazon.com/gp/aw/s/ref=is_s?k=%s' % asin,
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Connection': 'keep-alive',
                }

                if type(user_agent) is dict:
                    for key in user_agent:
                        if key=='useragent':
                            headers['User-Agent']=user_agent[key]
                        headers[key]= user_agent[key]
                    user_agent=user_agent['useragent']
                else:
                    headers['User-Agent']=user_agent




                if index % 50 == 0:
                    cookies = refresh_cookie()
                    proxy_check = False
                    while proxy_check == False:
                        try:
                            rand_proxy = random.choice(curr_proxy_list)
                            ip = requests.get("http://ls"
                                              "icanhazip.com/", proxies={"http": rand_proxy}, timeout=5).text
                            # latency = requests.get("http://icanhazip.com/", proxies={"http": rand_proxy}, timeout=5).elapsed.total_seconds()
                            if ip == requests.get("http://icanhazip.com/").text:
                                # if latency > 1:
                                proxy_check = False
                            else:
                                proxy_check = True
                        except:
                            curr_proxy_list.remove(rand_proxy)
                else:
                    cookies = cookies
                    rand_proxy = rand_proxy

                try:
                    response = requests.get('https://www.amazon.com/dp/%s' % asin, headers=headers, cookies=cookies, timeout=20,
                                            proxies={"http": rand_proxy})
                except:
                    cookies = refresh_cookie()
                    proxy_check = False
                    while proxy_check == False:
                        try:
                            rand_proxy = random.choice(curr_proxy_list)
                            ip = requests.get("http://icanhazip.com/", proxies={"http": rand_proxy}, timeout=5).text
                            # ip = requests.get("https://www.openroademdia.com", proxies={"http": rand_proxy}, timeout=(5)).text
                            # proxy_check = True
                            # latency = requests.get("http://icanhazip.com/", proxies={"http": rand_proxy}, timeout=5).elapsed.total_seconds()
                            if ip == requests.get("http://icanhazip.com/").text:
                                # if latency > 1:
                                proxy_check = False
                            else:
                                proxy_check = True
                        except:
                            curr_proxy_list.remove(rand_proxy)
                    response = requests.post('https://www.amazon.com/dp/%s' % asin, headers=headers, cookies=cookies,
                                             timeout=20, proxies={"http": rand_proxy})
                # response = requests.post('https://www.amazon.com/gp/search-inside/service-data', headers=headers, cookies=cookies, data=data)
                # response = req
                data = response.content
                filepath=root_file+"data/Results_Old_ASIN_Dog_Check_After_Migration/amazon_page_%s_%s.txt" % (asin, timestamp)
                with open(filepath,"w") as text_file:
                    text_file.write(data)
                file_size=os.path.getsize(filepath)
                #check if we received valid page based on size
                if file_size>6000:
                    self.k.key = 'ScrapedPages/%s/' %(row[2]) + "amazon_page_%s_%s.txt" % (asin, row[2])
                    self.k.set_contents_from_filename(filename=filepath, num_cb=20)
                    asin_scraped.append(row)

                    scraped+=1
                    if user_agent in user_agent_dict.keys():
                        user_agent_dict[user_agent]+=1
                    else:
                        user_agent_dict[user_agent]= 1
                else:
                    asin_not_scraped.append(row)
                    notscraped+=1

                    if user_agent in user_agent_dict_fail.keys():
                        user_agent_dict_fail[user_agent]+=1
                        # if user_agent_dict_fail[user_agent]>5:
                        #     desktop_agents.remove(user_agent)
                    else:
                        user_agent_dict_fail[user_agent]= 1


                os.remove(filepath)

        print "scraped  --- "+str(scraped)
        print "not scraped --- "+str(notscraped)
        # print "success"
        # print user_agent_dict
        # print "falied"
        # print user_agent_dict_fail

        return (asin_scraped, asin_not_scraped)

        # time.sleep(1)
    def rescrape(self):
        import os

        asins_rescrape = []
        for root, dirs, files in os.walk("Need-Rescrape"):
            for filename in files:
                filename = filename.replace("amazon_page_", "")
                filename = filename.replace("_20180323.txt", "")
                asins_rescrape.append(filename)

        asins_rescrape = pd.DataFrame(asins_rescrape)
        asins_rescrape.columns = ['asin']




def random_headers(desktop_agents):

    agent=choice(desktop_agents)
    return {'User-Agent': agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


# Set up refresh cookie function
def refresh_cookie():
    import pickle
    from selenium import webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    # chrome_options.add_argument('no-sandbox')
    # driver = webdriver.Chrome("/home/zhengdao/cronjob/sailthru/ebb_list_data_email/chromedriver", chrome_options=chrome_options)
    driver = webdriver.Chrome(root_file+"chromedrive/%s/chromedriver"%(chromedriver_type),
                              chrome_options=chrome_options)
    driver.get("https://amazon.com")
    cookie = driver.get_cookies()
    # pickle.dump( driver.get_cookies() , open("cookies2.pkl","wb"))
    # cookies = pickle.load(open("cookies.pkl", "rb"))
    driver.close()

    cookies = {}
    for item in cookie:
        name = item['name']
        cookies[name] = item['value']
    return cookies


# Download proxies
def refresh_proxy():
    curr_proxy_list = []
    content = requests.get('http://free-proxy-list.net').content
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("table", attrs={"id": "proxylisttable"})

    # The first tr contains the field names.
    headings = [th.get_text() for th in table.find("tr").find_all("th")]

    datasets = []
    for row in table.find_all("tr")[1:]:
        dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
        datasets.append(dataset)

    for dataset in datasets:
        # Check Field[0] for tags and field[1] for values!
        proxy = "http://"
        for field in dataset:
            if field[0] == 'IP Address':
                proxy = proxy + field[1] + ':'
            elif field[0] == 'Port':
                proxy = proxy + field[1]
        curr_proxy_list.append(proxy.__str__())
    return curr_proxy_list


curr_proxy_list = refresh_proxy()




