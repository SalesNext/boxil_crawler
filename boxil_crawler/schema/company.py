from pydantic import BaseModel
from typing import Optional


class Company(BaseModel):
    company_id: Optional[str] = None
    company_name: Optional[str] = None
    company_industry: Optional[str] = None
    company_large_industry: Optional[str] = None
    company_medium_industry: Optional[str] = None
    company_small_industry: Optional[str] = None
    company_address: Optional[str] = None
    company: Optional[str] = None
    