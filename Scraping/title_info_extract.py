
from datetime import datetime
import csv
import re
import datetime
import bottlenose
import xml.etree.ElementTree as ET
import time
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import urllib2
from bs4 import BeautifulSoup
import codecs
from BeautifulSoup import BeautifulSoup
import multiprocessing as mp
import boto
from boto.s3.key import Key
import boto3

class title_info_extract:
    def __init__(self):
        # self.__read_file_from_s3()
        # self.__move_from_S3()
        # self.__process_csv()
        self.__process_csv_scrape()


    def __process_csv(self):

        # amazon credentials

        key_access = 'AKIAIO6ZO7NXRZIL2M4A'
        key_secret = '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'
        associate_tag = 'httpwwwopen01 - 20'

        amazon = bottlenose.Amazon(key_access, key_secret, associate_tag, Region='US')

        #check if the file exists or not. If not, then create a new csv file with headers in
        file_path = "data/output/eisbn_amazon_api.csv"
        path_exists = False
        if os.path.isfile(file_path):
            data_existing = self.read_file("data/output/eisbn_amazon_api.csv")
            path_exists = True
            file_target = codecs.open(file_path, "a", encoding='utf-8')
        else:
            data_existing = []
            file_target = codecs.open(file_path, "wb", encoding='utf-8')

        file_writer = csv.writer(file_target)

        write_row = ["'%s'" % 'Process_date',
                    "'%s'" % 'ASIN',
                    "'%s'" % 'LowestUsedPrice',
                    "'%s'" % 'LowestNewPrice',
                    "'%s'" % 'SalesRank',
                    "'%s'" % 'Binding',
                    "'%s'" % 'Merchant',
                    "'%s'" % 'Price',
                    "'%s'" % 'Condition',
                    "'%s'" % 'Weight',
                    "'%s'" % 'EditorialReviews',
                    "'%s'" % 'Publisher',
                    "'%s'" % 'Title',
                    "'%s'" % 'Author',
                    "'%s'" % 'PublicationDate',
                    "'%s'" % 'NumberOfPages',
                    "'%s'" % 'ReleaseDate',
                    "'%s'" % 'EISBN',
                    "'%s'" % 'Parsed_isbn',
                    "'%s'" % 'Primaryisbn13',
                    "'%s'" % 'Pub_date',
                    "'%s'" % 'Title',
                    "'%s'" % 'Ratings_sum',
                    "'%s'" % 'Ratings_count',
                    "'%s'" % 'Rating_dist',
                    "'%s'" % 'Avg_rating',
                    "'%s'" % 'Reviews_count',
                    "'%s'" % 'Text_reviews_count',
                    "'%s'" % 'Num_pages',
                    "'%s'" % 'To-read',
                    "'%s'" % 'Currently-reading',
                    "'%s'" % 'Author_id',
                    "'%s'" % 'Author_fans_count',
                    "'%s'" % 'Error_code',
                    'Line_counter']
        if path_exists == False:
            file_writer.writerow(write_row)

        data = self.read_file("data/source/esibn.csv")

        process_date=str(datetime.datetime.now().date())

        csv_counter = 1
        if len(data_existing) > 1:
            csv_counter = int(data_existing[len(data_existing)-1][len(data_existing[len(data_existing)-1])-1]) + 1

        line_counter = csv_counter
        counter = 0
        for row in data[csv_counter:]:
            self.__process_csv_line_for_api(row, amazon, process_date, line_counter, file_writer, file_target, counter)
            counter += 1
            line_counter += 1

        file_target.close()

    def __process_csv_scrape(self):
        process_date=str(datetime.datetime.now().date())

        file_path = "data/output/amazon_scrape/eisbn_amazon_scrape.csv"
        path_exists = False
        if os.path.isfile(file_path):
            data_existing = self.read_file("data/output/amazon_scrape/eisbn_amazon_scrape.csv")
            path_exists = True
            file_target = codecs.open(file_path, "a", encoding='utf-8')
            #file_target = open(file_path, "a")
        else:
            data_existing = []
            file_target = codecs.open(file_path, "wb", encoding='utf-8')

        file_writer = csv.writer(file_target,quoting = csv.QUOTE_ALL)

        write_row = ['process_date',
                    'ASIN',
                    'Digital List Price Scrape' ,
                    'Print List Price Scrape',
                    'Kindle Price Scrape',
                    'SalesRank Scrape',
                    'NumberOfReviews',
                    'Rating',
                    'DescriptionScrape',
                    'EditorialReviewsScrape',
                    'KindleUnlimited',
                    'Line_counter']
        if path_exists == False:
            file_writer.writerow(write_row)

        data = self.read_file("data/output/eisbn_amazon_api.csv")

        csv_counter = 1
        if len(data_existing) > 1:
            csv_counter = int(data_existing[len(data_existing)-1][len(data_existing[len(data_existing)-1])-1]) + 1


        # load selenium web driver with ip

        options = webdriver.ChromeOptions()
        options.add_argument(
            '--user-agent=Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3')

        # proxy = ip_address+':'+port
        # proxy = '192.116.142.153:8080'
        # webdriver.DesiredCapabilities.CHROME['proxy'] = {
        #     "httpProxy": proxy,
        #     "ftpProxy": proxy,
        #     "sslProxy": proxy,
        #     "noProxy": None,
        #     "proxyType": "MANUAL",
        #     "class": "org.openqa.selenium.Proxy",
        #     "autodetect": False
        # }

        # driver = webdriver.Chrome('/Users/tamalroy/Documents/python_projects/facebook_data/chromedrive/chromedriver')
        driver = webdriver.Chrome('https://s3.amazonaws.com/slstests4/chromedriver')


        line_counter = csv_counter
        counter = 0
        for row in data[csv_counter:]:
            self.__process_csv_line_for_scraping(row,driver,process_date,line_counter,counter,file_writer,file_target)
            counter += 1
            line_counter += 1

        file_target.close()


    def __process_csv_line_for_api(self,row,amazon,process_date,line_counter,file_writer,file_target,counter):
        if len(row) == 0:
            return

        eisbn=row[0]
        result=self.__amazon_n_goodreads_api_call(eisbn, amazon)

        for items in result:
            item_des=items[0]
            goodread_des=items[1]

            write_row = ["'%s'" % process_date,
                         "'%s'" % item_des['ASIN'],
                         "'%s'" % item_des['LowestUsedPrice'],
                         "'%s'" % item_des['LowestNewPrice'],
                         "'%s'" % item_des['SalesRank'],
                         "'%s'" % item_des['Binding'],
                         "'%s'" % item_des['Merchant'],
                         "'%s'" % item_des['Price'],
                         "'%s'" % item_des['Condition'],
                         "'%s'" % item_des['Weight'],
                         "'%s'" % item_des['EditorialReviews'],
                         "'%s'" % item_des['Publisher'],
                         "'%s'" % item_des['Title'],
                         "'%s'" % item_des['Author'],
                         "'%s'" % item_des['PublicationDate'],
                         "'%s'" % item_des['NumberOfPages'],
                         "'%s'" % item_des['ReleaseDate'],
                         "'%s'" % item_des['EISBN'],
                         "'%s'" % goodread_des['parsed_isbn'],
                         "'%s'" % goodread_des['primaryisbn13'],
                         "'%s'" % goodread_des['pub_date'],
                         "'%s'" % goodread_des['title'],
                         "'%s'" % goodread_des['ratings_sum'],
                         "'%s'" % goodread_des['ratings_count'],
                         "'%s'" % goodread_des['rating_dist'],
                         "'%s'" % goodread_des['avg_rating'],
                         "'%s'" % goodread_des['reviews_count'],
                         "'%s'" % goodread_des['text_reviews_count'],
                         "'%s'" % goodread_des['num_pages'],
                         "'%s'" % goodread_des['to-read'],
                         "'%s'" % goodread_des['currently-reading'],
                         "'%s'" % goodread_des['author_id'],
                         "'%s'" % goodread_des['author_fans_count'],
                         "'%s'" % goodread_des['error_code'],
                         line_counter]

            for i in range(0, len(write_row)):

                col = write_row[i]
                if (type(col) is str or type(col) is unicode) and type(col) is not list and type(col) is not tuple:
                    encoded_str = re.sub(r'[^\x00-\x7F]+', '', col)
                    encoded_str = unicode(encoded_str).decode('utf-8').encode('utf-8')
                    write_row[i] = encoded_str

                elif type(col) is list:
                    for j in range(0, len(col)):
                        if type(col[j]) is str and type(col[j]) is not tuple:
                            encoded_lst_str = re.sub(r'[^\x00-\x7F]+', '', col[j]).decode('utf-8').encode('utf-8')
                            col[j] = encoded_lst_str
                    write_row[i] = col

            # print write_row
            file_writer.writerow(write_row)

        print(counter)
        file_target.flush()
        return

    def __process_csv_line_for_scraping(self,row,driver,process_date,line_counter,counter,file_writer,file_target):

        item_des = self.__initialize_item_amazon()

        asin = row[1]
        asin = asin[1:]
        asin = asin[:-1]

        # amazon scrape

        url = '''https://www.amazon.com/dp/%s''' % (asin)
        driver.get(url)

        try:
            price_raw_data = driver.find_element_by_xpath("""//div[@class="a-box-inner a-padding-base"]""").text
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
                item_des['Digital List Price Scrape'] = driver.find_element_by_xpath(
                    """//div[@id="digital-list-price"]/div/span/span[@class="a-text-strike"]""").text[1:]
            except NoSuchElementException:
                None
            try:
                item_des['Print List Price Scrape'] = driver.find_element_by_xpath(
                    """//div[@id="print-list-price"]/div/span/span[@class="a-text-strike"]""").text[1:]
            except NoSuchElementException:
                None
            try:
                item_des['Kindle Price Scrape'] = driver.find_element_by_xpath(
                    """//span[@class="a-size-base mediaTab_subtitle"]""").text[1:]
            except NoSuchElementException:
                None

        try:
            sales_rank_data = driver.find_element_by_id('SalesRank').text
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
        try:
            kindle_unlimited_data = driver.find_element_by_xpath("""//div[@class="a-section a-spacing-small a-spacing-top-micro a-text-left"]/div[@class="a-row"]/span[@class="a-size-base a-color-secondary ku-promo-message"]""").text
            if kindle_unlimited_data is not None:
                if 'Unlimited reading' in kindle_unlimited_data:
                    item_des['KindleUnlimited']="T"

        except NoSuchElementException:
            print "Does not fall under Kindle Unlimited"

        # Rating Scrape


        try:
            review_data = driver.find_element_by_xpath("""//div[@class="a-row a-spacing-extra-large"]""").text
            if review_data is not None:
                review_data = review_data.split('\n')
                temp = re.findall('[-+]?\d*\.\d+|\d+', ''.join(review_data[1].split(',')))
                if len(temp) > 0:
                    item_des['NumberOfReviews'] = temp[0]
                item_des['Rating'] = re.findall('[-+]?\d*\.\d+|\d+', review_data[2])[0]
        except NoSuchElementException:
            print "reviews not found"

        try:
            iframes = driver.find_elements_by_tag_name("iframe")

            result_iframe = []
            for iframe in iframes:
                driver.switch_to_default_content()
                driver.switch_to_frame(iframe)
                output = driver.page_source
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

        # write data from amazon scrape

        write_row = [process_date,
                     asin,
                     item_des['Digital List Price Scrape'],
                     item_des['Print List Price Scrape'],
                     item_des['Kindle Price Scrape'],
                     item_des['SalesRank Scrape'],
                     item_des['NumberOfReviews'],
                     item_des['Rating'],
                     item_des['DescriptionScrape'],
                     item_des['EditorialReviewsScrape'],
                     item_des['KindleUnlimited'],
                     line_counter]

        for i in range(0, len(write_row)):

            col = write_row[i]
            if (type(col) is str or type(col) is unicode) and type(col) is not list and type(col) is not tuple:
                encoded_str = re.sub(r'[^\x00-\x7F]+', '', col)
                encoded_str = unicode(encoded_str).decode('utf-8').encode('utf-8')
                write_row[i] = encoded_str

            elif type(col) is list:
                for j in range(0, len(col)):
                    if type(col[j]) is str and type(col[j]) is not tuple:
                        encoded_lst_str = re.sub(r'[^\x00-\x7F]+', '', col[j]).decode('utf-8').encode('utf-8')
                        col[j] = encoded_lst_str

                write_row[i] = col

        file_writer.writerow(write_row)
        print(counter)
        file_target.flush()



    def __amazon_n_goodreads_api_call(self,eisbn,amazon):

        result=[]

        amazon_info = self.__get_response_from_product_advertising_api(eisbn, amazon)
        time.sleep(1)
        if amazon_info is not None:
            for item_des in amazon_info:
                goodread_des = self.__goodread_data(item_des['EISBN'])
                result.append((item_des,goodread_des))

        return result



    def read_file(self, file):
        with open(file, 'r') as f:
            data = [row for row in csv.reader(f.read().splitlines())]
        return data

    def __get_response_from_product_advertising_api(self, itemid, amazon):


        # BrowseNodes,EditorialReview,Similarities,ItemAttributes
        xml_response = amazon.ItemLookup(ItemId=itemid, IdType='ISBN', SearchIndex='Books',
                                         ResponseGroup='Offers,OfferFull,SalesRank,ItemAttributes')
        # xml_response = amazon.ItemLookup(ItemId=itemid, ResponseGroup='BrowseNodes,EditorialReview,Similarities,ItemAttributes')
        root = ET.fromstring(xml_response)

        for items in root:
            if items.tag.split('}')[1] == 'Items':
                items_list = []
                for item in items:
                    if item.tag.split('}')[1] == 'Item':
                        item_des = self.__initialize_item_amazon()



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


    def __scrape_amazon(self, asin, item_des):
        driver = webdriver.Chrome('/Users/tamalroy/Documents/python_projects/facebook_data/chromedrive/chromedriver')

        counter = 0

        url = '''https://www.amazon.com/dp/%s'''%(asin)
        driver.get(url)


        try:
            price_raw_data=driver.find_element_by_xpath("""//div[@class="a-box-inner a-padding-base"]""").text
            if price_raw_data is not None:
                price_raw_data=price_raw_data.split('\n')
                for data_point in price_raw_data:
                    if len(re.findall('Digital List Price', data_point)) > 0:
                        item_des['Digital List Price Scrape'] = re.findall('[-+]?\d*\.\d+|\d+', data_point)[0]
                    if len(re.findall('Print List Price', data_point)) > 0:
                        item_des['Print List Price Scrape'] = re.findall('[-+]?\d*\.\d+|\d+', data_point)[0]
                    if len(re.findall('Kindle Price', data_point)) > 0:
                        item_des['Kindle Price Scrape'] = re.findall('[-+]?\d*\.\d+|\d+', data_point)[0]
        except NoSuchElementException:

            try:
                item_des['Digital List Price Scrape'] = driver.find_element_by_xpath("""//div[@id="digital-list-price"]/div/span/span[@class="a-text-strike"]""").text[1:]
            except NoSuchElementException:
                None
            try:
                item_des['Print List Price Scrape'] = driver.find_element_by_xpath("""//div[@id="print-list-price"]/div/span/span[@class="a-text-strike"]""").text[1:]
            except NoSuchElementException:
                None
            try:
                item_des['Kindle Price Scrape'] = driver.find_element_by_xpath("""//span[@class="a-size-base mediaTab_subtitle"]""").text[1:]
            except NoSuchElementException:
                None






        try:
            sales_rank_data=driver.find_element_by_id('SalesRank').text
            if sales_rank_data is not None:
                sales_rank_data=sales_rank_data.split('\n')
                item_des['SalesRank Scrape']=[]
                for data_point in sales_rank_data:
                    if ' in ' in data_point:
                        data_point=data_point.split(' in ')
                        temp=re.findall('[-+]?\d*\,\d+|\d+', data_point[0])
                        if len(temp)>0:
                            rank=int(''.join(temp[0].split(',')))
                            item_des['SalesRank Scrape'].append((data_point[1],rank))


        except NoSuchElementException:
            print "sales rank not found"

        # Rating Scrape


        try:
            review_data = driver.find_element_by_xpath("""//div[@class="a-row a-spacing-extra-large"]""").text
            if review_data is not None:
                review_data = review_data.split('\n')
                temp = re.findall('[-+]?\d*\.\d+|\d+', ''.join(review_data[1].split(',')))
                if len(temp) > 0:
                    item_des['NumberOfReviews'] = temp[0]
                item_des['Rating'] = re.findall('[-+]?\d*\.\d+|\d+', review_data[2])[0]
        except NoSuchElementException:
            print "reviews not found"






        try:
            iframes = driver.find_elements_by_tag_name("iframe")

            result_iframe = []
            for iframe in iframes:
                driver.switch_to_default_content()
                driver.switch_to_frame(iframe)
                output = driver.page_source
                result_iframe.append(output)

            description = [x for x in result_iframe if "productDescriptionSource" in x]
            description = [x for x in description if "Editorial Reviews" not in x][0].encode("utf-8")
            # Parse Description

            soup=BeautifulSoup(description)

            description=soup.find('div',{'id':'iframeContent'}).text

            editorial_reviews=None

            try:
                editorial_reviews = [x for x in result_iframe if "Editorial Reviews" in x][0].encode("utf-8")
                soup = BeautifulSoup(editorial_reviews)


                editorial_reviews=soup.find('div',{'class':'productDescriptionWrapper'}).text
            except:
                editorial_reviews = ''

            item_des['DescriptionScrape'] = description
            item_des['EditorialReviewsScrape']=editorial_reviews

        except:
            "description not found"

        return item_des







    def __goodread_data(self, eisbn):
        ID=eisbn
        dictionary = self.__initialize_item_goodreads()
        try:
            response = urllib2.urlopen('https://www.goodreads.com/book/isbn/%s?key=aTGB9VRWJxpCzfqykxUlA' % ID)
            xml = response.read()

            try:
                dictionary['parsed_isbn'] = ID
                dictionary['primaryisbn13'] = self.goodreadsParser(xml, '<isbn13>').replace('<![CDATA[', '').replace(']]>', '')


                dictionary['pub_date'] = self.goodreadsParser(xml, '<publication_year>') + '-' + self.goodreadsParser(xml,'<publication_month>')+ '-' + self.goodreadsParser(xml, '<publication_day>')
                dictionary['title'] = self.goodreadsParser(xml, '<title>').replace('<![CDATA[', '').replace(']]>', '')
                dictionary['ratings_sum'] = self.goodreadsParser(xml, '<ratings_sum type="integer">')
                dictionary['ratings_count'] = self.goodreadsParser(xml, '<ratings_count type="integer">')
                dictionary['rating_dist'] = self.goodreadsParser(xml, '<rating_dist>')
                dictionary['avg_rating'] = self.goodreadsParser(xml, '<average_rating>')
                dictionary['reviews_count'] = self.goodreadsParser(xml, '<reviews_count type="integer">')
                dictionary['text_reviews_count'] = self.goodreadsParser(xml, '<text_reviews_count type="integer">')
                dictionary['num_pages'] = self.goodreadsParser(xml, '<num_pages>').replace('<![CDATA[', '').replace(']]>', '')
                dictionary['to-read'] = self.goodreadsParser(xml, 'shelf name="to-read" count="')
                dictionary['currently-reading'] = self.goodreadsParser(xml, 'shelf name="currently-reading" count="')
                dictionary['author_id'] = self.goodreadsParser(xml, '<authors>\n<author>\n<id>')
                author_response = urllib2.urlopen('https://www.goodreads.com/author/show/%s?key=aTGB9VRWJxpCzfqykxUlA' % dictionary['author_id'])
                xml_author = author_response.read()
                dictionary['author_fans_count'] = self.goodreadsParser(xml_author, '<fans_count type="integer">')
            except:
                dictionary['error_code']='data not found'
        except urllib2.HTTPError as err:
            if err.code == 404:
                dictionary['error_code']=err.code
            else:
                dictionary['error_code'] =err.code
        return dictionary



    def __get_book_info_from_keywords(self):
        key_access = 'AKIAIO6ZO7NXRZIL2M4A'
        key_secret = '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'
        associate_tag = 'httpwwwopen01 - 20'

        amazon = bottlenose.Amazon(key_access, key_secret, associate_tag, Region='US')

        xml_response = amazon.ItemSearch(Keywords="miracle of dunkirk", SearchIndex="KindleStore",
                                         ResponseGroup='ItemAttributes')

        root = ET.fromstring(xml_response)


        for items in root:
            if items.tag.split('}')[1] == 'Items':
                items_list = []
                for item in items:
                    if item.tag.split('}')[1] == 'Item':
                        item_des = self.__initialize_item_amazon()



                        for attr in item:
                            if attr.tag.split('}')[1] == 'ASIN':
                                item_des[attr.tag.split('}')[1]] = attr.text

                            if attr.tag.split('}')[1] == 'ItemAttributes':
                                for itemAttributes in attr:
                                    if itemAttributes.tag.split('}')[-1] == 'Binding':
                                        item_des['Binding'] = itemAttributes.text
                                    if itemAttributes.tag.split('}')[-1] == 'Publisher':
                                        item_des['Publisher'] = itemAttributes.text
                                    if itemAttributes.tag.split('}')[-1] == 'Title':
                                        item_des['Publisher'] = itemAttributes.text
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

                            if attr.tag.split('}')[1] == 'Offers':
                                for offers in attr:
                                    if offers.tag.split('}')[-1] == 'Offer':
                                        for offer in offers:
                                            if offer.tag.split('}')[-1] == 'Merchant':
                                                for merchant in offer:
                                                    if merchant.tag.split('}')[-1] == 'Name':
                                                        if merchant.text == u'Amazon.com':
                                                            item_des['Merchant'] = 'Amazon.com'
                                                        else:
                                                            item_des['Merchant'] = 'other'

                                            if offer.tag.split('}')[-1] == 'OfferAttributes':
                                                for offerAttributes in offer:
                                                    if offerAttributes.tag.split('}')[-1] == 'Condition':
                                                        item_des['Condition'] = offerAttributes.text

                                            if offer.tag.split('}')[-1] == 'OfferListing':
                                                for offerListing in offer:
                                                    if offerListing.tag.split('}')[-1] == 'Price':
                                                        for price in offerListing:
                                                            if price.tag.split('}')[-1] == 'Amount':
                                                                item_des['Price'] = price.text

                                                    if offerListing.tag.split('}')[-1] == 'IsEligibleForPrime':
                                                        item_des['Prime_eligible'] = offerListing.text




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


    def __move_from_S3(self):
        # S3 connection
        access_key_id = "AKIAJYWCN7X4U6DYFWAA"
        access_key = "BPGc2daOQ9vDc87FpRvXQU3t7q/PbXLeSmRMk/v7"
        bucket_name = "slstests3"
        folder = "uploads"
        key = boto.connect_s3(access_key_id, access_key)
        bucket = key.get_bucket(bucket_name, validate=False)

        k = Key(bucket)
        k.key = folder + '/eisbn.csv'
        for fliename in bucket.list():
            k.key = fliename.name
            k.get_contents_to_filename("data/source/eisbn1.csv")

    def __read_file_from_s3(self):
        access_key_id = "AKIAJYWCN7X4U6DYFWAA"
        access_key = "BPGc2daOQ9vDc87FpRvXQU3t7q/PbXLeSmRMk/v7"

        session = boto3.Session(access_key_id, access_key)

        BUCKET = "slstests4"
        KEY = "esibn.csv"

        client =session.client('s3')


        result = client.get_object(Bucket=BUCKET, Key=KEY)

        # Read the object (not compressed):
        text = result["Body"].read().decode()
        print text



        ######

        isbn_list = text.split('\n')

        sqs = session.resource('sqs', region_name='us-east-1')
        queue = sqs.get_queue_by_name(QueueName='test')

        i = 0


        for i in range(1,len(isbn_list)):

            print len(isbn_list[i])

            queue.send_message(MessageBody=isbn_list[i]
                               # , MessageAttributes={
                    # 'Isbn': {
                    #     'StringValue': isbn_list[i],
                    #     'DataType': 'String'
                    # }
                # }
            )



        #response = queue.send_message(Entries=message_list)

        print "success"



        #####
        # Get the service resource


        sqs = session.resource('sqs', region_name='us-east-1')


        # create queue
        # queue = sqs.create_queue(QueueName='test')
        # Get the queue
        queue = sqs.get_queue_by_name(QueueName='dev-aws-python-messages')

        x=queue.receive_messages()





        data='Asdfasdfa'

        print (queue.url)

        print (queue.attributes.get('DelaySeconds'))

        # Create a new message
        # response = queue.send_message(MessageBody='world')

        # The response is NOT a resource, but gives you a message ID and MD5

        # print(response.get('MessageId'))
        # print(response.get('MD5OfMessageBody'))


        # Creating message with custom attributes
        # queue.send_message(MessageBody='boto3', MessageAttributes={
        #     'Author': {
        #         'StringValue': 'Daniel',
        #         'DataType': 'String'
        #     }
        # })
        #
        # queue.send_message(MessageBody='boto31', MessageAttributes={
        #     'Author': {
        #         'StringValue': 'Danielsdaf',
        #         'DataType': 'String'
        #     }
        # })


        messages = set()
        for i in range(0, 6):
            msg_list = queue.receive_messages(VisibilityTimeout=1, MaxNumberOfMessages=10, WaitTimeSeconds=5)
            for msg in msg_list:
                messages.add(msg.body)

        print list(messages)


        for i in range(500):
            messages = []
            for j in range(10):
                n = str(i * 10 + j)
                messages.append({
                    "Id": n,
                    "MessageBody": "Message %s" % n
                })
            queue.send_messages(Entries=messages)

        # Messages can be sent in batches

        # response = queue.send_messages(Entries=[
        #     {
        #         'Id': '1',
        #         'MessageBody': 'world'
        #     },
        #     {
        #         'Id': '2',
        #         'MessageBody': 'boto3',
        #         'MessageAttributes': {
        #             'Author': {
        #                 'StringValue': 'Daniel',
        #                 'DataType': 'String'
        #             }
        #         }
        #     },
        #     {
        #         'Id': '3',
        #         'MessageBody': 'boto31',
        #         'MessageAttributes': {
        #             'Author': {
        #                 'StringValue': 'Daniels',
        #                 'DataType': 'String'
        #             }
        #         }
        #     }
        # ])

        # Print out any failures
        # print(response.get('Failed'))

        # Process messages by printing out body and optional author name
        for message in queue.receive_messages(MessageAttributeNames=['Author']):
            # Get the custom author message attribute if it was set
            author_text = ''
            if message.message_attributes is not None:
                author_name = message.message_attributes.get('Author').get('StringValue')
                if author_name:
                    author_text = ' ({0})'.format(author_name)

            # Print out the body and author (if set)
            print('Hello, {0}!{1}'.format(message.body, author_text))

            # Let the queue know that the message is processed
            message.delete()



        # response = queue.send_message(
        #     MessageBody=data
        # )
        #
        # # The response is NOT a resource, but gives you a message ID and MD5
        # print(response.get('MessageId'))
        # print(response.get('MD5OfMessageBody'))
        #
        # messages = queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=10)
        # for message in messages:
        #     print message
