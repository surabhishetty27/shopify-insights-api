from fastapi import APIRouter, HTTPException
from models.schemas import URLRequest, BrandInsights
from services.scraper import get_shopify_insights

router = APIRouter()

@router.post("/fetch-insights", response_model=BrandInsights)
def fetch_insights(request: URLRequest):
    try:
        data = get_shopify_insights(request.website_url)
        if not data:
            raise HTTPException(status_code=401, detail="Website not found or invalid")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
