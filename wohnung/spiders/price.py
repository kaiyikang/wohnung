import scrapy
from urllib import parse

class PriceSpider(scrapy.Spider):
    name = 'price'
    
    wg_base_url = "https://www.wg-gesucht.de"
    
    def start_requests(self):
        """负责dump出最初的url
        """        
        urls = ["https://www.wg-gesucht.de/1-zimmer-wohnungen-in-Munchen.90.1.1.0.html?offer_filter=1&city_id=90&noDeact=1&categories%5B%5D=1&rent_types%5B%5D=0"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """ yield pages
        """
        all_pages = response.css("ul.pagination.pagination-sm a")
        for page in all_pages[1:-1]:
            url = page.css("a::attr(href)").get()
            url = parse.urljoin(self.wg_base_url,url)
            yield scrapy.Request(url=url, callback=self.page_parse)
            
        
    def page_parse(self,response):
        """ 获取每个wohnung的链接
        """
        all_wohnungs = response.css("h4.headline a.detailansicht::attr(href)").getall()
        for wohnung in all_wohnungs:
            url = parse.urljoin(self.wg_base_url,wohnung)
            yield scrapy.Request(url=url, callback=self.wohnung_parse)
            
    
    def page_parse(self,response):
        """ 获取wohnung中的信息，填入表格
        """
        all_wohnungs = response.css("h4.headline a.detailansicht::attr(href)").getall()
        for wohnung in all_wohnungs:
            url = parse.urljoin(self.wg_base_url,wohnung)
            yield scrapy.Request(url=url, callback=self.wohnung_parse)