from sqlalchemy.orm import Session
from models.db_models import Brand, Product, FAQ

def save_brand_data(db: Session, data: dict):
    # save brand
    brand = Brand(name=data.get("brand_name"), about=data.get("about"))
    db.add(brand)
    db.commit()
    db.refresh(brand)

    # save products
    for p in data.get("product_catalog", []):
        title = p.get("title") or p.get("name")
        if title:
            product = Product(title=title, brand_id=brand.id)
            db.add(product)

    # save FAQs
    for faq in data.get("faqs", []):
        if faq.get("question") and faq.get("answer"):
            faq_entry = FAQ(
                question=faq.get("question"),
                answer=faq.get("answer"),
                brand_id=brand.id
            )
            db.add(faq_entry)

    db.commit()
