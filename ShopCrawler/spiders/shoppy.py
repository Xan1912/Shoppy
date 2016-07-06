from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from ShopCrawler.items import ShopcrawlerItem
from scrapy.selector import Selector
from scrapy.spiders import Spider
from lxml import html
from unittest.case import TestCase

class ShopSpider(CrawlSpider):

	name = 'shoppy'
	allowed_domains = ["www.shopping.com"]
	
	keyword = raw_input("Enter desired keyword:")	
	page_number = raw_input("Enter desired page number:")

	if not keyword:
		print "Error 404: Not found."

	def set_urls(keyword, page_number):
		 
		if not page_number:
			start = ["http://www.shopping.com/products?KW={0}" .format(keyword)]
			return start
		else:	
			start = ["http://www.shopping.com/products~PG-{0}?KW={1}" .format(page_number, keyword)]
			return start

	if keyword:
		
		start_urls = set_urls(keyword, page_number) 
	
		rules = (Rule(SgmlLinkExtractor(allow = ['\\/info']), callback=('parse_item'), follow=True),)

	
		def parse_item(self, response):
			sel = Selector(response)
			sites = sel.xpath('//div[@class="contentInner  singleModelContainer "]')
		
			items = []

			for site in sites:
			
				item = ShopcrawlerItem()

				item['title'] = "".join(site.xpath('//div[@class="hproduct"]/h1/text()').extract())
				item['price'] = "".join(site.xpath('//div[@class="productPriceBox"]/span/text()').extract())
				items.append(item)

			return items



	