# -*- coding: utf-8 -*-
import scrapy
import re
import logging

class BiliSpider(scrapy.Spider):
	name = "biliname"
	pattern = re.compile(r"{.*}")
	f = open("top1000.json","r")
	videoInfos = eval(f.read())
	miscount = 0

	def start_requests(self):
		for videoInfo in self.videoInfos:
			url = videoInfo["url"]
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		def extract_with_css(query):
			return response.css(query).extract_first().strip()
		title = response.css("div.v-title h1::text").extract_first()
		if title:
			title = title.strip()
		else:
			title = response.css("head title::text").extract_first().strip()
		tminfo = response.css("div.tminfo > span a::text").extract_first()
		if tminfo:
			tminfo = tminfo.strip()
		else:
			tminfo  = "未知"
		publish_time = response.css("div.tminfo > time > i::text").extract_first()
		if publish_time:
			publish_time = publish_time.strip()
		else:
			publish_time = "未知"
		matchStr = re.search(r"av(?P<aid>\d*)", response.url)
		fanghao = "nil"
		aid = ""
		if not matchStr:
			aid = response.css(".tminfo .v-av-link::text").extract_first()
			if aid:
				aid = re.search(r"\d+", aid).group()
				fanghao = re.search(r"\d+$", aid).group()
		else:
			aid = matchStr.group("aid")
		videoInfo = self.getVideoInfoByAid(aid)
		videoInfo["title"] = title
		videoInfo["tminfo"] = tminfo
		videoInfo["publish_time"] = publish_time
		videoInfo["fanghao"] = fanghao
		# videoInfo["aid"] = aid
		yield videoInfo

	def getVideoInfoByAid(self, aid):
		for videoInfo in self.videoInfos:
			if videoInfo["aid"] == aid:
				return videoInfo
		return {}
