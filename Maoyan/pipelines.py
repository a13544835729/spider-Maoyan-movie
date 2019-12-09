# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MaoyanPipeline(object):
    def process_item(self, item, spider):
        print(item['name'],item['star'],item['time'])
        return item


import pymysql
from .settings import *
#数据库存入mysql
class MaoyanMysqlPipeline(object):
    #监听爬虫,爬虫启动时只执行一次
    def open_spider(self,spider):
        self.db=pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PWD,
        database=MYSQL_DB,
        charset=MYSQL_CHAR
        )
        self.cur=self.db.cursor()
        print('我是open spider')


    def process_item(self,item,spider):
        sql='insert into filmtab values(%s,%s,%s)'
        L=[item['name'],item['star'],item['time']]
        self.cur.execute(sql,L)
        self.db.commit()

        #return 将item传到下一个管道
        return item

    #监听爬虫,爬虫结束时只执行一次,一般用于数据库断开
    def close_spider(self,spider):
        self.cur.close()
        self.db.close()
        print('我是结束spider')

import pymongo
#
class MaoyanMongoPipeline(object):
    def open_spider(self,spider):
        self.conn=pymongo.MongoClient(
            host=MONGO_HOST,
            port=MONGO_PORT
        )
        self.db=self.conn['maoyandb']
        self.myset=self.db['maoyanset']
        print('开始')


    def process_item(self,item,spider):
        # L=dict(item)
        L={
            'name':item['name'],
            'star':item['star'],
            'time':item['time']
           }
        self.myset.insert_one(L)
        return item

    # def close_spider(self,spider):

