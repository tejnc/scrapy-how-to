import scrapy


class BookCrawler(scrapy.Spider):
    name = 'book-crawler'

    def start_requests(self):
        self.start_url = 'https://books.toscrape.com'
        yield scrapy.Request(
            url=self.start_url,
            callback=self.parse,
        )

    def parse(self, response):
        books = response.xpath("//article[@class='product_pod']")
        for book in books:
            title = book.xpath('./h3/a/text()').get()
            price = book.xpath('./div[@class="product_price"]/p[@class="price_color"]/text()').get()
            availability = book.xpath('./div[@class="product_price"]/p[@class="instock availability"]/text()').get()
            image_src = book.xpath('./div[@class="image_container"]/a/img/@src').get()

            yield {
                'title': title,
                'price': price,
                'availability': availability,
                'image_src': image_src,
            }

        next_page = response.xpath('//a[text()="next"]/@href').get()
        if next_page is not None:
            next_url = 'https://books.toscrape.com/'  + next_page if next_page.__contains__('catalogue') else 'https://books.toscrape.com/' + 'catalogue/' + next_page
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
            )
