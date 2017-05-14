# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import io  
import sys
import codecs
import time

browser = webdriver.Chrome()

# browser.get('https://s.taobao.com/search?q=%E8%A1%A3%E6%9C%8D&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170513')
baseUrl = "https://s.taobao.com/search?ie=utf8&initiative_id=staobaoz_20170513&stats_click=search_radio_all%3A1&js=1&imgfile=&q=%E8%A1%A3%E6%9C%8D+%E7%94%B7+%E7%9F%AD%E8%A2%96&suggest=0_3&_input_charset=utf-8&wq=%E8%A1%A3%E6%9C%8D+%E7%94%B7&suggest_query=%E8%A1%A3%E6%9C%8D+%E7%94%B7&source=sugges&fs=1"
browser.get(baseUrl)

urls = []
def collectUrl(elems):
	try:
		for elem in elems:
			url = elem.find_element_by_css_selector("div.row.row-2.title > a").get_attribute("href")
			urls.append(url)
	except Exception,e:
		print e
	# print url.encode('gb18030')
count = 0
while True:
	elems = browser.find_elements_by_css_selector('#mainsrp-itemlist > div > div > div:nth-child(1) > div')  # Find the search box
	collectUrl(elems)
	nextButton = browser.find_element_by_css_selector("#mainsrp-pager > div > div > div > ul > li.item.next > a")
	count = count + 1
	if nextButton and count < 40:
		#打印结果显示，在第一页时，下一页的地址还是第一页，第二页开始正常
		#所以不能正常使用brower.get，只能模拟点击
		print nextButton.get_attribute("href")
		# browser.get(nextButton.get_attribute("href"))
		nextButton.click()
		#由于点击并不会等待加载完毕
		#强制等待界面加载完成(部分)
		while True:
			time.sleep(1)
			tmpButton = browser.find_element_by_css_selector("#mainsrp-pager > div > div > div > ul > li.item.next > a")
			if tmpButton:
				break
	else:
		break
f = codecs.open('result.txt','w','utf-8')
def collectInfo(url):
	browser.get(url)
	# 淘宝和天猫的界面 不一样
	elems = browser.find_elements_by_css_selector('#J_DetailMeta > div.tm-clear > div.tb-property > div > div.tb-key > div > div > dl:nth-child(1) > dd > ul > li')
	if len(elems) == 0:
		elems = browser.find_elements_by_css_selector('#J_isku > div > dl.J_Prop.J_TMySizeProp.tb-prop.tb-clear.J_Prop_measurement > dd > ul > li')
		
	size = []
	for elem in elems:
		size.append(elem.text)
	sizeStr = ",".join(size)
	# 抓取数量,天猫能正常抓取数量 ，而淘宝不能
	countElem = browser.find_elements_by_css_selector("#J_DetailMeta > div.tm-clear > div.tb-property > div > ul > li.tm-ind-item.tm-ind-sellCount > div > span.tm-count")
	if len(countElem) == 0:
		countElem = browser.find_elements_by_css_selector("#J_Counter > div > div.tb-sell-counter > a")

	line = url + "," + countElem[0].text + ", " + sizeStr + "\n"
	f.write(line)
count = 0
for url in urls:
	if count > 1300:
		break
	count = count + 1
	collectInfo(url)
f.close()

browser.quit()