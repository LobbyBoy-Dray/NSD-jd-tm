# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
from jdWare.items import SpuItem
from jdWare.items import SkuItem
from jdWare.items import ReviewItem


# 需:增加2页测试

class JdspiderSpider(scrapy.Spider):
	name = 'jdSpider'
	allowed_domains = ['so.m.jd.com']
	keyword = "ps4"
	pageNum = 1
	pagesize = 100
	wareCounter = 0
	headers_search = {
		"accept":"*/*",
		"accept-encoding":"gzip, deflate, br",
		"accept-language":"zh-CN,zh;q=0.9",
		"user-agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25",
	}
	headers_detail = {
		"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"accept-encoding":"gzip, deflate, br",
		"accept-language":"zh-CN,zh;q=0.9",
		"cache-control":"max-age=0",
		"upgrade-insecure-requests":"1",
		"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
	}
	headers_rate = {
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"Accept-Encoding":"gzip, deflate, br",
		"Accept-Language":"zh-CN,zh;q=0.9",
		"Connection":"keep-alive",
		"Host":"club.jd.com",
		"Upgrade-Insecure-Requests":"1",
		"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
	}
	headers_price = {
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"Accept-Encoding":"gzip, deflate, br",
		"Accept-Language":"zh-CN,zh;q=0.9",
		"Connection":"keep-alive",
		"Host":"pe.3.cn",
		"Upgrade-Insecure-Requests":"1",
		"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
	}
	headers_review = {
		"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"accept-encoding":"gzip, deflate, br",
		"accept-language":"zh-CN,zh;q=0.9",
		"upgrade-insecure-requests":"1",
		"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
	}


	def start_requests(self):
		# page从1开始，75页是最后一页，76页开始就没有了
		url = "https://so.m.jd.com/ware/search._m2wq_list?keyword=%s&datatype=1&page=%s&pagesize=%s" % (self.keyword, str(self.pageNum), str(self.pagesize))
		yield scrapy.Request(url, headers = self.headers_search, dont_filter = True)


	def parse(self, response):
		pattern = re.compile(r"searchCB\((.*)\)")
		text = response.text
		text = text.replace('\n','')
		text = text.replace('\\','\\\\')
		# 特殊字符替换
		data = pattern.search(text).group(1)
		data = json.loads(data)
		# try:
		# 	data = json.loads(data)
		# except:
		# 	print("json解析错误")
		# 	with open("errorDATA.txt", "w", encoding = 'utf-8') as f:
		# 		f.write(data)
		# 	time.sleep(100)
		wares = data["data"]["searchm"]["Paragraph"]
		# 增加2页测试
		if wares:
			for ware in wares:
				self.wareCounter += 1
				wNum = "P%s" % str(self.wareCounter)
				wId = ware["wareid"]
				url = "https://item.jd.com/%s.html" % str(wId)
				yield scrapy.Request(url, headers = self.headers_detail, callback = self.parseWareDetail, meta = {'wNum':wNum, 'wId':wId}, dont_filter = True)
			print("【%s】第【%s】页, 共【%s】件商品" % (self.keyword, str(self.pageNum), str(len(wares))))
			# 下一页
			self.pageNum += 1
			url = "https://so.m.jd.com/ware/search._m2wq_list?keyword=%s&datatype=1&page=%s&pagesize=%s" % (self.keyword, str(self.pageNum), str(self.pagesize))
			yield scrapy.Request(url, headers = self.headers_search, dont_filter = True)
		else:
			print("【%s】最后一页+1" % self.keyword)


	def parseWareDetail(self, response):
		meta = response.meta
		# SPU_NUM
		wNum = meta["wNum"]
		# SPU_ID
		wID = meta["wId"]
		# SPU_TIT: 商品名称
		wName = response.xpath(".//div[@class='sku-name']/text()").extract()[0].strip()
		# SPU_DESP: 商品介绍
		wDesp = []
		allDesp = response.xpath(".//div[@class='p-parameter']/ul/li")
		for i in allDesp:
			desp = i.xpath("string(.)").extract()[0].strip()
			wDesp.append(desp)
		# SPU_SPEC: 商品规格
		wSpec = []
		allSpec = response.xpath(".//div[@class='Ptable']/div/dl/dl")
		for i in allSpec:
			i1 = i.xpath("./dt/text()").extract()[0].strip()
			i2 = i.xpath("./dd/text()").extract()[0].strip()
			i3 = ":".join([i1,i2])
			wSpec.append(i3)
		url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds=%s" % str(wID)
		yield scrapy.Request(url, headers = self.headers_rate, callback = self.parseRate, meta = {"wNum":wNum, "wID":wID, "wName":wName, "wDesp":wDesp, "wSpec":wSpec}, dont_filter = True)
		# SKU项目，不同版本
		all_SPU_NUM = response.xpath(".//div[@id='choose-attrs']/div[1]/div[@class='dd']/div/@data-sku").extract()
		all_SKU_TIT = response.xpath(".//div[@id='choose-attrs']/div[1]/div[@class='dd']/div/@data-value").extract()
		temp = ','.join(all_SPU_NUM)
		url = "https://pe.3.cn/prices/mgets?skuids=%s" % temp
		yield scrapy.Request(url, headers = self.headers_price, callback = self.parsePrice, meta = {"wNum":wNum, "wID":wID, "all_SPU_NUM":all_SPU_NUM, "all_SKU_TIT":all_SKU_TIT}, dont_filter = True)
		# Review项目，评论，page从0开始
		reviewPageNum = 0
		url = "https://sclub.jd.com/comment/productPageComments.action?productId=%s&score=0&sortType=6&page=%s&pageSize=10" % (wID, str(reviewPageNum))
		yield scrapy.Request(url, headers = self.headers_review, callback = self.parseReview, meta = {"wNum":wNum, "wID":wID, "reviewPageNum":reviewPageNum}, dont_filter = True)


	# SPU项目全部爬取完毕
	def parseRate(self, response):
		meta = response.meta
		wNum = meta["wNum"]
		wID = meta["wID"]
		wName = meta["wName"]
		wDesp = meta["wDesp"]
		wSpec = meta["wSpec"]
		text = response.text
		data = json.loads(text)
		# SPU_RATE: 商品口碑得分
		wGoodRate = data["CommentsCount"][0]["GoodRate"]
		# SPU_REVNUM: 总评论数量
		wRevNum = data["CommentsCount"][0]["CommentCount"]
		# SPU_TREVNUM: 实际评论数量
		wTrevNum = data["CommentsCount"][0]["CommentCount"] - data["CommentsCount"][0]["DefaultGoodCount"]
		spuItem = SpuItem()
		spuItem["SPU_NUM"] = wNum
		spuItem["SPU_ID"] = wID
		spuItem["SPU_TIT"] = wName
		spuItem["SPU_DESP"] = wDesp
		spuItem["SPU_SPEC"] = wSpec
		spuItem["SPU_RATE"] = wGoodRate
		spuItem["SPU_REVNUM"] = wRevNum
		spuItem["SPU_TREVNUM"] = wTrevNum
		print("SPU: 商品【%s】" % str(wID))
		yield spuItem


	# SKU项目全部爬取完毕
	def parsePrice(self, response):
		meta = response.meta
		wNum = meta["wNum"]
		wID  = meta["wID"]
		all_SPU_NUM = meta["all_SPU_NUM"]
		all_SKU_TIT = meta["all_SKU_TIT"]
		data = json.loads(response.text)
		for i in zip(all_SPU_NUM, all_SKU_TIT, data):
			skuItem = SkuItem()
			skuItem["SPU_NUM"] = wNum
			skuItem["SKU_ID"]  = i[0]
			skuItem["SKU_TIT"] = i[1]
			skuItem["SKU_PRICEBF"] = float(i[2]["op"])
			skuItem["SKU_PRICEAF"] = float(i[2]["p"])
			print("SKU: 商品【%s】" % str(wID))
			yield skuItem


	# REVIEW项目
	def parseReview(self, response):
		meta = response.meta
		noCommentsTarget = meta.get("noCommentsTarget",0)
		wNum = meta["wNum"]
		wID  = meta["wID"]
		reviewPageNum = meta["reviewPageNum"]
		text = response.text
		data = json.loads(text)
		reviews = data["comments"]
		if reviews:
			for review in reviews:
				reviewItem = ReviewItem()
				reviewItem["SPU_NUM"] = wNum
				reviewItem["SPU_TIT"] = review["referenceName"]
				reviewItem["U_NAME"] = review["nickname"]
				reviewItem["U_LEVEL"] = review["userLevelName"]
				reviewItem["SKU_TIT"] = review["productColor"]
				reviewItem["REV_TIME"] = review["creationTime"]
				reviewItem["REV_CONTENT"] = review["content"]
				reviewItem["REV_SCORE"] = review["score"]
				reviewItem["REV_PIC"] = 1 if review.get("images") else 0
				yield reviewItem
			print("REVIEW: 商品【%s】, 第【%s】页" % (str(wID), str(reviewPageNum)))
			reviewPageNum += 1
			url = "https://sclub.jd.com/comment/productPageComments.action?productId=%s&score=0&sortType=6&page=%s&pageSize=10" % (wID, str(reviewPageNum))
			yield scrapy.Request(url, headers = self.headers_review, callback = self.parseReview, meta = {"wNum":wNum, "wID":wID, "reviewPageNum":reviewPageNum}, dont_filter = True)
		else:
			# 尝试2次，每次1分钟
			if noCommentsTarget < 2:
				noCommentsTarget += 1
				print("第%s次无comments!休眠60s后重试!" % str(noCommentsTarget))
				time.sleep(63)
				yield scrapy.Request(response.url, headers = self.headers_review, callback = self.parseReview, meta = {"wNum":wNum, "wID":wID, "reviewPageNum":reviewPageNum, "noCommentsTarget":noCommentsTarget}, dont_filter = True)
			else:
				print("========== 停止! ==========")
				print("comments为空")
				print(response.url)










