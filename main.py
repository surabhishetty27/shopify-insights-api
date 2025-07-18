from fastapi import FastAPI
from routes.insights import router as insights_router
from database import Base, engine
from models import db_models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shopify Store Insights Fetcher")
app.include_router(insights_router, prefix="/api")


