# -*- coding: utf-8 -*-
# @Time    : 2020/3/25 15:32
# @Author  : Marko Li 'lxh800109@gmail.com'
# @Site    : 
# @File    : quotes_spider.py
# @Software: PyCharm
# __create_data__=2020/3/25 15:32
# @Description: add Description
import json

import scrapy


#  运行该命令：scrapy crawl quotes
# 爬虫必须继承自Spider
class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # parse 是scrapy的默认回调方法
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


class QuotesSpider2(scrapy.Spider):
    name = "quotes2"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)


# 运行命令：scrapy crawl quotes3
class QuotesSpider3(scrapy.Spider):
    name = "quotes3" # 在该项目中要唯一
    allowed_domains = ['quotes.toscrape.com']
    page = 1
    start_urls = [
        'http://quotes.toscrape.com/api/quotes?page=1',
    ]

    def parse(self, response):
        data = json.loads(response.text) # 从第一页开始 解析response.text 赋值给data
        for quote in data['quotes']: # 遍历并打印quote['text']
            yield {'quote': quote['text']}
        if data['has_next']: # 如果有下一页，则继续发起请求
            self.page += 1
            url = 'http://quotes.toscrape.com/api/quotes?page={}'.format(self.page)
            yield scrapy.Request(url=url, callback=self.parse)
# 提取数据的学习方式-使用scrapy shell：scrapy shell 'http://quotes.toscrape.com/page/1/' windows上使用双引号

# 使用response获取元素
# response.css('title').getall() 获取title元素包括title标签
# response.css('title::text').getall() 获取title文本,getall是获取全部
# get()可以获取单个 或者css():[0].get()

# 可以使用正则表达式提取内容：
# response.css('title::text').re(r'Quotes.*')

# 使用response.xpath('/html/body/div[1]/div[2]/div[1]/div[6]/span[1]/text()').getall()

# 完善上文的xpath：根据类选择器查找
# response.xpath('//span[has-class("text")]/text()').getall()

# 更换一个网站：
# scrapy shell "quotes.toscrape.com/scroll"
# view(response) 查看缓存在本地的请求，然后查看数据结构，用来定位

# 需要注意的是：在复杂的网站中，需要添加headers或cookies使其生效


