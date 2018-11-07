# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from jdWare.items import SpuItem
from jdWare.items import SkuItem
from jdWare.items import ReviewItem

class JdwarePipeline(object):

	def __init__(self):
		self.client = pymongo.MongoClient(host = settings['MONGO_HOST'], port = settings['MONGO_PORT'])
		self.db = self.client[settings['MONGO_DB']]

	def process_item(self, item, spider):
		if isinstance(item, SpuItem):
			postItem = dict(item)
			self.db["SPU"].insert(postItem)
		elif isinstance(item, SkuItem):
			postItem = dict(item)
			self.db["SKU"].insert(postItem)
		elif isinstance(item, ReviewItem):
			postItem = dict(item)
			self.db["REVIEW"].insert(postItem)