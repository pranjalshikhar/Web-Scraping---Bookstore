import scrapy
import pandas as pd


class books(scrapy.Spider):
    name = "books"

    def start_requests(self):
        urls = [
            'http://books.toscrape.com/catalogue/page-1.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        
        # For Creating JSON        

        for q in response.css("article.product_pod"):
            img = q.css("img.thumbnail::attr(src)").get()
            name = q.css("h3 a::attr(title)").get()
            price = q.css("p.price_color::text").get()
            
            
            yield {
                "img" : img,
                "name" : name,
                "price" : price
            }
        
        # For Recursive Crawling

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
            
            
            
            
js = pd.read_json(r'books.json')
df = js.to_csv(r'books.csv', index=None, header=True)