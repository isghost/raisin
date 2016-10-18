# -*- coding: utf-8 -*-
import scrapy
import re
import logging

class BiliSpider(scrapy.Spider):
	name = "bili"
	baseUrl = 'http://api.bilibili.com/archive_stat/stat'
	index = 6107145
	endIndex = 6476162
	pattern = re.compile(r"{.*}")

	def start_requests(self):
		
		for i in range(self.index,self.endIndex + 1):
			if i%30 == 0:
				logging.info("current av id = " + str(i))
			url = self.baseUrl + "?callback=jQuery123&aid=" + str(i) + "&type=jsonp&_=1476622123693"
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		result = response.body.decode(response.encoding)
		jsonStr = re.search(self.pattern,result).group()
		videoInfo = eval(jsonStr)
		if videoInfo["code"] != 0:
			return 
		aid = re.search(r"aid=(?P<aid>\d*)",response.url).group("aid") 
		data = videoInfo["data"]
		data["url"] = "http://www.bilibili.com/video/av" + str(aid)
		data["aid"] = aid
		yield data
