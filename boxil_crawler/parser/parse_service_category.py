from collections.abc import Iterable

from salesnext_crawler.events import CrawlEvent, DataEvent, Event
from scrapy.http.response.html import HtmlResponse
from scrapy import Request
import re
from pydantic import BaseModel

from boxil_crawler.parser.parse_service_list import parse_service_list




def parse_service_category(
    event: CrawlEvent[None, Event, HtmlResponse],
    response: HtmlResponse,
    
) -> Iterable[Event]:
    categories = response.xpath("//a[@class='Label_sm__nzecC CategoryList_category__nOn1f']/@href").getall()
    for category in categories:
        url = f'https://boxil.jp{category}'
        yield CrawlEvent(
            request=Request(url),
            metadata=event.metadata,
            callback=parse_service_list,
        )
    