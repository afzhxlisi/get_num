# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GetNumItem(scrapy.Item):
    threeMonSaled = scrapy.Field()
    totalWatchNum = scrapy.Field()
    typename = scrapy.Field()
    numType = scrapy.Field()
    price = scrapy.Field()
    onSale = scrapy.Field()
    pass
