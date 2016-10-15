运行
==========

	scrapy crawl douban -o douban.json

豆瓣有防爬虫的机制，需要以下配置
========

	USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
	DOWNLOAD_DELAY = 2
	COOKIES_ENABLED = False

