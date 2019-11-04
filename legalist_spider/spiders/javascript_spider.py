import re
from .spider import Spider


class JavascriptQuotesSpider(Spider):
    """
         A spider that query the javascript page http://quotes.toscrape.com/js'
         and retrieves all the quotes, authors and tags.
    """

    #  URL query: "http://quotes.toscrape.com/js/page/NUMBER/"
    name = "js_quotes"
    base_url = "http://quotes.toscrape.com/js/page/%s/"
    page = 1

    # Construct the initial URL query
    start_urls = [
        base_url % page,
    ]

    def parse(self, response):
        # Response body is an HTML that includes js to
        # Render the quotes into the HTML
        js_text = response.selector.xpath("//script").getall()[1].replace("\n", "")
        # Remove any instance of two spaces or more
        js_text = re.sub("\s\s+", "", js_text)

        # Regular Expressions to extract the tags, authors, and texts
        # From the JSON obj
        tags_pattern = '"tags": \[.*?\]'
        author_pattern = '"name": ".*?"'
        text_pattern = '"text": ".*?"'

        # Extract the tags, authors, and texts
        tags_list = re.findall(tags_pattern, js_text)
        authors_list = re.findall(author_pattern, js_text)
        texts_list = re.findall(text_pattern, js_text)

        # To use the same pipeline we need to yield each item individually
        list_of_dicts = []

        for i in range(len(authors_list)):
            tags = tags_list[i]
            author = authors_list[i]
            text = texts_list[i]

            author = author.split(": ")[1]
            text = text.split(": ")[1]

            list_of_dicts.append({"text": text, "author": author, "tags": tags})

        # yield each item individually
        for info_dict in list_of_dicts:
            yield info_dict

        # Find the next page anchor tag, then select the href
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            self.page += 1
            yield response.follow(self.base_url % self.page, callback=self.parse)
