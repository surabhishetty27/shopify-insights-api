from pydantic import BaseModel
from typing import List, Dict, Optional

class URLRequest(BaseModel):
    website_url: str

class BrandInsights(BaseModel):
    brand_name: Optional[str]
    product_catalog: List[Dict]
    hero_products: List[Dict]
    policies: Dict[str, str]
    faqs: List[Dict[str, str]]
    social_handles: Dict[str, str]
    contact: Dict[str, List[str]]
    about: Optional[str]
    important_links: Dict[str, str]
