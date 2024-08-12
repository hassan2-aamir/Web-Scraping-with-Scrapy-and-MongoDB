from scrapy import Spider
from scrapy.selector import Selector
from scraper.items import ScraperItem
from scrapy import Request

class ScraperSpider(Spider):
    name = "scraper"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "https://stackoverflow.com/questions/tagged/python?tab=Newest&pagesize=50",
    ]

    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="s-post-summary--content"]/h3')
        for question in questions:
            item = ScraperItem()
            item['title'] = question.xpath(
                'a[@class="s-link"]/text()').extract()[0]
            item['url'] = question.xpath(
                'a[@class="s-link"]/@href').extract()[0]
            
            absolute_url = response.urljoin(item['url'])
            
            # Make a request to the question's page and pass the item along with it
            request = Request(absolute_url, callback=self.parse_question)
            request.meta['item'] = item
            yield request
            
            

    def parse_question(self, response):
        item = response.meta['item']
        
        # Extract the main text of the question from the question page
        question_text = response.xpath('//div[@class="s-prose js-post-body"]/p/text()').extract()
        item['question'] = ' '.join(question_text)
        
        yield item