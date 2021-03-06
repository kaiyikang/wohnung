import scrapy
from urllib import parse
from ..items import WohnungItem
import datetime
import hashlib


def get_md5(s):
    md = hashlib.md5()
    md.update(s.encode('utf-8'))
    return md.hexdigest()

print(get_md5('kang'))

class PriceSpider(scrapy.Spider):
    name = 'price'
    
    wg_base_url = "https://www.wg-gesucht.de"
    
    def start_requests(self):
        """负责dump出最初的url
        """        
        # 第一个是wg-gesucht 1 zimmer ，第二个是 wg-gesucht wg
        urls = ["https://www.wg-gesucht.de/1-zimmer-wohnungen-in-Munchen.90.1.1.0.html?offer_filter=1&city_id=90&noDeact=1&categories%5B%5D=1&rent_types%5B%5D=0","https://www.wg-gesucht.de/wg-zimmer-in-Munchen.90.0.1.1.html?category=0&city_id=90&rent_type=0&noDeact=1&img=1&rent_types%5B0%5D=0",]
        
        for idx, url in enumerate(urls):
            if idx == 0: # 1 zimmer
                yield scrapy.Request(url=url, meta={'wohnung_type':"wg1"},callback=self.page_parse)
            if idx == 1: # wg
                yield scrapy.Request(url=url, meta={'wohnung_type':"wg"},callback=self.page_parse)
                
    def page_parse(self, response):
        """ yield pages
        """
        wohnung_type = response.meta.get("wohnung_type")
        if wohnung_type == "wg" or wohnung_type == "wg1":
            all_pages = response.css("ul.pagination.pagination-sm a")
            for page in all_pages[1:-1]:
                url = page.css("a::attr(href)").get()
                url = parse.urljoin(self.wg_base_url,url)
                yield scrapy.Request(url=url, meta={'wohnung_type':wohnung_type},callback=self.wohnung_parse)
        elif wohnung_type == "immo":
            pass
    
    def wohnung_parse(self,response):
        main_content = response.css("[id=main_column]")
        wohnungs = main_content.css("div.wgg_card.offer_list_item") 
         
        for item in wohnungs:
            
            wohnung = WohnungItem()
            # 类型
            wohnung_type = response.meta.get("wohnung_type")
            wohnung['wohnung_type'] = wohnung_type
            
            # 标题
            title = item.css("h3.truncate_title::attr(title)").get()
            wohnung['title'] = title
            
            # md5
            wohnung['md5'] = get_md5(title)
            
            # 网页链接
            url = item.css("h3.truncate_title a::attr(href)").get()
            wohnung['url'] = parse.urljoin(self.wg_base_url,url)
            
            # 总租金
            wohnung['gesamtmiete'] = item.css("div.row.noprint.middle div.col-xs-3 b::text").get()
            
            # Adresse
            adr = item.css("div.row.noprint div.col-xs-11 span::text").get().replace("\n","").replace("  ","")
            wohnung["adresse"] = adr
            
            # recording data
            crawltime = scrapy.Field()
            wohnung["crawltime"] = datetime.date.today()

            # time
            zeit = item.css("div.row.noprint.middle div.col-xs-5::text").get().strip().replace("\n", "").replace(" ","")
            wohnung["zeit"] = zeit
            
            yield wohnung
        
    # def wohnung_parse(self,response):
    #     """ 获取每个wohnung的链接
    #     """
    #     wohnung_type = response.meta.get("wohnung_type")
    #     if wohnung_type == "wg":
    #         all_wohnungs = response.css("h4.headline a.detailansicht::attr(href)").getall()
    #         for wohnung in all_wohnungs:
    #             url = parse.urljoin(self.wg_base_url,wohnung)
    #             yield scrapy.Request(url=url,meta={'wohnung_type':"wg"}, callback=self.parse)
    #     elif wohnung_type == "immo":
    #         pass
        
        
    # def parse(self,response):
        # wohnung = WohnungItem()
        
        # # 房子来源
        # wohnung_type = response.meta.get("wohnung_type")
        # wohnung['wohnung_type'] = wohnung_type
        
        # # 标题
        # title = response.css("h1.headline::text")[1].get().strip()
        # wohnung['title'] = title
        
        # # md5
        # wohnung['md5'] = get_md5(title)
        
        # # 网页链接
        # wohnung['url'] = response.url
        
        # # 总租金
        # wohnung['gesamtmiete'] = response.css("[id=graph_wrapper] div.basic_facts_bottom_part label.amount::text").get().strip()
        # # check 
        # # response.css("[id=graph_wrapper] div.basic_facts_bottom_part label.description::text").get().strip()
        
        # # Nebencost
        # nb = response.css("[id=graph_wrapper] [id=utilities_costs] label.graph_amount::text").get().strip()
        # wohnung["nebencost"] = None if nb == "n.a." else nb
        # # check
        # # response.css("[id=graph_wrapper] [id=utilities_costs] label.graph_description::text").get().strip()
        
        # # 押金
        # kaution = response.css("[id=provision_equipment_wrapper] div.provision-equipment")[0].css("label.amount::text").get().strip()
        # wohnung["kaution"] = kaution
        
        # # Adresse
        # adr = response.css("div.col-sm-4.mb10 a::text")[0].get().strip() + " " + response.css("div.col-sm-4.mb10 a::text")[1].get().strip()
        
        # # recording data
        # crawltime = scrapy.Field()
        # wohnung["crawltime"] = datetime.date.today()

        # # frei From
        # fromtime = response.css("div.col-sm-3 p b::text")[0].get()
        # wohnung["freiab"] = fromtime
        
        # # frei To
        # totime = response.css("div.col-sm-3 p b::text")[1].get()
        # wohnung["freizu"] = None if "Online" in totime else totime # if no frei zu zeit
        
        
        # yield wohnung
