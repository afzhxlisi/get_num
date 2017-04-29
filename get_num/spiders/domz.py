# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.http import Request
from get_num.items import GetNumItem
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import MySQLdb

class CrawlSpider(scrapy.Spider):

    name = "domz"
    allowed_domains = ["sh.lianjia.com"]
    start_urls = ['http://sh.lianjia.com/ershoufang']
    page = 1;
    count =1;
    total = 1;
    def parse(self, response):
        nums = response.xpath("//ul[@class='content']//span[contains(@class,'num')]/text()")
        onSale = nums[0].extract()
        self.total = onSale
        lastThreeMonSales = nums[1].extract()
        totalWatchNum = nums[2].extract()
        typename=response.xpath("//*[@class='m-side-bar']/div/span[@class='header-text']/text()")[0].extract()
        numType=response.xpath("//*[@class='m-side-bar']/div/span[contains(@class,'c-hollow-tag')]/text()")[0].extract()
        item =GetNumItem()
        item['onSale']=onSale
        item['threeMonSaled'] = totalWatchNum
        item['totalWatchNum'] = totalWatchNum
        item['typename'] = typename
        item['numType'] = numType
        yield item
        urls = self.getComList();
        for url in urls:
            xiaoqu = url[0].replace('/xiaoqu/','').replace('.html','')
            xiaoqu = 'q'+xiaoqu
            url = "http://sh.lianjia.com/ershoufang/" + xiaoqu
            yield Request(url, callback=self.parseItem)
    def parseItem(self,response):
        nums = response.xpath("//ul[@class='content']//span[contains(@class,'num')]/text()")
        price = nums[0].extract()
        #self.total = price
        onsale = nums[1].extract()
        threeMonSaled = nums[2].extract()
        totalWatchNum = nums[3].extract()
        print nums
        typename = response.xpath("//*[@class='m-side-bar']/div/a[contains(@class,'header-text')]/text()")[0].extract()
        numType = response.xpath("//*[@class='m-side-bar']/div/span[contains(@class,'c-hollow-tag')]/text()")[
            0].extract()
        item = GetNumItem()
        item['price'] = price
        item['threeMonSaled'] = threeMonSaled
        item['totalWatchNum'] = totalWatchNum
        item['typename'] = typename
        item['numType'] = numType
        item['onSale'] = onsale

        yield item
    def getComList(self):
        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='12345678', db='test', port=3306,
                                        charset='utf8')
        self.cur = self.conn.cursor()

        str = datetime.date.today().__str__()
        cur = self.cur
        cur.execute('select comurl from lianjia where date(time) =date(\''+str+'\')')
        results = cur.fetchall()
        self.cur.close()
        self.conn.close()
        return results