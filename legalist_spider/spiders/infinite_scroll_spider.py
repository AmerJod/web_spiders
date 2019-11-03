import scrapy
import json
from .spider import Spider


class InfiniteScrollQuotesSpider(Spider):
    """
          A spider that query the infinite scroll page http://quotes.toscrape.com/scroll'
          and retrieves all the quotes, authors and tags.
    """

    # API URL: "http://quotes.toscrape.com/api/quotes?page=NUMBER"
    name = "scroll_quotes"
    base_url = "http://quotes.toscrape.com/api/quotes?page=%s"
    page = 1

    # Construct the initial api query
    start_urls = [
        base_url % page,
    ]

    def parse(self, response):
        # Response.body is a JSON obj as string
        response_body = response.body
        data = json.loads(response_body)
        quotes = data["quotes"]

        # For each quote select the text, author, and tags.
        for quote in quotes:
            info_dict = {
                "text": quote["text"],
                "author": quote["author"]["name"],
                "tags": quote["tags"],
            }

            yield info_dict

        # Check if there are more pages to query
        # And query the next page if exist
        if data["has_next"]:
            self.page += 1
            yield response.follow(self.base_url % self.page, callback=self.parse)
