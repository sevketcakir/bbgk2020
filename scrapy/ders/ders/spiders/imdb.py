import scrapy


class ImdbSpider(scrapy.Spider):
    name = 'imdb'
    allowed_domains = ['www.imdb.com']
    start_urls = ['http://www.imdb.com/chart/top/']

    def parse(self, response):
        urls = response.css(".titleColumn a::attr(href)").getall()
        for url in urls:
            yield response.follow(url, callback=self.parse_movie)

    def parse_movie(self, response):
        #rating: strong span
        #year: #titleYear a
        #director: .ready+ .credit_summary_item a
        #storyline: p span
        cast = response.css('.cast_list a::text').getall()
        d = {
            "title": response.css('h1::text').get()[:-1],
            "cast": str(list(zip(cast[::2], cast[1::2]))),
            "rating": response.css('strong span::text').get(),
            "year": response.css('#titleYear a::text').get(),
            "director": response.css('.ready+ .credit_summary_item a').get(),
            "storyline": response.css('p span::text').get()
        }
        yield d


