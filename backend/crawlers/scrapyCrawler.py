import scrapy
from scrapy.crawler import CrawlerProcess

class AliexpressTabletsSpider(scrapy.Spider):
    name = 'aliexpress_tablets'
    start_urls = ['https://www.aliexpress.com/category/200216607/tablets.html']


    def parse(self, response):
        print("procesing:"+response.url)
        #Extract data using css selectors
        product_name=response.css('.product::text').extract()
        price_range=response.css('.value::text').extract()
        #Extract data using xpath
        orders=response.xpath("//em[@title='Total Orders']/text()").extract()
        company_name=response.xpath("//a[@class='store $p4pLog']/text()").extract()

        row_data=zip(product_name,price_range,orders,company_name)

        #Making extracted data row wise
        for item in row_data:
            #create a dictionary to store the scraped info
            scraped_info = {
                #key:value
                'page':response.url,
                'product_name' : item[0], #item[0] means product in the list and so on, index tells what value to assign
                'price_range' : item[1],
                'orders' : item[2],
                'company_name' : item[3],
            }

            print(scraped_info)

            #yield or give the scraped info to scrapy
            yield scraped_info


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(AliexpressTabletsSpider)
process.start() # the script will block here until the crawling is finished
