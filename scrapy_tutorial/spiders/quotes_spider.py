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
from scrapy.linkextractors import LinkExtractor
#  运行该命令：scrapy crawl quotes
# 爬虫必须继承自Spider
from scrapy.spiders import CrawlSpider, Rule, XMLFeedSpider, CSVFeedSpider

from scrapy_tutorial.items import ScrapyTutorialItem


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
    name = "quotes3"  # 在该项目中要唯一
    allowed_domains = ['quotes.toscrape.com']
    page = 1
    start_urls = [
        'http://quotes.toscrape.com/api/quotes?page=1',
    ]

    def parse(self, response):
        data = json.loads(response.text)  # 从第一页开始 解析response.text 赋值给data
        for quote in data['quotes']:  # 遍历并打印quote['text']
            yield {'quote': quote['text']}
        if data['has_next']:  # 如果有下一页，则继续发起请求
            self.page += 1
            url = 'http://quotes.toscrape.com/api/quotes?page={}'.format(self.page)
            yield scrapy.Request(url=url, callback=self.parse)


# 运行命令：scrapy crawl quotes4 -o quotes.json
class QuotesSpider4(scrapy.Spider):  # 必须要继承自Spider
    name = 'quotes4'  # 在该项目中必须唯一
    start_urls = [
        'http://quotes.toscrape.com/tag/humor/',
    ]

    # 默认回调parse方法
    def parse(self, response):
        for quote in response.css('div.quote'):  # 按照css选择器来过滤数据
            yield {
                'author': quote.xpath('span/small/text()').get(),  # 在选择器下找到并获取文本数据
                # get 获取一条数据
                'text': quote.css('span.text::text').get(),
            }

        next_page = response.css(
            'li.next a::attr("href")').get()  # 可以把选择器传给follow方法，可以传递多个 多个使用：response.follow_all(..)
        if next_page is not None:  # 判断是否有下一页，有则继续回调
            # response.follow 创建request的另外一种方式 支持相对url的调用。
            yield response.follow(next_page, self.parse)
            # yield from response.follow_all(css='ul.pager a',callback=self.parse)


# 运行命令：scrapy crawl quotes5
# 运行保存的命令：scrapy crawl quotes4 -o quotes5.json 该命令会在原有文件的基础上新增，而不是覆盖
# scrapy crawl quotes4 -o quotes5.jl  JSON Lines 该文件格式存储json lines 每条数据都是一行
class QuotesSpider5(scrapy.Spider):
    name = 'quotes5'
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }


# scrapy crawl quotes6
class QuotesSpider6(scrapy.Spider):
    name = 'quotes6'

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('smal.author::text').get(),
            }
            next_page = response.css('li.next a::attr(href)').get()
            if next_page is not None:
                yield response.follow(next_page, self.parse)


class MySpider(scrapy.Spider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = [
        'http://www.example.com/1.html',
        'http://www.example.com/2.html',
        'http://www.example.com/3.html',
    ]

    # 不使用start_urls的方式：
    # def start_requests(self):
    #     yield scrapy.Request('http://www.example.com/1.html', self.parse)
    #     yield scrapy.Request('http://www.example.com/2.html', self.parse)
    #     yield scrapy.Request('http://www.example.com/3.html', self.parse)
    # 在__init__ 方法中设置参数：
    # def __init__(self,category=None,*args,**kwargs):
    #     super(MySpider,self).__init__(*args,**kwargs)
    #     self.start_urls=['url' & category]
    def parse(self, response):
        # self.logger.inof('A response from %s just arrived!', response.url)
        # 从单个回调返回多个请求
        for h3 in response.xpath('//h3').getall():
            yield {'title': h3}
        for href in response.xpath('//a/@href').getall():
            yield scrapy.Request(response.urljoin(href), self.parse)


# CrawlSpider 定义了一组规则为了跟踪链接
class QuotesSpider6(CrawlSpider):
    name = 'QuotesSpider6'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com']
    # CrawSpider 必须要指定的。定义爬取网站的特定行为。
    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('category\.php',), deny=('subsection\.php',))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('item\.php',)), callback='parse_item'),
    )

    def parse_item(self, response):
        self.logger.info('Hi this is an item page: %s', response.url)
        item = scrapy.Item()
        item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        item['name'] = response.xpath('//td[@id="item_name"]/text()').get()
        item['description'] = response.xpath('//td[@id="item_description"]/text()').get()
        item['link_text'] = response.meta['link_text']
        return item


class QuotesSpider7(XMLFeedSpider):
    name = 'QuotesSpider7'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com/feed.xml']
    iterator = 'iternodes'
    itertag = 'item'

    def parse_node(self, response, node):
        self.logger.info('hi ,this a <%s> node :%s', self.itertag, ''.join(node.getall()))
        item = ScrapyTutorialItem()
        item['id'] = node.xpath('@id').get()
        item['name'] = node.xpath('name').get()
        item['description'] = node.xpath('description').get()
        return item


class QuotesSpider8(CSVFeedSpider):
    name = 'QuotesSpider8'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com/feed.csv']
    delimiter = ';'
    quotechar = "'"
    headers = ['id', 'name', 'description']

    def parse_node(self, response, row):
        self.logger.info('hi ,this a row %r', row)
        item = ScrapyTutorialItem()
        item['id'] = row['id']
        item['name'] = row['name']
        item['description'] = row['description']
        return item
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

# 使用attr获取href中的路径
# response.css("li.next a::attr(href)").get() or response.css("li.next a").attrib['href']
