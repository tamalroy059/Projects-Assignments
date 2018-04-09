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
import random
import re

class title_review_extract:
    def __init__(self, driver, asin):
        self.__process_csv_line_for_scraping(driver, asin)
        # self.critical_reviews=self.__extract_critical_review(driver,asin)
        self.ret_num=11

    def __extract_critical_review(self, driver, asin):
        # load selenium web driver with ip
        url = 'http://www.amazon.com/reviews/%s/ref=cm_cr_arp_d_viewopt_fmt?formatType=current_format&&filterByStar=critical' % asin
        driver.get(url)

        try:
            pages = driver.find_element_by_xpath("""//*[@id="cm_cr-pagination_bar"]""").text.split('\n')
            max_pages = pages[len(pages) - 2]
            max_pages = int(max_pages)
            pages_to_scrape = min(max_pages, 5)
            print pages
        except:
            pages_to_scrape = 1

        ##extract critical reviews

        final_reviews=[]

        for p in range(1, pages_to_scrape + 1):
            reviews = driver.find_elements_by_css_selector('span.a-size-base.review-text')

            if len(reviews) < 1:
                each_review = ''
                final_reviews.append(each_review)
            elif len(reviews) < 2:
                each_review = driver.find_element_by_css_selector('span.a-size-base.review-text').text
                final_reviews.append(each_review)
            else:
                for rev in reviews:
                    each_review = rev.text
                    final_reviews.append(each_review)
            time.sleep(random.randint(1, 1))


            url = 'http://www.amazon.com/reviews/%s/ref=cm_cr_arp_d_viewopt_fmt?formatType=current_format&&filterByStar=critical&&pageNumber=%s' % (asin, p)
            driver.get(url)
        print "here reviews"
        print final_reviews
        return final_reviews

    ######
    def __process_csv_line_for_scraping(self,driver, asin):
        print "asin = "+asin
        # item_des = self.__initialize_item_amazon()
        item_des=dict()

        # amazon scrape

        url = '''https://www.amazon.com/dp/%s''' % (asin)
        driver.get(url)

        try:
            print "price raw data"
            extract_path = driver.find_element_by_xpath("""//div[@class="a-box-inner a-padding-base"]""")

            if extract_path is not None:
                price_raw_data = extract_path.text
                print price_raw_data
                if price_raw_data is not None:
                    price_raw_data = price_raw_data.split('\n')
                    for data_point in price_raw_data:
                        if len(re.findall('Digital List Price', data_point)) > 0:
                            item_des['Digital List Price Scrape'] = re.findall('[-+]?\d*\.\d+|\d+', data_point)[0]
                        if len(re.findall('Print List Price', data_point)) > 0:
                            item_des['Print List Price Scrape'] = re.findall('[-+]?\d*\.\d+|\d+', data_point)[0]
                        if len(re.findall('Kindle Price', data_point)) > 0:
                            item_des['Kindle Price Scrape'] = re.findall('[-+]?\d*\.\d+|\d+', data_point)[0]
        except NoSuchElementException:

            try:
                extract_path=driver.find_element_by_xpath("""//div[@id="digital-list-price"]/div/span/span[@class="a-text-strike"]""")
                if extract_path is not None:
                    digital_list_price=extract_path.text
                    # print "digital list price"
                    # print digital_list_price
                    item_des['Digital List Price Scrape'] = driver.find_element_by_xpath(
                        """//div[@id="digital-list-price"]/div/span/span[@class="a-text-strike"]""").text[1:]
            except NoSuchElementException:
                None
            try:
                extract_path = driver.find_element_by_xpath("""//div[@id="print-list-price"]/div/span/span[@class="a-text-strike"]""")
                if extract_path is not None:
                    print_list_price = extract_path.text
                    # print "print list price"
                    # print print_list_price
                    item_des['Print List Price Scrape'] = driver.find_element_by_xpath(
                        """//div[@id="print-list-price"]/div/span/span[@class="a-text-strike"]""").text[1:]
            except NoSuchElementException:
                None
            try:
                extract_path = driver.find_element_by_xpath("""//span[@class="a-size-base mediaTab_subtitle"]""")
                if extract_path is not None:
                    kindle_price = extract_path.text
                    # print "kindle price"
                    # print kindle_price
                    item_des['Kindle Price Scrape'] = driver.find_element_by_xpath("""//span[@class="a-size-base mediaTab_subtitle"]""").text[1:]
            except NoSuchElementException:
                None

        try:
            extract_path = driver.find_element_by_id('SalesRank')
            if extract_path is not None:
                sales_rank_data = extract_path.text
                # print "sales_rank_data"
                # print sales_rank_data
                if sales_rank_data is not None:
                    sales_rank_data = sales_rank_data.split('\n')
                    item_des['SalesRank Scrape'] = []
                    for data_point in sales_rank_data:
                        if ' in ' in data_point:
                            data_point = data_point.split(' in ')
                            temp = re.findall('[-+]?\d*\,\d+|\d+', data_point[0])
                            if len(temp) > 0:
                                rank = int(''.join(temp[0].split(',')))
                                item_des['SalesRank Scrape'].append((data_point[1], rank))


        except NoSuchElementException:
            print "sales rank not found"



        #kindle unlimited
        # try:
        #     print "kindle unlimited data"
        #     kindle_unlimited_data = driver.find_element_by_xpath("""//div[@class="a-section a-spacing-small a-spacing-top-micro a-text-left"]/div[@class="a-row"]/span[@class="a-size-base a-color-secondary ku-promo-message"]""").text
        #     print kindle_unlimited_data
        #
        #     if kindle_unlimited_data is not None:
        #         if 'Unlimited reading' in kindle_unlimited_data:
        #             item_des['KindleUnlimited']="T"
        #
        # except NoSuchElementException:
        #     print "Does not fall under Kindle Unlimited"

        # Rating Scrape

        try:
            extract_path = driver.find_element_by_xpath("""//div[@class="a-row a-spacing-extra-large"]""")
            if extract_path is not None:
                review_data = extract_path.text
                # print "review data"
                # print review_data

                if review_data is not None:
                    review_data = review_data.split('\n')
                    temp = re.findall('[-+]?\d*\.\d+|\d+', ''.join(review_data[1].split(',')))
                    if len(temp) > 0:
                        item_des['NumberOfReviews'] = temp[0]
                    item_des['Rating'] = re.findall('[-+]?\d*\.\d+|\d+', review_data[2])[0]
        except NoSuchElementException:
            print "reviews not found"

        try:
            description_scrape=[]
            editorial_reviews_scrape=[]
            iframes = driver.find_elements_by_tag_name("iframe")
            result_iframe = []
            print "iframes here"
            print len(result_iframe)
            for iframe in iframes:
                driver.switch_to_default_content()
                driver.switch_to_frame(iframe)
                output = driver.page_source
                # print output
                # soup = BeautifulSoup(output)
                # extract_text = soup.find('div', {'id': 'iframeContent'})
                # if extract_text is not None:
                #     description_scrape.append(extract_text.text.encode("utf-8"))
                # extract_text=soup.find('div', {'class': 'productDescriptionWrapper'})
                # if extract_text is not None:
                #     editorial_reviews_scrape.append(extract_text.text.encode("utf-8"))
                # print "Output IFrame"
                # print description_scrape
                # print editorial_reviews_scrape
                result_iframe.append(output)

            description = [x for x in result_iframe if "productDescriptionSource" in x]
            description = [x for x in description if "Editorial Reviews" not in x][0].encode("utf-8")


            # Parse Description

            soup = BeautifulSoup(description)


            description = soup.find('div', {'id': 'iframeContent'}).text



            editorial_reviews = None

            try:
                editorial_reviews = [x for x in result_iframe if "Editorial Reviews" in x][0].encode("utf-8")
                soup = BeautifulSoup(editorial_reviews)

                editorial_reviews = soup.find('div', {'class': 'productDescriptionWrapper'}).text
            except:
                editorial_reviews = ''

            item_des['DescriptionScrape'] = description.replace('"', '\'')
            item_des['EditorialReviewsScrape'] = editorial_reviews.replace('"', '\'')

        except:
            "description not found"
        print "final item object"
        print item_des
        return item_des
    ######


    def __initialize_item_amazon(self):
        item_des=dict()
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
        item_des['EISBN'] = None
        item_des['NumberOfReviews'] = None
        item_des['Rating'] =None
        item_des['DescriptionScrape']=None
        item_des['EditorialReviewsScrape']=None
        item_des['Review_count']=None
        item_des['KindleUnlimited']=None
        return item_des

    def get_reviews(self):
        return self.ret_num



