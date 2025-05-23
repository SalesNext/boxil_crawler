from collections.abc import Iterable
from urllib.parse import urljoin
from boxil_crawler.parser.parse_service_detail import parse_service_detail
from salesnext_crawler.events import CrawlEvent, Event
from scrapy.http.response.html import HtmlResponse
from scrapy import Request
import re


def parse_service_list(
    event: CrawlEvent[None, Event, HtmlResponse],
    response: HtmlResponse,
    
) -> Iterable[Event]:
    service_urls = response.xpath("//a/@href").getall()
    service = []
    review = []
    for url in service_urls:
        if '/service/' in url and '/reviews' not in url:
            service.append(url)
        if '/reviews/' in url:
            review.append(url)
    service = list(set(service))
    review = list(set(review))
    next_page = response.xpath("//a[@class='Pagination_control__ChC_H']/@href").get()
    
    if next_page:
        for page in next_page:
            yield CrawlEvent(
                request=Request(f"{response.url}/{page}"),
                metadata=None,
                callback=parse_service_list,
            )
    for url in service:
        yield CrawlEvent(
            request=Request(urljoin(response.url, url)),
            metadata=None,
            callback=parse_service_detail,
        )
    