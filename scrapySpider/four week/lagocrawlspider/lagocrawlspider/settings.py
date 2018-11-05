# -*- coding: utf-8 -*-

# Scrapy settings for lagocrawlspider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'lagocrawlspider'

SPIDER_MODULES = ['lagocrawlspider.spiders']
NEWSPIDER_MODULE = 'lagocrawlspider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'lagocrawlspider (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 20
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False
# COOKIES_ENABLED = True    #Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1523631857,1523671777,1523765874,1523781660; _ga=GA1.2.551491057.1523631858; user_trace_token=20180413230417-f016f5ad-3f2b-11e8-b82e-5254005c3644; LGUID=20180413230417-f016f8ed-3f2b-11e8-b82e-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; _gid=GA1.2.1802172387.1523631862; ab_test_random_num=0; LG_LOGIN_USER_ID=5e1a3dc835dc9aeebfa19d8c6a47992a19c3c6895cdbb58c044838e20b2f8fad; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=1c5e90f5510c52b142bb4a28a86d1a4a45c323a1e59962027c6e1e8db8e2dec8; SEARCH_ID=94383baf19a14ea495ceeebbd2093e97; JSESSIONID=ABAAABAAAIAACBI20C14993F6C4A337EEDFC399232A170F; LGRID=20180415174658-f0bea4d5-4091-11e8-862c-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1523785619; _putrc=370D01BAEF24F673123F89F2B170EADC; login=true; unick=llf; TG-TRACK-CODE=search_code; LGSID=20180415174437-9cc26a0f-4091-11e8-b88d-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; gate_login_token=""; X_HTTP_TOKEN=f663b3fd12d4b0168889a05546a0928b; _gat=1

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'lagocrawlspider.middlewares.LagocrawlspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'lagocrawlspider.middlewares.LagocrawlspiderDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'lagocrawlspider.pipelines.LagocrawlspiderPipeline': 300,
   'lagocrawlspider.pipelines.MysqlTwistedPipline': 1,

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
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
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
MYSQL_HOST = "localhost"
MYSQL_DBNAME = "articlespider"   #数据库名
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"

SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SQL_DATE_FORMAT = "%Y-%m-%d"

