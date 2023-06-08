import scrapy

class LinkSpider(scrapy.Spider):
    name = 'linkspider'

    def start_requests(self):
        # Prompt the user to input the website address
        address = input("Enter the website address: ")
        yield scrapy.Request(url=address, callback=self.parse)

    def parse(self, response):
        # Extract all links on the page
        links = response.css('a::attr(href)').getall()

        for link in links:
            yield response.follow(link, callback=self.parse_link)

    def parse_link(self, response):
        # Check if the link is broken (e.g., 404 status code)
        if response.status == 404:
            yield {
                'url': response.url,
                'status': response.status,
            }
