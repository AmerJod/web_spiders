
import time

from apscheduler.schedulers.blocking import BlockingScheduler

from scrapy.crawler import CrawlerProcess

# from spiders import TableQuotesSpider, JavascriptQuotesSpider, DefaultQuotesSpider, LoginQuotesSpider


from spiders.default_spider import DefaultQuotesSpider
from spiders.infinite_scroll_spider import InfiniteScrollQuotesSpider
from spiders.javascript_spider import JavascriptQuotesSpider
from spiders.login_spider import LoginQuotesSpider
from spiders.table_spider import TableQuotesSpider

def run_all_spiders():
    process_default = CrawlerProcess()
    # We assume that the default spider has to run first and finish before the other spiders run.
    process_default.crawl(DefaultQuotesSpider)
    process_default.start()
    time.sleep(120)
    process_default.stop()


    process = CrawlerProcess()
    active_spiders = [TableQuotesSpider, JavascriptQuotesSpider, LoginQuotesSpider, InfiniteScrollQuotesSpider]
    for spider in active_spiders:
        process.crawl(spider)
    process.start()


# Scheduler the spiders
scheduler = BlockingScheduler()
scheduler.add_job(run_all_spiders, 'cron', day="*", hour='11,23')

if __name__ == '__main__':
    scheduler.start()