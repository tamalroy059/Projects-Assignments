import requests
import boto3
import ip_scrape

access_key_id = "AKIAJYWCN7X4U6DYFWAA"
access_key = "BPGc2daOQ9vDc87FpRvXQU3t7q/PbXLeSmRMk/v7"
session = boto3.Session(access_key_id, access_key)


request_line="http://list.didsoft.com/get?email=bhaley@openroadmedia.com&pass=uk4s8u&pid=httppremium"
result = requests.get(request_line).content
result_list = result.split('\n')

proxies =[]

file = open("ip_list.txt", "w")


for item in result_list:
    if '#' in item:
        item_des = item.split('#')
        ip = item_des[0]
        area = item[1]
        proxies.append(ip)
        file.write(str(ip)+'\n')

file.close()


# ip_object = ip_scrape.ip_scrape()
#
# proxies = ip_object.ip_scraping()



# -*- coding: utf-8 -*-

# Scrapy settings for amz_bot project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'amz_bot'

SPIDER_MODULES = ['amz_bot.spiders']
NEWSPIDER_MODULE = 'amz_bot.spiders'

# print proxies

ROTATING_PROXY_LIST = proxies





# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'amz_bot (+http://www.yourdomain.com)'
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'



# Retry many times since proxies often fail
# RETRY_TIMES = 2

# Retry on most error codes since proxies fail for different reasons
# RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]


# Obey robots.txt rules
ROBOTSTXT_OBEY = False



DNS_TIMEOUT=20

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 30
# CONCURRENT_REQUESTS_PER_IP = 2

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'amz_bot.middlewares.AmzBotSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'amz_bot.middlewares.MyCustomDownloaderMiddleware': 543,
#}

DOWNLOADER_MIDDLEWARES = {
    # ...
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
    'amz_bot.rotate_useragent.RotateUserAgentMiddleware' :400,
    # ...
}

ROTATING_PROXY_CLOSE_SPIDER = True

ROTATING_PROXY_PAGE_RETRY_TIMES = 2

ROTATING_PROXY_BACKOFF_BASE = 30




# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'amz_bot.pipelines.AmzBotPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

