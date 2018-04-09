
import re
import time
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import boto3
import psycopg2
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import ProxyType
import random
from selenium.webdriver.support.ui import WebDriverWait




class amazon_title_extract:


    def __init__(self):
        self._driver = self.__initialize_web_driver()

        access_key_id = "AKIAJYWCN7X4U6DYFWAA"
        access_key = "BPGc2daOQ9vDc87FpRvXQU3t7q/PbXLeSmRMk/v7"

        self._session = boto3.Session(access_key_id, access_key)


    def __phantomjs_web_driver(self):
        user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36")

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = user_agent
        dcap["phantomjs.page.settings.javascriptEnabled"] = True

        headers = {'Accept': '*/*',
                   'Accept-Encoding': 'gzip,deflate,sdch',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Cache-Control': 'max-age=0'}

        for key, value in enumerate(headers):
            webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value

        service_args = ['--proxy-type=http', '--ignore-ssl-errors=true']

        driver = webdriver.PhantomJS(service_log_path=os.path.devnull,
                                     executable_path="/home/ec2-user/python_projects/title_selection/title_selection/chromedrive/phantomjs",
                                     service_args=service_args, desired_capabilities=dcap)

        return driver


    def __chrome_driver(self):

        options = webdriver.ChromeOptions()

        user_agent = self.__random_user_agent()
        options.add_argument(
            '--user-agent=%s'%(user_agent))

        options.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})

        # options.add_argument("headless")

        # chrome_path='/home/ec2-user/python_projects/title_selection/title_selection/chromedrive/chromedriver'
        chrome_path = '/Users/tamalroy/Documents/python_projects/title_selection/chromedrive/chromedriver'

        driver = webdriver.Chrome(chrome_path, chrome_options=options)

        driver.set_page_load_timeout(20)

        # clear_cache(driver)

        return driver


    def __initialize_web_driver(self):

        return self.__phantomjs_web_driver()

    def quitDriver(self):
        self._driver.quit()






    def extract_title_info(self, asin):

        driver=self._driver


        # item_des = self.__initialize_item_amazon()
        item_des = dict()

        # amazon scrape
        item_des['ASIN']=asin
        page_source=None

        url = '''file:///home/ec2-user/python_projects/scrapy_project/scrapy_project/amz_bot/scraped/%s.html''' % (asin)
        try:
            driver.get(url)

            print url

            try:
                extract_path = driver.find_element_by_xpath("""//div[@class="a-box-inner a-padding-base"]""")

                if extract_path is not None:
                    price_raw_data = extract_path.text
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
                    extract_path = driver.find_element_by_xpath(
                        """//div[@id="digital-list-price"]/div/span/span[@class="a-text-strike"]""")
                    if extract_path is not None:
                        digital_list_price = extract_path.text
                        # print "digital list price"
                        # print digital_list_price
                        item_des['Digital List Price Scrape'] = driver.find_element_by_xpath(
                            """//div[@id="digital-list-price"]/div/span/span[@class="a-text-strike"]""").text[1:]
                except NoSuchElementException:
                    pass

                try:
                    extract_path = driver.find_element_by_xpath(
                        """//div[@id="print-list-price"]/div/span/span[@class="a-text-strike"]""")
                    if extract_path is not None:
                        print_list_price = extract_path.text
                        # print "print list price"
                        # print print_list_price
                        item_des['Print List Price Scrape'] = driver.find_element_by_xpath(
                            """//div[@id="print-list-price"]/div/span/span[@class="a-text-strike"]""").text[1:]
                except NoSuchElementException:
                    pass

                try:
                    extract_path = driver.find_element_by_xpath("""//span[@class="a-size-base mediaTab_subtitle"]""")
                    if extract_path is not None:
                        kindle_price = extract_path.text
                        # print "kindle price"
                        # print kindle_price
                        item_des['Kindle Price Scrape'] = driver.find_element_by_xpath(
                            """//span[@class="a-size-base mediaTab_subtitle"]""").text[1:]
                except NoSuchElementException:
                    pass

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
                                    item_des['SalesRank Scrape'].append((str(data_point[1]), str(rank)))

                item_des['SalesRank Scrape'] = str(item_des['SalesRank Scrape'])


            except NoSuchElementException:
                pass

            # kindle unlimited
            try:
                extract_text = driver.find_element_by_xpath("""//div[@class="a-section a-spacing-small a-spacing-top-micro a-text-left"]/div[@class="a-row"]/span[@class="a-size-base a-color-secondary ku-promo-message"]""")
                kindle_unlimited_data = extract_text.text

                if kindle_unlimited_data is not None:
                    if 'Unlimited reading' in kindle_unlimited_data:
                        item_des['KindleUnlimited']="True"

            except NoSuchElementException:
                item_des['KindleUnlimited'] = "False"

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
                pass

            try:
                description_scrape = []
                editorial_reviews_scrape = []
                iframes = driver.find_elements_by_tag_name("iframe")
                result_iframe = []

                for iframe in iframes:
                    driver.switch_to_default_content()
                    driver.switch_to_frame(iframe)
                    output = driver.page_source
                    soup = BeautifulSoup(output, "lxml")
                    extract_text = soup.find('div', {'id': 'iframeContent'})
                    if extract_text is not None:
                        description_scrape.append(extract_text.text.encode("utf-8").replace('"', '\''))
                    extract_text=soup.find('div', {'class': 'productDescriptionWrapper'})
                    if extract_text is not None:
                        editorial_reviews_scrape.append(extract_text.text.encode("utf-8").replace('"', '\''))
                if len(description_scrape)>0:
                    item_des['DescriptionScrape'] = description_scrape

                if len(editorial_reviews_scrape)>0:
                    item_des['EditorialReviewsScrape'] = editorial_reviews_scrape

            except:
                pass

            if len(item_des.keys())>2:
                item_des['Notes']=None
            else:
                item_des['Notes'] = "Not Available in Amazon"

        except TimeoutException as ex:
            print("Exception has been thrown. " + str(ex))

        return item_des

    ######


    def __initialize_item_amazon(self):
        item_des = dict()
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
        item_des['Rating'] = None
        item_des['DescriptionScrape'] = None
        item_des['EditorialReviewsScrape'] = None
        item_des['KindleUnlimited'] = None
        return item_des



    def connect_to_reshift(self):

        # Set up variables for Redshift API
        dbname = "sailthrudata"
        host = "sailthru-data.cmpnfzedptft.us-east-1.redshift.amazonaws.com"
        user = "datateam"
        password = "datateamMaiden180"

        conn_string = "dbname=%s port='5439' user=%s password=%s host=%s" % (dbname, user, password, host)
        print "Connecting to database\n        ->%s" % (conn_string)
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()

        return (conn, cur)

    def close_redshift(self,conn):
        conn.close()

    def insert_to_redshift(self,conn, cur, value,table_name):

        value_string  = ','.join('\''+str(e).replace('\'','\"')+'\'' for e in value)

        sql_string = '''
        INSERT INTO %s (asin,rating,digital_list_price,print_list_price,
        kindle_price, editorial_reviews, description, review_count, salesrank, kindle_unlimited)
        VALUES (%s);
        '''%(table_name, value_string)
        cur.execute(sql_string)

        conn.commit()

    def insert_to_redshift_reviews(self, conn, cur, values, table_name="amazon_review_scrape"):
        convert_list=[]

        for value in values:
            convert_list.append('(' + '\'' +value['asin'] + '\'' + ',' + '\'' + value['review'].replace('\'','\"') + '\'' + ')')

        value_string = ','.join(e for e in convert_list)

        sql_string = '''
                INSERT INTO %s (asin, review)
                VALUES %s;
                ''' % (table_name, value_string)

        print sql_string
        cur.execute(sql_string)
        conn.commit()


    def get_items_from_sqs(self):
        sqs_name='dev-aws-python-amazon-scrape'
        sqs = self._session.resource('sqs', region_name='us-east-1')
        queue = sqs.get_queue_by_name(QueueName=sqs_name)

        response = queue.receive_messages(VisibilityTimeout=30, MaxNumberOfMessages=10,
                                          MessageAttributeNames=['file_name', 'process_date', 'EISBN'])

        for queue_item in response:
            print queue_item.body
            print queue_item.message_attributes.get('EISBN').get('StringValue')
            queue_item.delete()


    def __random_user_agent(self):
        user_agent_list = [ \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        return random.choice(user_agent_list)



def get_clear_browsing_button(driver):
    """Find the "CLEAR BROWSING BUTTON" on the Chrome settings page."""
    return driver.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')

def clear_cache(driver, timeout=60):
    """Clear the cookies and cache for the ChromeDriver instance."""
    # navigate to the settings page
    driver.get('chrome://settings/clearBrowserData')

    # wait for the button to appear
    wait = WebDriverWait(driver, timeout)
    wait.until(get_clear_browsing_button)

    # click the button to clear the cache
    get_clear_browsing_button(driver).click()

    # wait for the button to be gone before returning
    wait.until_not(get_clear_browsing_button)
















