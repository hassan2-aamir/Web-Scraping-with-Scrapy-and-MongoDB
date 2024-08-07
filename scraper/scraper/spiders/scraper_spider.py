from scrapy import Spider
from scrapy.selector import Selector
from scraper.items import ScraperItem

class ScraperSpider(Spider):
    name = "scraper"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "http://stackoverflow.com/questions?pagesize=50&sort=newest",
    ]

    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="s-post-summary--content"]/h3')
        for question in questions:
            item = ScraperItem()
            item['title'] = question.xpath(
                'a[@class="s-link"]/text()').extract()[0]
            item['url'] = question.xpath(
                'a[@class="s-link"]/@href').extract()[0]
            yield item
