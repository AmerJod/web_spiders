- Author:   Amer Joudiah
- Date:     3/11/2019

``Web Spiders``: A simple demo project (web spiders) :)
=================================================================

A spider crawling project (MVP version),...

This project contains five web spiders that are used to scrape data from the http://quotes.toscrape.com website.

Additionally, pipelines have been developed to clean the data before writing it into JSON files or a database.

.......

Spiders Included:
=================

1.  ``Default Spider``:
        -    The default spider is used to scrape quote data (author, text, and tags) as well as microdata for each author of each quote, including: the author's name, the author's birth date, the author's birthplace, and a description of the author
             This spider simply scrapes the static HTML displayed upon a page request. Then, the scraper goes to the next page by scraping the anchor tag href for the 'Next' button and continues to scrape quotes.

2.  ``Infinite Scroll Spider``:
        -    The infinite scroll spider is used to scrape quote data (author, text, and tags). Since the quotes are loaded upon scroll, we cannot simply scrape the HTML. Therefor, we simulate an API request that is sent out upon scrolling to get the quotes. We get the API endpiont by inspecting the browser's network tab and observing the requests leaving the browser.
             This API call 'http://quotes.toscrape.com/api/quotes?page=NUMBER'.  By simulating this request to the API for each page number, JSON objects for the quotes can be obtained.

3.  ``javascript spider``:
        -    The javascript spider is used to scrape quote data (author, text, and tags). The quotes are rendered in by the JavaScript into HTML after the initial access to the webpage. This means that if a request to the webpage is sent, the returned HTML data is before the quotes have been loaded into the webpage. However, the quote data is stored within the JavaScript file. Quote data is then scraped from the JavaScript file using regular expressions.

4.  ``Login spider``:
        -   The login spider is used to scrape quote data (author, text, and tags).....cd

5.  ``Tableful Spider``:
        -   The login spider is used to scrape quote data (author, text, and tags). The quotes are stored into a html table.

6.  ``Random Spider``:
        - TODO

7.  ``Ajax Spider``:
        - TODO