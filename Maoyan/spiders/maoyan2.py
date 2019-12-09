# -*- coding: utf-8 -*-
import scrapy
from ..items import MaoyanItem
import time


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan2'
    allowed_domains = ['maoyan.com']
    # start_urls = ['https://maoyan.com/board/4?offset=0']
    offset=0

    #重写start_requests()方法
    def start_requests(self):
        url='https://maoyan.com/board/4?offset={}'
        for offset in range(0,91,10):
            page_url=url.format(offset)
            yield  scrapy.Request(
                url=page_url,
                callback=self.parse_html
            )
            time.sleep(0.5)

    def parse_html(self, response):
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



