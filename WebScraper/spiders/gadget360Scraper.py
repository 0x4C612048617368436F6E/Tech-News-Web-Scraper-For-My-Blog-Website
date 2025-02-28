import scrapy
import json
from WebScraper.items import WebscraperItem
from newspaper import Article

class gadget360Scraper(scrapy.Spider):
    name = "gadget360Scraper"
    start_urls = "https://www.gadgets360.com/artificial-intelligence#pfrom=topnav_desk"
    allowed_domains = ["www.gadgets360.com"]
    scheme = "https://"
    NumOfNewsArticles = 3
    JSONFILELOCATION = "../subNewsArticleXPathParameters.json"
    
    #define start_request function
    def start_requests(self):
        yield scrapy.Request(self.start_urls,callback=self.parse)
    
    #define parse function
    def parse(self,response):
        #process the information here
        if response is None:
            print("response Object is empty")
            exit(-1)

        #get the link
        subNewsURL = response.xpath('//div[@class="nlist bigimglist stories"]/ul/li/a/@href').getall()
        for i in range(self.NumOfNewsArticles):
            if(len(subNewsURL[i]) <=0):
                print("Unable to get link")
                exit(-1)
            yield scrapy.Request(subNewsURL[i],callback=self.parseSubNewsPage)

    def parseSubNewsPage(self,res):
        #handle each sub news
        subNewsItem = WebscraperItem()
        subNewsItem['Title'] = res.xpath('//div[@class="lead_heading header_wrap"]/h1/text()').get()

        subNewsItem['DateAndTime'] = res.xpath('//div[@class="dateline"]/span[@class="value-title"]/@title').get()

        '''
        Will be using the newspaper third part to extract the articles, as this is our only option
        '''
        article = Article(url="%s" %(res.url),language="en")
        article.download()
        article.parse()
        subNewsItem['ExtractedInformation'] = article.text

        yield subNewsItem