# -*- coding: utf-8 -*-
# @Time    : 2020/3/27 10:54
# @Author  : Marko Li 'lxh800109@gmail.com'
# @Site    : 
# @File    : SelectorsLearn.py
# @Software: PyCharm
# __create_data__=2020/3/27 10:54
# @Description: add Description

# xpath 使用text()
# css 使用 ::text
# 使用selector response.selector.xpath('//span/text()').get()

from scrapy.selector import Selector
from scrapy.http import HtmlResponse

# body = '<html><body><span>good</span></body></html>'
# response = HtmlResponse(url='http://example.com', body=body)
# Selector(response=response).xpath('//span/text()').get()

# <html>
#  <head>
#   <base href='http://example.com/' />
#   <title>Example website</title>
#  </head>
#  <body>
#   <div id='images'>
#    <a href='image1.html'>Name: My image 1 <br /><img src='image1_thumb.jpg' /></a>
#    <a href='image2.html'>Name: My image 2 <br /><img src='image2_thumb.jpg' /></a>
#    <a href='image3.html'>Name: My image 3 <br /><img src='image3_thumb.jpg' /></a>
#    <a href='image4.html'>Name: My image 4 <br /><img src='image4_thumb.jpg' /></a>
#    <a href='image5.html'>Name: My image 5 <br /><img src='image5_thumb.jpg' /></a>
#   </div>
#  </body>
# </html>

# scrapy shell https://docs.scrapy.org/en/latest/_static/selectors-sample1.html

# response.xpath('//title/text()') 获取title标签在内的文本
# response.xpath('//title/text()').get() 获取title标签内的文本 如果有多个匹配到的，返回匹配到的第一个；如果没有匹配项，返回None
# response.css('img').xpath('@src').getall()
# response.xpath('//div[@id="images"]/a/text()').get(default='not-found')
# response.xpath('//div[@id="not-exists"]/text()').get() is None
# response.css('img').attrib['src'] 返回匹配到的第一个
# response.css('base').attrib(href')

# response.xpath('//base/@href').get()
# response.css('base::attr(href)').get()
# response.css('base').attrib['href']
# response.css('a[href*=image]::attr(href)').getall()
# response.css('#images *::text').getall() 获取id=images下的所有子节点的文本内容
# response.css('a::attr(href)').getall() 获取a链接中href属性的值
# links = response.xpath('//a[contains(@href,"image")]')
# for index,link in enumerate(links):
#    args=(index,link.xpath('@href').get(),link,xpath('img@src').get())

# 获取属性值的方法：
# response.xpath('//a/@href').getall()
# response.css('a::attr(href)').getall()
# 在python代码中使用：[a.attrib['href'] for a in response.css('a')]
# response.xpath('//a[contains(@href,"image")]/text()').re(r'Name:\s*(.*)')
# response.xpath('//a[contains(@href,"image")]/text()').re_first(r'Name:\s*(.*)') re是取得全部 re_first 只取得第一个



