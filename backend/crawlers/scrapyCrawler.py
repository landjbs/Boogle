from scrapy.crawler import CrawlerProcess
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from stack.items import StackItem


class StackCrawlerSpider(CrawlSpider):
    name = 'stack_crawler'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['www.yale.edu']

    rules = [
    Rule(LinkExtractor(allow=r'questions\?page=[0-9]&sort=newest'),
         callback='parse_item', follow=True)]

    def parse_item(self, response):
        questions = response.xpath('//div[@class="summary"]/h3')

        for question in questions:
            item = StackItem()
            item['url'] = question.xpath(
                'a[@class="question-hyperlink"]/@href').extract()[0]
            item['title'] = question.xpath(
                'a[@class="question-hyperlink"]/text()').extract()[0]
            yield item


process.crawl(StackCrawlerSpider)
process.start() # the script will block here until the crawling is finished
