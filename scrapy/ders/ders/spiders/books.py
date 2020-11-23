import scrapy
# .product_pod a
# .next a
#kitap ismi: h1
#kitap fiyatı: .product_main .price_color
#adet: .product_main .availability
#açıklama: #product_description+ p
#kategori: .breadcrumb li~ li+ li a

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        urls = response.css('.product_pod a::attr(href)').getall()
        for url in urls:
            yield response.follow(url, callback=self.parse_book)

        next = response.css('.next a::attr(href)').get()
        if next is not None:
            yield response.follow(next, callback=self.parse)

    def parse_book(self, response):
        d = {
            "title": response.css("h1::text").get(),
            "price": response.css(".product_main .price_color::text").get(),
            "quantity": response.css(".product_main .availability::text").get(),
            "description": response.css("#product_description+ p::text").get(),
            "category": response.css(".breadcrumb li~ li+ li a::text").get(),
        }
        yield d
