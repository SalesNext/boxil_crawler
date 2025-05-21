from collections.abc import Iterable
from urllib.parse import urljoin
from boxil_crawler.schema.service import Service
from salesnext_crawler.events import CrawlEvent, Event, DataEvent
from scrapy.http.response.html import HtmlResponse
from scrapy import Request
import re
import json
from boxil_crawler.parser.parse_service_review import parse_service_review


def parse_service_rating(
    event: CrawlEvent[None, Event, HtmlResponse],
    response: HtmlResponse,
    
) -> Iterable[Event]:
    counts = []
    service_rating_count = response.xpath("//div[@class='serviceReputationMetricsBarBlock__count']")
    for rating in service_rating_count:
        rate = "".join(rating.xpath(".//text()").getall())
        if rate is None:
            rate = 0
        
        counts.append(rate)
    
    data = event.metadata["data"]
     
    data.source_review_url = response.url 
    data.review_average_rating = response.xpath("//div[@class='serviceReputationMetricsRateBlock']/text()").get()     
    data.review_5star_count = str(counts[0])
    data.review_4star_count = str(counts[1])
    data.review_3star_count = str(counts[2])
    data.review_2star_count = str(counts[3])
    data.review_1star_count = str(counts[4])

    data.review_from_1_10_employees_company_count = str(counts[5])
    data.review_from_11_30_employees_company_count = str(counts[6])
    data.review_from_31_100_employees_company_count = str(counts[7])
    data.review_from_101_500_employees_company_count = str(counts[8])
    data.review_from_above_500_employees_company_count = str(counts[9])
       
    scripts = response.xpath("//script/text()").getall()
    for script in scripts:
        if 'gon.reviewChart=' in script:
            match = re.search(r'gon\.reviewChart\s*=\s*(\{.*?\});', script, re.DOTALL)
            if match:
                json_str = match.group(1)
                json_data = json.loads(json_str)
                chart = json_data.get("service", {}).get("reviewAverageHash")                
                data.service_ease_of_use_rating = str(chart.get("ease_of_use"))
                data.service_usefulness_rating = str(chart.get("usefulness") or "")
                data.service_customize_rating = str(chart.get("customize") or "")
                data.service_functional_satisfaction_rating = str(chart.get("functional_satisfaction") or "")
                data.service_stability_rating = str(chart.get("service_stability") or "")
                data.service_impression_of_sales_staff_rating = str(chart.get("impression_of_sales_staff") or "")
                data.service_quality_of_support_rating = str(chart.get("quality_of_support") or "")
                data.service_of_initial_setup_rating = str(chart.get("ease_of_initial_setup") or "")
                data.service_adequacy_rating = str(chart.get("adequacy") or "")
               
    yield DataEvent("service", data)
   
    
   
                    