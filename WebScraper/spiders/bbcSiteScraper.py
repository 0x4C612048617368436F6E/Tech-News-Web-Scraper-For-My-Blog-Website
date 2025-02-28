import scrapy
import json
from WebScraper.items import WebscraperItem
from newspaper import Article

class bbcSiteScraper(scrapy.Spider):
    name = "bbcSiteScraper"
    start_urls = "https://www.bbc.co.uk/news/technology"
    allowed_domains = ["www.bbc.co.uk"]
    scheme = "https://"
    NumOfNewsArticles = 3
    JSONFILELOCATION = "../subNewsArticleXPathParameters.json"
    
    @staticmethod
    def readJSONFile(path:str):
        with open(path,'r') as data:
            try:
                returnData = json.load(data)
            except Exception as e:
                print(e)
        return returnData

    #define start_request function
    def start_requests(self):
        yield scrapy.Request(self.start_urls,callback=self.parse)

    #define parse function
    def parse(self,response):
        #process the information here
        if response is None:
            print("response Object is empty")
            exit(-1)
        parsedJSONFile = bbcSiteScraper.readJSONFile(self.JSONFILELOCATION)

        #lets handle each page URL
        for i in range(self.NumOfNewsArticles):
            #will read the JSON file and extract
            subNewsURL = response.xpath(f'//li[@class="{parsedJSONFile[i]['li_class']}"]/div[@class="{parsedJSONFile[i]['div1_class']}"]/div[@class="{parsedJSONFile[i]['div2_class']}"]/div[@class="{parsedJSONFile[i]['div3_class']}"]/div[@class="{parsedJSONFile[i]['div4_class']}"]/div[@class="{parsedJSONFile[i]['div5_class']}"]/a[@class="{parsedJSONFile[i]['a_class']}"]/@href').get()
            #check if we have anyhting
            if(len(subNewsURL) <= 0):
                print("Unable to get URL")
                exit(-1)

            yield scrapy.Request(self.scheme+self.allowed_domains[0]+subNewsURL,callback=self.parseSubNewsPage)


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