import scrapy


class CoronavirusSpider(scrapy.Spider):
    name = "coronavirus"
    allowed_domains = ["www.worldometers.info"]
    # start_urls = ["https://www.worldometers.info/coronavirus"]
    
    #extra-----------------------------------------------------
    start_link = 'https://www.worldometers.info/coronavirus'
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    }
    def start_requests(self):
        yield scrapy.Request(url=self.start_link, callback=self.parse,headers=self.header)
    
    
    
    #extra-----------------------------------------------------
    def parse(self, response):
        for country in (response.xpath("//td/a[contains(@class, 'mt_a')]")):
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()
            # absolute_url = f"https://www.worldometers.info/coronavirus/{link}"
            # absolute_url = response.urljoin(link)
            if link:
                yield response.follow(url=link,callback=self.page2parser,meta= {'country-name':name},headers=self.header)
            
            
    def page2parser(self, response):
        country_name = response.request.meta['country-name']
        activeCases = response.xpath("(//div[contains(@class, 'maincounter-number')])[1]/span/text()").get()
        death = response.xpath(" (//div[contains(@class, 'maincounter-number')])[2]/span/text()").get()
        recoreved = response.xpath(" (//div[contains(@class, 'maincounter-number')])[3]/span/text()").get()
        
        yield{
            'name' :country_name,           #conecpt of meta to use variable of other functions
            'active_cases':activeCases,
            'death':death,
            'recovered' :recoreved
        }
            # yield{
            #     'country_name': name,
            #     'country_link': absolute_url
            # }
        # link = response.xpath("(//td/a)[1]/@href").get()
        # name = response.xpath("(//td/a)[1]/text()").get()
        #response.xpath("(//td/a)[1]/text()")

        # yield{ #to print something we use yield
        #     'country name' :name,
        #     'link' :link
        # }