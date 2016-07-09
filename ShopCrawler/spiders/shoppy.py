from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from ShopCrawler.items import ShopcrawlerItem
from scrapy.selector import Selector
from scrapy.spiders import Spider
from lxml import html
import requests
import bs4

class ShopSpider(CrawlSpider):

	name = 'shoppy'
	allowed_domains = ["www.shopping.com"]
	
	keyword = raw_input("Enter desired keyword:")	
	page_number = raw_input("Enter desired page number:")

	if not page_number:

		start_urls = ["http://www.shopping.com/products?KW={0}" .format(keyword)]
		rules = (Rule(SgmlLinkExtractor(allow = ['\\/info', '\\/itm', '\\/like']), callback=('parsePage'), follow=True),)

	else:
		
		start_urls = ["http://www.shopping.com/products~PG-{0}?KW={1}" .format(page_number, keyword)]
		rules = (Rule(SgmlLinkExtractor(allow = ['\\/info', '\\/itm', '\\/like']), callback=('parsePage'), follow=False),)

	baseUrl = "".join(start_urls)
	response = requests.get(baseUrl)
	soup = bs4.BeautifulSoup(response.text, "lxml")
	count = ("".join(soup.find("span", {"class": "numTotalResults"}).contents)).strip()
	print count
	
	def parsePage(self, response):
		sel = Selector(response)
		sites = sel.xpath('//div[@class="contentInner  singleModelContainer "]')
		
		items = []

		for site in sites:
			
			item = ShopcrawlerItem()

			item['title'] = "".join(site.xpath('//div[@class="hproduct"]/h1/text()').extract())
			item['price'] = "".join(site.xpath('//div[@class="productPriceBox"]/span/text()').extract())
			
			items.append(item)

		return items

	

	

		


	