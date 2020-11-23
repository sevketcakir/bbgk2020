import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css(".text::text").getall()
        by = response.css(".author::text").getall()
        for q,b in zip(quotes, by):
            d = {
                "quote": q,
                "by": b
            }
            yield d
        url = response.css('.next a::attr(href)').get()
        if url is not None:
            yield response.follow(url, callback=self.parse)
