from fastapi.templating import Jinja2Templates
from app.config import TEMPLATE_DIR, SITE_NAME

templates = Jinja2Templates(directory=TEMPLATE_DIR)
templates.env.filters["money"] = lambda n: f"Rs {n:,}"
templates.env.globals["SITE_NAME"] = SITE_NAME
templates.env.globals["NAV"] = [
    ("iPhone", "/iphone/"), ("Accessories", "/#products"),
    ("Services", "/#offers"), ("Exchange", "/#offers"),
]
