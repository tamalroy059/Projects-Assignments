

from selenium import webdriver
import datetime
import urllib2
import socket



class ip_scrape:

    def ip_scraping(self):

        ip_list=[]

        options = webdriver.ChromeOptions()
        options.add_argument(
            '--user-agent=Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3')


        current_time = datetime.datetime.now()

        driver = webdriver.Chrome(
            '/Users/tamalroy/Documents/python_projects/amazon_product_advertising/chromedrive/chromedriver',
            chrome_options=options)
        driver.get("https://free-proxy-list.net/")

        for i in range(15):

            if i>0:
                driver.find_element_by_xpath("""//li[@id="proxylisttable_next"]//a""").click()

            ip_lists = driver.find_elements_by_xpath("""//div[@class="table-responsive"]//table//tbody/tr""")

            for ip in ip_lists:
                temp = ip.text.split(' ')

                ip_list.append(str(temp[0])+':'+str(temp[1]))
                # ip_desc = dict()
                #
                # ip_desc['ip_address'] = temp[0]
                # ip_desc['port'] = temp[1]

        driver.close()
        valid_proxy=self.__check_ip_lists(proxyList=ip_list)


        return valid_proxy


    ## Bad Proxy
    def is_bad_proxy(self,pip):
        try:
            proxy_handler = urllib2.ProxyHandler({'http': pip})
            opener = urllib2.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib2.install_opener(opener)
            req = urllib2.Request('https://www.google.com/')  # change the URL to test here
            sock = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print 'Error code: ', e.code
            return e.code
        except Exception, detail:
            print "ERROR:", detail
            return True
        return False

    def __check_ip_lists(self, proxyList):
        socket.setdefaulttimeout(120)

        # two sample proxy IPs
        # proxyList = ['125.76.226.9:80', '213.55.87.162:6588']

        for currentProxy in proxyList:
            if self.is_bad_proxy(currentProxy):
                proxyList.remove(currentProxy)

        return proxyList