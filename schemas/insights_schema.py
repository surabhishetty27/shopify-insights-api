from pydantic import BaseModel

class ProductCreate(BaseModel):
    title: str
    price: str
    url: str
