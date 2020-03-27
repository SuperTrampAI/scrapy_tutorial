# -*- coding: utf-8 -*-
# @Time    : 2020/3/26 13:56
# @Author  : Marko Li 'lxh800109@gmail.com'
# @Site    : 
# @File    : toscrape-css.py
# @Software: PyCharm
# __create_data__=2020/3/26 13:56
# @Description: add Description


import scrapy

# 所有的自定义的spider都必须继承scrapy.Spider
# 该类提供了一个默认的start_request() 该实例发送来自start_url ，并默认调用parse方法
class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css" # scrapy更具该变量查找spider 并实例化，如果这个spider是抓取单个网页，一般使用域名命名该spider
    # allowed_domains=''
    # custom_settings = '' 覆盖默认的配置，
    start_urls = [ # 下载的第一个页面将是该变量的值
        'http://quotes.toscrape.com/',
    ]
    # 默认回调方法
    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                'text': quote.css("span.text::text").extract_first(),
                'author': quote.css("small.author::text").extract_first(),
                'tags': quote.css("div.tags > a.tag::text").extract()
            }

        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