access_key_id = "AKIAJYWCN7X4U6DYFWAA"
access_key = "BPGc2daOQ9vDc87FpRvXQU3t7q/PbXLeSmRMk/v7"
session = boto3.Session(access_key_id, access_key)

def scrape_amazon(event, context):
    user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36")

    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = user_agent
    dcap["phantomjs.page.settings.javascriptEnabled"] = True

    # browser = webdriver.PhantomJS(service_log_path=os.path.devnull, executable_path="/var/task/phantomjs", service_args=['--ignore-ssl-errors=true'], desired_capabilities=dcap)
    browser = webdriver.PhantomJS(service_log_path=os.path.devnull, executable_path="/var/task/phantomjs")


    region_name= os.environ['region']
    sqs_name= os.environ['sqsattribute']

    # print "sqs name = "+sqs_name
    # print "dynamo db = " + os.environ['DYNAMODB_TABLE']

    sqs = session.resource('sqs', region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName=sqs_name)


    # asin='B0078X73NO'
    # url = 'http://www.amazon.com/reviews/%s/ref=cm_cr_arp_d_viewopt_fmt?formatType=current_format&&filterByStar=critical' % asin
    # browser.get(url)
    # pages = browser.find_element_by_xpath("""//*[@id="cm_cr-pagination_bar"]""").text.split('\n')
    # print "scraped part"
    # print pages

    response = queue.receive_messages(VisibilityTimeout=30)
    if len(response)==0:
        print "No Message Processed"
    else:
        for item in response:
            title_review_extract(browser,"B005T54IAY")
            item.delete()
        print "success"
