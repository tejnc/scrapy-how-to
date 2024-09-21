import logging
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import defer, reactor
from scrapy.utils.log import configure_logging


def launch_spider():

    @defer.inlineCallbacks
    def crawl():
        configure_logging() # needs to called explicitly when using CrawlRunner
        runner = CrawlerRunner(get_project_settings())
        yield runner.crawl('book-crawler')
        reactor.stop()

    crawl()
    reactor.run()

launch_spider()