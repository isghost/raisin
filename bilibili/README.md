运行
==========

	scrapy crawl bili -o biliinfo.csv

说明
===================
bilibili没有反爬虫机制，不影响网站运行和抓取时间，将时间间隔设置为`0.1`，抓取时间大概为`15个小时`，请
求数为`369018`。数据丢失数量`30`个，原因不明。    
数量有几十万行，采用csv格式，便于`excel`后期处理

配置
========

	DOWNLOAD_DELAY = 0.1

数据下载地址(https://github.com/isghost/raisin/releases)
=================

进一步处理
=======
从获取到的信息里面，筛选出播放数量排名前1000的数据`TOP1000.csv`，转为json`top1000.json`，根据url获取
更加详细的信息。

	scrapy crawl biliname -o top1000info.csv
