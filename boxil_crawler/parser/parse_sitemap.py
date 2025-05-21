from collections.abc import Iterable
from typing import TypedDict
from boxil_crawler.parser.parse_service_detail import parse_service_detail
from boxil_crawler.parser.parse_service_rating import parse_service_rating
from salesnext_crawler.events import CrawlEvent, Event, SitemapEvent
from scrapy import Request

import re

def search_string(pattern: str, text: str) -> str:
    result = re.search(pattern, text)
    if result:
        return result.group()
    return ""

def parse_sitemap(event: SitemapEvent[None, Event], url: str) -> Iterable[Event]:
    if "?categoryId=" in url:
        service_id = search_string(r"(\d+)", url)
        if service_id:
            yield CrawlEvent(
                request=Request(url),
                metadata=None,
                callback=parse_service_detail,
            )
   