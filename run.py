from scrapy import cmdline
import datetime
time = datetime.datetime.now().strftime('%Y_%m_%d')

cmdline.execute(['scrapy', 'crawl','price','-O','dataset/'+time+'.json',])
cmdline.execute(['cp','dataset/'+time+'.json','dataset/latest.json',])
