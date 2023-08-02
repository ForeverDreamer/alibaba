# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose
from scrapy_djangoitem import DjangoItem
from product.models import Product



def convert_price(price):
    if price:
        return float(price[1:].strip().replace(',', '')[1:])


def shorten_amazon_link(link):
    # product_id = link.split('/')[-1]
    # return 'https://amazon.in/dp/' + product_id
    return link


class AlicrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ProductItem(DjangoItem):
    django_model = Product


class TshirtItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(convert_price))
    description = scrapy.Field()
