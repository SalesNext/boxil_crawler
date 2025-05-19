from collections.abc import Iterable
from enum import Enum
from typing import Optional
from salesnext_crawler.crawler import ScrapyCrawler
from salesnext_crawler.events import CrawlEvent, Event, SitemapEvent
from scrapy import Request
import pyarrow as pa    
from boxil_crawler.parser.parse_service_category import parse_service_category



class BoxilCrawler(ScrapyCrawler):
    def __init(self, daily: bool = False) -> None:
        self.daily = daily
        
        
    def start(self) -> Iterable[Event]:
        
        url = "https://boxil.jp/categories/?via=si-categoryList-popularCategory"
        yield CrawlEvent(
            request = Request(url),
            metadata= None,
            callback = parse_service_category
        )
