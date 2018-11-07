# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpuItem(scrapy.Item):
	SPU_NUM  = scrapy.Field()
	SPU_ID   = scrapy.Field()
	SPU_TIT  = scrapy.Field()
	SPU_DESP = scrapy.Field()
	SPU_SPEC = scrapy.Field()
	SPU_RATE = scrapy.Field()
	SPU_REVNUM = scrapy.Field()
	SPU_TREVNUM = scrapy.Field()



class SkuItem(scrapy.Item):
	SPU_NUM  = scrapy.Field()
	SKU_ID   = scrapy.Field()
	SKU_TIT  = scrapy.Field()
	SKU_PRICEBF = scrapy.Field()
	SKU_PRICEAF = scrapy.Field()



class ReviewItem(scrapy.Item):
	SPU_NUM = scrapy.Field()
	SPU_TIT = scrapy.Field()
	U_NAME = scrapy.Field()
	U_LEVEL = scrapy.Field()
	SKU_TIT = scrapy.Field()
	REV_TIME = scrapy.Field()
	REV_CONTENT = scrapy.Field()
	REV_SCORE = scrapy.Field()
	REV_PIC = scrapy.Field()
