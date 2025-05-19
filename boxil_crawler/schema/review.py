from pydantic import BaseModel
from typing import Optional, List

class Review(BaseModel):
    review_service_id: Optional[str] = None
    reviewer_name: Optional[str] = None
    reviewer_role: Optional[str] = None
    reviewer_type_of_business: Optional[str] = None
    reviewer_usage_status: Optional[str] = None
    reviewer_number_range_of_user_account: Optional[str] = None
    reviewer_posted_at: Optional[str] = None
    reviewer_rating_score: Optional[str] = None
    reviewer_status_tags: Optional[List[str]] = None
    review_title: Optional[str] = None
    review_url: Optional[str] = None
    review_description: Optional[str] = None
    review_content: Optional[str] = None
    review_good_point: Optional[List[str]] = None
    review_good_point_count: Optional[int] = None
    review_bad_point: Optional[List[str]] = None
    review_bad_point_count: Optional[int] = None