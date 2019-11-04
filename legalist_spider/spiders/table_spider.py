from .spider import Spider


class TableQuotesSpider(Spider):
    """
        A spider that query the table page http://quotes.toscrape.com/tableful/'
        and retrieves all the quotes, authors and tags.
    """

    name = "table_quotes"
    base_url = "http://quotes.toscrape.com/tableful"

    start_urls = [
        base_url,
    ]

    def parse(self, response):

        # First row and last row are blank
        table_rows = response.css("tr")[1:]
        quotes_table_rows = table_rows[:-1]

        # Go through all the tables rows (tr)
        for i, tr in enumerate(quotes_table_rows):
            # Every even row will be a text and author
            if i % 2 == 0:
                # Text and author are in the same table column (td)
                # need to split them
                text_and_author = tr.css("td::text").get()
                text_and_author = text_and_author.split(" Author: ")

                text = text_and_author[0]
                author = text_and_author[1]

            # Every odd row will be tags
            else:
                tags = tr.css("a::text").getall()

                info_dict = {"text": text, "author": author, "tags": tags}

                # Yield only in the odd iteration
                yield info_dict

        # Find the next page anchor tag, then select the href
        # B check if the last two td tags contain the word 'Next'
        for text in table_rows[-1].css("td a::text").getall():
            if "Next" in text:
                next_page = table_rows[-1].css("td a::attr(href)").getall()[-1]
                # Send a request to the next page if exist
                if next_page is not None:
                    yield response.follow(next_page, callback=self.parse)
