from .spider import Spider
from scrapy.http import FormRequest


class LoginQuotesSpider(Spider):
    """
        A spider that query the page http://quotes.toscrape.com/ after login'
        and retrieves all the quotes, authors and tags.
    """

    name = "login_quotes"
    base_url = "http://quotes.toscrape.com/login"

    start_urls = [
        base_url,
    ]

    def parse(self, response):
        # Get the csrf_token from the form
        token = response.css("form input::attr(value)").extract_first()

        return FormRequest.from_response(
            response,
            formdata={"csrf_token": token, "password": "amer", "username": "amer"},
            callback=self.scrape_pages,
        )

    def scrape_pages(self, response):

        for quote in response.css("div.quote"):

            quote_dict = {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("span small::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

            yield quote_dict

            # Find the next page anchor tag, then select the href
            next_page = response.css("li.next a::attr(href)").get()
            # Send a request to the next page if exist
            if next_page is not None:
                yield response.follow(next_page, callback=self.scrape_pages)
