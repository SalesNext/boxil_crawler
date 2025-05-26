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
        
        crawled_service_ids = []
        crawled_company_ids = []
        if self.daily:
            crawled_service_table : pa.Table = self.readers["service"].read()
            crawled_service_ids = crawled_service_table.select(["service_id"]).drop_null().to_pydict()["service_id"]
            crawled_service_ids = list(crawled_service_ids)
            
            crawled_company_table : pa.Table = self.readers["company"].read()
            crawled_company_ids = crawled_company_table.select(["company_id"]).drop_null().to_pydict()["company_id"]
            crawled_company_ids = list(crawled_company_ids) 
       
        
        for crawl_type in self.crawl_type:
            if crawl_type == CrawlType.CATEGORY:
                url = "https://boxil.jp/categories/?via=si-categoryList-popularCategory"
                yield CrawlEvent(
                    request = Request(url),
                    metadata= {"crawled_company_ids": crawled_company_ids, "crawled_service_ids": crawled_service_ids},
                    callback = parse_service_category
                )
            elif crawl_type == CrawlType.SITEMAP:
                yield SitemapEvent(
                    url = "https://boxil.jp/sitemap.xml",
                    metadata = {"crawled_company_ids": crawled_company_ids, "crawled_service_ids": crawled_service_ids},
                    callback = parse_sitemap
                )
