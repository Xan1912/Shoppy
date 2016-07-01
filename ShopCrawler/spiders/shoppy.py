from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from ShopCrawler.items import ShopcrawlerItem
from scrapy.selector import Selector
from scrapy.spiders import Spider
from lxml import html


        

class ShopSpider(CrawlSpider):

	name = 'shoppy'
	allowed_domains = ["www.shopping.com"]
	
	keyword = raw_input("Enter desired keyword:")	
	page_number = raw_input("Enter desired page_number:")

	
	url = "http://www.shopping.com/products?KW={0}" .format(keyword) 
	url2 = "http://www.shopping.com/products~PG-{0}?KW={1}" .format(page_number, keyword)
	
	if page_number == None:
		start_urls = [url]
	else:	
		start_urls=[url, url2]

	rules = (Rule(SgmlLinkExtractor(allow = ['\\/info']), callback=('parse_item'), follow=True),)

	def parse_item(self, response):
		sel = Selector(response)
		sites = sel.xpath('//div[@class="contentInner  singleModelContainer "]')
		print sites
		items = []

		for site in sites:
			
			item = ShopcrawlerItem()

			item['title'] = "".join(site.xpath('//div[@class="hproduct"]/h1/text()').extract())
			item['price'] = "".join(site.xpath('//div[@class="productPriceBox"]/span/text()').extract())
			items.append(item)

		return items