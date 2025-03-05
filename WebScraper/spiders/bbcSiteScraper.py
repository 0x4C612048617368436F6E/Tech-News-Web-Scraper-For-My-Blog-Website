import scrapy
import json
from WebScraper.items import WebscraperItem
from newspaper import Article
import os

class bbcSiteScraper(scrapy.Spider):
    name = "bbcSiteScraper"
    start_urls = "https://www.bbc.co.uk/news/technology"
    allowed_domains = ["www.bbc.co.uk","bbc.co.uk"]
    scheme = "https://"
    NumOfNewsArticles = 3
    JSONFILELOCATION = "./subNewsArticleXPathParameters.json"
    
    @staticmethod
    def readJSONFile(path:str):
        #do some file checks
        if(not (os.path.exists(path))):
            print("File does not exist")
            exit(-1)
        with open(path,'r') as data:
            try:
                returnData = json.load(data)
            except Exception as e:
                print(e)
        return returnData

    #define start_request function
    def start_requests(self):
        print("Started")
        yield scrapy.Request(self.start_urls,callback=self.parse)

    #define parse function
    def parse(self,response):
        print("Starting parse")
        #process the information here
        #if response is None:
         #   print("response Object is empty")
          #  exit(-1)
        print("OKK====")
        parsedJSONFile = bbcSiteScraper.readJSONFile(self.JSONFILELOCATION)
        print(parsedJSONFile)
        #lets handle each page URL
        subNewsURL = response.xpath(f'//div[@class="{parsedJSONFile[0]['div5_class']}"]/a/@href').getall()
        for i in range(self.NumOfNewsArticles):
            #will read the JSON file and extract
            subNewsURLidx = subNewsURL[i]
            #check if we have anyhting
            if(len(subNewsURL) <= 0):
                print("Unable to get URL")
                exit(-1)

            print(self.scheme+self.allowed_domains[0]+subNewsURLidx)

            yield scrapy.Request(self.scheme+self.allowed_domains[0]+subNewsURLidx,callback=self.parseSubNewsPage)


    def parseSubNewsPage(self,res):
        #handle each sub news
        subNewsItem = WebscraperItem()
        subNewsItem['Title'] = res.xpath('//h1[@class="ssrcss-1s9pby4-Heading e10rt3ze0"]/span/text()').get()

        subNewsItem['DateAndTime'] = res.xpath('//span[@class="ssrcss-61mhsj-MetadataText e4wm5bw1"]/time/text()').get()

        '''
        Will be using the newspaper third part to extract the articles, as this is our only option
        '''
        article = Article(url="%s" %(res.url),language="en")
        article.download()
        article.parse()
        subNewsItem['ExtractedInformation'] = article.text

        yield subNewsItem