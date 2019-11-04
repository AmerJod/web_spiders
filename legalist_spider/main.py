import time

from apscheduler.schedulers.blocking import BlockingScheduler
from scrapy.crawler import CrawlerProcess

from spiders.default_spider import DefaultQuotesSpider
from spiders.infinite_scroll_spider import InfiniteScrollQuotesSpider
from spiders.javascript_spider import JavascriptQuotesSpider
from spiders.login_spider import LoginQuotesSpider
from spiders.table_spider import TableQuotesSpider

from legalist_spider import config

def run_spider(spider_name='scroll_quotes'):
    # Run without scheduler
    from scrapy import cmdline
    cmdline.execute(f"scrapy crawl {spider_name}".split())



def run_all_spiders():
    process_default = CrawlerProcess()
    # We assume that the default spider has to run first and finish before the other spiders run.
    process_default.crawl(DefaultQuotesSpider)
    process_default.start()
    time.sleep(120)
    # process_default.stop()

    process = CrawlerProcess()
    process.join()
    active_spiders = [
        TableQuotesSpider,
        JavascriptQuotesSpider,
        LoginQuotesSpider,
        InfiniteScrollQuotesSpider,
    ]
    for spider in active_spiders:
        process.crawl(spider)
    process.start()


# Scheduler the spiders
scheduler = BlockingScheduler()
scheduler.add_job(run_all_spiders, "cron", day="*", hour="11,23")

if __name__ == "__main__":
    if config.run_with_scheduler:
        scheduler.start()
    else:
        run_spider(config.spider_name)
