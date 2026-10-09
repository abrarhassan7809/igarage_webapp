U = "https://images.unsplash.com/"
def _img(id_): return f"{U}{id_}?auto=format&fit=crop&w=400&q=80"

PRODUCTS = [
    dict(n="iPhone 18 Pro", c="iPhone", img=_img("photo-1695048133142-1a20484d2569"), price=449999, d='6.3" OLED', ch="A20 Pro", st="256GB"),
    dict(n="iPhone 17e", c="iPhone", img=_img("photo-1510557880182-3d4d3cba35a5"), price=189999, d='6.1" OLED', ch="A19", st="256GB"),
    dict(n="iPad Air", c="iPad", img=_img("photo-1544244015-0df4b3ffc6b0"), price=199999, d='11" Liquid Retina', ch="M3", st="128GB"),
    dict(n="iPad", c="iPad", img=_img("photo-1561154464-82e9adf32764"), price=119999, d='11" Liquid Retina', ch="A16", st="128GB"),
    dict(n="MacBook Air", c="Mac", img=_img("photo-1517336714731-489689fd1ca8"), price=289999, d='13.6" Liquid Retina', ch="M4", st="256GB"),
    dict(n="MacBook Neo", c="Mac", img=_img("photo-1611186871348-b1ce696e52c9"), price=229999, d='13" Retina', ch="A-series", st="256GB"),
    dict(n="Watch Series 11", c="Watch", img=_img("photo-1508685096489-7aacd43bd3b1"), price=109999, d="Always-on OLED", ch="S11", st="64GB"),
    dict(n="AirPods Pro 3", c="AirPods", img=_img("photo-1600294037681-c80b4cb5b434"), price=69999, d="ANC + Transparency", ch="H2", st="—"),
    dict(n="AirTag (4 pack)", c="Accessories", img=_img("photo-1628172922123-28956b9c9703"), price=34999, d="—", ch="U1", st="—"),
]

_BLACK, _WHITE, _SILVER, _BURG = ("Black", "#2a2a2c"), ("White", "#f1f1f1"), ("Silver", "#d9d9dc"), ("Burgundy", "#6b1f2a")
IPHONES = [
    dict(slug="iphone-18-pro-max", n="iPhone 18 Pro Max", series="iPhone 18", base=549999, sto={"256GB": 0, "512GB": 60000, "1TB": 130000}, col=[_BURG, _SILVER, _BLACK], display='6.9" OLED, 120Hz', chip="A20 Pro"),
    dict(slug="iphone-18-pro", n="iPhone 18 Pro", series="iPhone 18", base=479999, sto={"256GB": 0, "512GB": 60000, "1TB": 130000}, col=[_BURG, _SILVER, _BLACK], display='6.3" OLED, 120Hz', chip="A20 Pro"),
    dict(slug="iphone-17-pro", n="iPhone 17 Pro", series="iPhone 17", base=429999, sto={"256GB": 0, "512GB": 55000}, col=[("Cosmic Orange", "#c4622d"), ("Deep Blue", "#2b3f5c"), _SILVER], display='6.3" OLED, 120Hz', chip="A19 Pro"),
    dict(slug="iphone-17", n="iPhone 17", series="iPhone 17", base=299999, sto={"256GB": 0, "512GB": 50000}, col=[_BLACK, _WHITE, ("Sage", "#9fb59a")], display='6.3" OLED, 120Hz', chip="A19"),
    dict(slug="iphone-air", n="iPhone Air", series="iPhone Air", base=349999, sto={"256GB": 0, "512GB": 50000}, col=[("Space Black", "#2a2a2c"), ("Sky Blue", "#a9c7e0")], display='6.5" OLED, 120Hz', chip="A19 Pro"),
    dict(slug="iphone-17e", n="iPhone 17e", series="iPhone 17e", base=189999, sto={"256GB": 0, "512GB": 45000}, col=[_BLACK, _WHITE], display='6.1" OLED', chip="A19"),
]

HERO = [
    dict(cls="s1", tag="Coming soon", title="iPhone Pro", text="Register your interest for launch day.", cta="Register interest", href="/#products"),
    dict(cls="s2", tag="New prices", title="MacBook price list", text="PTA-approved with local warranty.", cta="See prices", href="/#compare"),
    dict(cls="s3", tag="Back to school", title="Student pricing", text="Extended warranty on eligible Macs.", cta="View offers", href="/#offers"),
]
TRUST = [("patch-check", "Official warranty"), ("phone", "PTA approved"), ("shop", "Trusted resellers")]
OFFERS = [
    ("arrow-repeat", "iPhone trade-in", "Exchange a PTA-approved iPhone and pay only the difference."),
    ("shield-check", "Protection plan", "Cover for accidents and liquid damage on iPhone."),
    ("mortarboard", "Student pricing", "Special Mac prices with a longer warranty."),
]
NEWS = [
    ("Press · May 2026", "Recognized as Fastest Growing Brand of the Year"),
    ("Press · Feb 2026", "New protection plan for iPhone launched"),
    ("Press · Mar 2025", "First official iPhone trade-in program"),
]
STORES = {"karachi": 3, "lahore": 4, "islamabad": 2, "multan": 1}  # demo data

def categories(): return ["All", *dict.fromkeys(p["c"] for p in PRODUCTS)]
def series(): return ["All", *dict.fromkeys(p["series"] for p in IPHONES)]
def get_iphone(slug): return next((p for p in IPHONES if p["slug"] == slug), None)
def filter_products(cat="All"): return [p for p in PRODUCTS if cat == "All" or p["c"] == cat]
def filter_iphones(s="All", sort="def"):
    out = [p for p in IPHONES if s == "All" or p["series"] == s]
    if sort in ("asc", "desc"): out.sort(key=lambda p: p["base"], reverse=sort == "desc")
    return out
