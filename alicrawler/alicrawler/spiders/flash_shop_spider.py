# 每个spider应该可以对应多个产品，每个产品对应一个Item，每个Item对应各自的django model
import time
import random
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from alicrawler.items import TshirtItem
from scrapy_selenium import SeleniumRequest


class FlashShopSpider(scrapy.Spider):
    name = 'flash_shop_spider'

    def start_requests(self):

        # We scrape the first 5 pages of books to scrape
        urls = [
            'https://www.fendi.cn/man/readytowear/t-shirts-and-polos.html',
        ]

        # We generate a Request for each URL
        # We also specify the use of the parse function to parse the responses
        for url in urls:
            yield SeleniumRequest(
                wait_time=10,
                # css_selector直接从浏览器元素里边拷贝，别自己写了，老是出错
                wait_until=EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > div.products.page-layout > div.page-content > div.main > div.btn-wrap > div')),
                url=url, callback=self.navigate
            )

    def navigate(self, response):
        driver = response.request.meta['driver']
        # time.sleep(5)
        # while "w-product-card" not in driver.page_source:
        #     time.sleep(1)
        detail_urls = response.css('.w-product-card > a::attr(href)').extract()
        for url in detail_urls:
            yield SeleniumRequest(
                wait_time=10,
                wait_until=EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > div.product-detail.page-layout > div.page-content > div.main > div > div.product-container > div > div.product-r > div.product-more-list.product-more-item > div > dl.accordion-item.active > dd > div > div')),
                url=url, callback=self.parse
            )

    def parse(self, response, **kwargs):
        driver = response.request.meta['driver']
        # time.sleep(5)
        # while "accordion-info-inner" not in driver.page_source:
        #     time.sleep(1)
        # driver.implicitly_wait(random.randint(1, 3))
        # product_list = response.css('.w-product-card > a::attr(href)').extract()

        product_loader = ItemLoader(item=TshirtItem(), selector=response)

        product_loader.default_output_processor = TakeFirst()

        product_loader.add_css('title', '.product-desc::text')
        product_loader.add_css('description', '.accordion-info-inner > .desc::text')

        yield product_loader.load_item()
