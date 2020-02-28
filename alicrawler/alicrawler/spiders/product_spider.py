# 每个spider应该可以对应多个产品，每个产品对应一个Item，每个Item对应各自的django model

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

from alicrawler.items import ProductItem
from scrapy_selenium import SeleniumRequest


class ProductSpider(scrapy.Spider):
    name = 'product_spider'

    # start_urls = ['http://127.0.0.1:8000/ct/ri']
    # start_urls = ['http://www.okbuy.com/p-nike/detail-shoe-17844839.html']
    def start_requests(self):

        # We scrape the first 5 pages of books to scrape
        urls = [
            'http://www.okbuy.com/p-nike/detail-shoe-17844839.html',
        ]

        # We generate a Request for each URL
        # We also specify the use of the parse function to parse the responses
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10)

    def parse(self, response):
        product = response.css('div.prodConDetail')
        product_loader = ItemLoader(item=ProductItem(), selector=product)

        product_loader.default_output_processor = TakeFirst()

        product_loader.add_css('title', '#prodTitleName::text')
        product_loader.add_css('desc', '#prodTitleName::text')
        product_loader.add_css('price', '#prodPriceAj::text')

        print('\n')

        yield product_loader.load_item()
