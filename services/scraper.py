import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_shopify_insights(base_url: str):
    # URL
    if not base_url.startswith("http"):
        base_url = "https://" + base_url.strip("/")

    response = requests.get(base_url)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, "lxml")

    # Product Catalog from /products.json
    try:
        product_json = requests.get(urljoin(base_url, "/products.json")).json()
        products = product_json.get("products", [])
    except:
        products = []

    # homepage
    hero = soup.select(".product-card, .product")[:3]
    hero_products = [{"title": h.get_text(strip=True)} for h in hero]

    # routes
    policies = {}
    for ptype in ["privacy-policy", "refund-policy"]:
        try:
            policy_url = urljoin(base_url, f"/policies/{ptype}")
            ptext = requests.get(policy_url).text
            policies[ptype.split("-")[0]] = BeautifulSoup(ptext, "lxml").get_text()
        except:
            policies[ptype.split("-")[0]] = ""

    # FAQs 
    faqs = []
    for a in soup.find_all("a", href=True):
        if "faq" in a["href"].lower() or "help" in a["href"].lower():
            faq_url = urljoin(base_url, a["href"])
            try:
                faq_page = requests.get(faq_url).text
                faq_soup = BeautifulSoup(faq_page, "lxml")
                faqs.extend([
                    {"question": q.get_text(), "answer": a.get_text()}
                    for q, a in zip(faq_soup.find_all("h2"), faq_soup.find_all("p"))
                ])
            except:
                continue

    # Socials
    socials = {}
    for a in soup.find_all("a", href=True):
        if "instagram" in a["href"]:
            socials["instagram"] = a["href"]
        elif "facebook" in a["href"]:
            socials["facebook"] = a["href"]
        elif "tiktok" in a["href"]:
            socials["tiktok"] = a["href"]

    # Contact Info
    text = soup.get_text()
    import re
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    phones = re.findall(r'\+?\d[\d\s\-\(\)]{8,}', text)

    # About the Brand
    about = ""
    for a in soup.find_all("a", href=True):
        if "about" in a["href"].lower():
            try:
                about_url = urljoin(base_url, a["href"])
                about_text = requests.get(about_url).text
                about = BeautifulSoup(about_text, "lxml").get_text()
                break
            except:
                continue

    # Links
    links = {}
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        if "track" in href:
            links["order_tracking"] = urljoin(base_url, href)
        if "blog" in href:
            links["blog"] = urljoin(base_url, href)
        if "contact" in href:
            links["contact_us"] = urljoin(base_url, href)

    return {
        "brand_name": base_url.split("//")[-1].split(".")[0],
        "product_catalog": products,
        "hero_products": hero_products,
        "policies": policies,
        "faqs": faqs,
        "social_handles": socials,
        "contact": {"emails": list(set(emails)), "phones": list(set(phones))},
        "about": about,
        "important_links": links
    }
