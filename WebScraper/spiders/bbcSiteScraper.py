import scrapy

class bbcSiteScraper(scrapy.Spider):
    name = "bbcSiteScraper"
    start_urls = "https://www.bbc.co.uk/news/technology"
    allowed_domains = ["www.bbc.co.uk"]
    NumOfNewsArticles = 3
    

    #define start_request function
    def start_requests(self):
        yield scrapy.Request(self.start_urls,callback=self.parse)

    #define parse function
    def parse(self,response):
        #process the information here
        if response is None:
            print("response Object is empty")
            exit(-1)
        #lets handle each page URL
        for i in self.NumOfNewsArticles:
            #will read the JSON file and extract
            pass

    def parseSubNewsPage(self,res):
        #handle each sub news
        pass