from collections.abc import Iterable
from enum import Enum
from typing import Optional
from salesnext_crawler.crawler import ScrapyCrawler
from salesnext_crawler.events import CrawlEvent, Event, SitemapEvent
from scrapy import Request
import pyarrow as pa    
from boxil_crawler.parser.parse_service_category import parse_service_category
from boxil_crawler.parser.parse_sitemap import parse_sitemap

class CrawlType(str, Enum):
    CATEGORY = "CATEGORY"
    SITEMAP = "SITEMAP"


class BoxilCrawler(ScrapyCrawler):
    def __init__(self, daily: bool = False,
               crawl_type: list[CrawlType] = [
                   CrawlType.CATEGORY,
                   CrawlType.SITEMAP]) -> None:
        self.daily = daily
        self.crawl_type = crawl_type
        
    def start(self) -> Iterable[Event]:
        
        for crawl_type in self.crawl_type:
            if crawl_type == CrawlType.CATEGORY:
                url = "https://boxil.jp/categories/?via=si-categoryList-popularCategory"
                yield CrawlEvent(
                    request = Request(url),
                    metadata= None,
                    callback = parse_service_category
                )
            elif crawl_type == CrawlType.SITEMAP:
                yield SitemapEvent(
                    url = "https://boxil.jp/sitemap.xml",
                    metadata = None,
                    callback = parse_sitemap
                )
