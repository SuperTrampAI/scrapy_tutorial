# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyTutorialItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()


class Product(scrapy.Item):
    name=scrapy.Field()
    price=scrapy.Field()
    stock=scrapy.Field()
    tags=scrapy.Field()
    last_updated=scrapy.Field(serializer=str)

