import scrapy
import sys
reload(sys)
sys.setdefaultencoding('gbk')
class DoubanSpider(scrapy.Spider):
	name = "douban"
	start_urls = ['http://www.dbmeinv.com/dbgroup/show.htm?pager_offset=1']
	pageNum = 0
	def parse(self, response):
		self.pageNum = self.pageNum + 1
		# follow links to author pages
		# print(response.css('a::attr(href)').extract())
		for href in response.css('div.thumbnail div.img_single a::attr(href)').extract():
			yield scrapy.Request(response.urljoin(href),callback=self.parse_author)
		# follow pagination links
		next_page = response.css('li.next a::attr(href)').extract_first()
		if self.pageNum > 300:
			return 
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)

	def parse_author(self, response):
		def extract_with_css(query):
			return response.css(query).extract_first().strip()
		imgUrl = response.css("div.topic-figure img::attr(src)").extract()
		imgUrl = [response.urljoin(url) for url in imgUrl]
		yield {
		'name': extract_with_css('div.media-body h1::text'),
		'publish_time': extract_with_css('div.info abbr::attr(title)'),
		'author': extract_with_css('div.info a::attr(data-name)'),
		'imgUrl': imgUrl,
		}