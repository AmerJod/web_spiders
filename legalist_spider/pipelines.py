# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import datetime

# Load modules from the common lib
from spiderlib.db.database import Database
from spiderlib.db.db_modules.tag import Tag
from spiderlib.db.db_modules.author import Author
from spiderlib.db.db_modules.quote import Quote

from . import config
import re


class CleanDataPipeline(object):
    """ Clean the data """

    def process_item(self, item, spider):
        # list_obj = []
        author_details = item.get("author_details")

        # Could use a list of
        if author_details:
            author_details["author_name"] = author_details.get("author_name").strip()
            author_details["date_of_birth"] = author_details.get("date_of_birth").strip()

            # Get city and Country
            location = author_details.get("location", "").strip()
            location = re.sub("in\s", "", location)
            locations_list = location.split(",")
            author_details["city"] = ', '.join(locations_list[:-1]).strip()
            author_details["country"] = locations_list[-1].strip()
            author_details["description"] = author_details.get("description").strip()

            item["author_details"] = author_details


        item["author"] = item.get("author").strip()
        # TODO: Risky, might through an error
        item["text"] = re.findall('“(.*?)”', item.get("text"))[0]
        item["tags"] = item.get("tags")

        return item


class JsonWriterPipeline(object):
    """ JSON Writer - write JSON in file """

    def open_spider(self, spider):
        dt = str(datetime.datetime.now())
        file_name = "quotes_" + dt + ".json"
        self.file = open(f"{file_name}", "w+")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(item) + "\n"
        self.file.write(line)
        return item


class DatabaseWriterPipeline(object):
    """ Write into the database """

    conn = None
    dict_authors = {}
    dict_tags = {}

    def process_item(self, item, spider):
        # Check if the Author Details if it has data
        author_details = item.get("author_details")
        if author_details:
            author_name = author_details.get("author_name")
            date_of_birth = author_details.get("date_of_birth")
            city = author_details.get("city")
            country = author_details.get("country")
            description = author_details.get("description")

            # check if the author is in the db
            author_obj = self.conn.query_one(Author, author_name=author_name)
            if not author_obj:
                # If not exist add it and get the obj
                author_obj = Author(
                    author_name=author_name,
                    date_of_birth=date_of_birth,
                    city=city,
                    country=country,
                    description=description,
                )

                author_id = self.conn.add(author_obj).author_id
                self.dict_authors[author_name] = author_id

        # Get the quote data
        author = item.get("author")
        quote = item.get("text")
        tags = item.get("tags")

        # Using simple caching mechanism - dict
        # Check if it is in the cache
        author_id = self.dict_authors.get(author)

        if not author_id:
            # Check if the author is already exist in the db
            author_obj = self.conn.query_one(Author, author_name=author)

            if not author_obj:
                # If not exist add it and get the obj
                author_db = Author(author_name=author)
                author_id = self.conn.add(author_db).author_id
            else:
                author_id = author_obj.author_id

            # Add it to the cache: kks
            self.dict_authors[author] = author_id

        # TODO: check if the quote has any updates in regards to the tags - FUTURE WORK
        # Check it the quote is already in the db
        # We can do smart cashing using the dict
        quote_obj = self.conn.query_one(Quote, text=quote)
        if not quote_obj:
            # If not exist add it and return the obj
            quote_obj = Quote(text=quote, author_id=author_id)

            for _tag in tags:
                tag_obj = self.conn.query_one(Tag, tag=_tag)
                if not tag_obj:
                    tag_obj = Tag(tag=_tag)

                quote_obj.tags.append(tag_obj)

            # Add the Quote object
            self.conn.add(quote_obj)

    def open_spider(self, spider):
        self.conn = Database(**config.POSTGRES_CONN)

    def close_spider(self, spider):
        self.conn._session.close()
