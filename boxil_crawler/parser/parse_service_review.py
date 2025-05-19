from collections.abc import Iterable
from urllib.parse import urljoin
from boxil_crawler.schema.review import Review
from salesnext_crawler.events import CrawlEvent, Event, DataEvent
from scrapy.http.response.html import HtmlResponse
from scrapy import Request



def parse_service_review(
    event: CrawlEvent[None, Event, HtmlResponse],
    response: HtmlResponse,
    
) -> Iterable[Event]:
    
    next_page = response.xpath("//a[@title='next_page']/@href").get()
    next_page = urljoin(response.url, next_page)
    
    reviews = response.xpath("//div[@class='reputationAnswerItemWrap']")
    for review in reviews:
        data = Review()
        data.reviewer_name = review.xpath(".//div[@class='reputationAnswerItemTopRightItemBaseInfoBlock__username']/text()").get()
        data.reviewer_role = review.xpath(".//div[@class='reputationAnswerItemTopRightItemBaseInfoBlock__position']/text()").get()
        data.reviewer_type_of_business = review.xpath(".//div[@class='reputationAnswerItemTopRightItemBlock__typeOfBusiness']/text()").get()
        data.reviewer_usage_status = review.xpath(".//div[@class='reputationAnswerItemTopRightItemBlock__usageStatus']/text()").get().replace("利用状況：","")
        data.reviewer_number_range_of_user_account = review.xpath(".//div[@class='reputationAnswerItemTopRightItemBlock__separator__numberRangeOfUserAccount']/text()").get().replace("利用アカウント数：","")
        data.reviewer_posted_at = review.xpath(".//div[@class='reputationAnswerItemTopRightItemBlock'][contains(.,'投稿日：')]/text()").get().replace("投稿日：","")
        data.reviewer_rating_score = review.xpath(".//span[@class='reputationAnswerItemStatusScoreBlock__scoreNum']/text()").get()
        data.reviewer_status_tags = review.xpath(".//div[@class='reputationAnswerItemStatusTagBlock__text']/text()").getall()
        data.review_title = review.xpath(".//div[@class='reputationAnswerItemBasicBlock__title']/a/text()").get()
        data.review_url = review.xpath(".//div[@class='reputationAnswerItemBasicBlock__title']/a/@href").get()
        data.review_id =  data.review_url.split("/")[-2]
        data.service_review_id = data.review_url.split("/")[-4]
        data.review_description = review.xpath(".//div[@class='reputationAnswerItemBasicBlock__description']/text()").get()
        data.review_content = review.xpath(".//div[@class='reputationAnswerItemFirstQuestionBlock__answer']/text()").get()
        data.review_good_point = review.xpath(".//div[@class='reputationAnswerGoodPointsBlock__text']/text()").getall()
        data.review_good_point_count = len( data.review_good_point)
        data.review_bad_point = review.xpath(".//div[@class='reputationAnswerBadPointsBlock__text']/text()").getall()
        data.review_bad_point_count = len( data.review_bad_point)
        yield DataEvent("review", data) 
        
    print(data)    
     
    yield DataEvent("review", data)   
    
    yield CrawlEvent(
        request=Request(next_page),
        metadata=None,
        callback=parse_service_review,
    )