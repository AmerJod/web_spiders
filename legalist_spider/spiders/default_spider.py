from .spider import Spider


class DefaultQuotesSpider(Spider):
    """
        A spider that query the default page http://quotes.toscrape.com/'
        and retrieves all the quotes, authors and tags.
    """

    name = "default_quotes"
    base_url = "http://quotes.toscrape.com/"

    start_urls = [
        base_url,
    ]

    def parse(self, response):
        # Response is a selector obj
        # Select div tag with class quote
        for quote in response.css("div.quote"):

            #  Get the micro-data of the author
            author_href = quote.css("span a::attr(href)").get()

            quote_dict = {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("span small::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

            yield response.follow(
                author_href, callback=self.parse_author, cb_kwargs=quote_dict
            )

            # Find the next page anchor tag, then select the href
            next_page = response.css("li.next a::attr(href)").get()
            # Send a request to the next page if exist
            if next_page is not None:
                print(f"next_page: {next_page}")
                yield response.follow(next_page, callback=self.parse)


    def parse_author(self, response, **cb_kwargs):
        """ parse page """

        author_details_div = response.css("div.author-details")

        cb_kwargs["author_details"] = {
            "author_name": author_details_div.css("h3.author-title::text").get(),
            "date_of_birth": author_details_div.css(
                "p span.author-born-date::text"
            ).get(),
            "location": author_details_div.css(
                "p span.author-born-location::text"
            ).get(),
            "description": author_details_div.css("div.author-description::text").get(),
        }

        yield cb_kwargs
