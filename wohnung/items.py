# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WohnungItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    # 标题
    title = scrapy.Field()
    
    # 网页链接
    wohnungurl = scrapy.Field()
    
    # 总租金
    gesamtmiete = scrapy.Field()
    
    # 押金
    kaution = scrapy.Field()
    
    # Adresse
    adresse = scrapy.Field()
    
    # frei From
    freiab = scrapy.Field()
    
    # frei To
    freizu = scrapy.Field()