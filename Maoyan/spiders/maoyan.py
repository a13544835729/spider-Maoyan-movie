# -*- coding: utf-8 -*-
import scrapy
from ..items import MaoyanItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/board/4?offset=0']
    offset=0

    def parse(self, response):
        #给items.py 中的类实例化
        item=MaoyanItem()
        dd_list=response.xpath('//dl[@class="board-wrapper"]/dd')
        for dd in dd_list:
            #给item对象的3个属性赋值,必须使用['']
            item['name']=dd.xpath('./a/@title').get()
            item['star']=dd.xpath('.//p[@class="star"]/text()').get()
            item['time']=dd.xpath('.//p[@class="releasetime"]/text()').get()

            #数据交给管道的方式
            yield item

            #把下一页的地址交给调度器
        self.offset+=10
        if self.offset<=90:
            url='https://maoyan.com/board/4?offset='+str(self.offset)
            yield  scrapy.Request(
                url=url,
                callback=self.parse
            )


