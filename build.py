#!/usr/bin/env python3
"""Build the Ice Vault static site into dist/.

    python3 build.py            # build
    python3 -m http.server 8080 -d dist   # preview at http://localhost:8080
"""
import json
import math
import os
import random
import shutil
import sys
import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
DIST = os.path.join(ROOT, "dist")
# BASE="/ice-vault" builds for a sub-folder (GitHub project pages). SITE_URL overrides the public domain.
BASE = os.environ.get("BASE", "").rstrip("/")
import re
_ATTR_RE = re.compile(r'((?:href|src|action)=")/(?!/)')

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

from config import SITE
if os.environ.get("SITE_URL"):
    SITE["domain"] = os.environ["SITE_URL"].rstrip("/")
from data.catalog import (CATEGORIES, VIRTUAL_COLLECTIONS, NAV, SECONDARY_NAV, PRODUCTS, CUSTOM_PROJECTS,
                          REVIEWS, FAQ, PRICE_BUCKETS, COLOR_NAMES, STONE_NAMES, money_round)
import svggen

TYPE_LABELS = {
    "cuban": "Miami Cuban", "rope": "Rope", "tennis": "Tennis", "franco": "Franco", "box": "Box", "figaro": "Figaro",
    "paperclip": "Paperclip", "station": "Station", "cross": "Cross", "medallion": "Medallion", "initial": "Initial",
    "dogtag": "Dog tag", "heart": "Heart", "drop": "Pear drop", "eye": "Evil eye", "star": "Star", "signet": "Signet",
    "cuban-ring": "Cuban link", "eternity": "Eternity", "band": "Band", "halo": "Halo", "solitaire": "Solitaire",
    "three-stone": "Three stone", "studs": "Studs", "cluster": "Cluster", "baguette": "Baguette", "hoops": "Hoops",
    "single": "Single", "drops": "Drops", "cross-e": "Cross", "cuban-b": "Cuban", "tennis-b": "Tennis", "rope-b": "Rope",
    "id": "ID", "franco-b": "Franco", "bangle": "Bangle", "paperclip-b": "Paperclip", "watch": "Watch",
}
PURITY_LABELS = {"10K": "10K gold", "14K": "14K gold", "18K": "18K gold", "21K": "21K gold", "925": ".925 silver", "Steel": "Stainless steel"}
STONE_LABELS = {"dia": "Natural diamond", "lab": "Lab diamond", "blk": "Black diamond", "eme": "Emerald", "rub": "Ruby", "sap": "Sapphire", "multi": "Multi-color diamond", "none": "No stones"}

RING_SETTINGS = [
    ("solitaire", "Solitaire", 950, "Four or six prongs, nothing else. The stone does the talking."),
    ("hidden-halo", "Hidden halo", 1350, "A ring of small diamonds under the center stone. Visible from the side."),
    ("halo", "Halo", 1650, "Diamonds around the center stone. Makes the center look larger."),
    ("three-stone", "Three stone", 1950, "Center stone with two side stones. Past, present, future."),
    ("pave", "Pave band", 1550, "Small diamonds set into the band, center stone in prongs."),
    ("cathedral", "Cathedral", 1150, "Arched shoulders lift the stone. A classic profile."),
]
RING_SHAPES = ["round", "oval", "emerald", "cushion", "radiant", "pear", "marquise", "princess"]
RING_METALS = [("14K", "Y"), ("14K", "W"), ("14K", "R"), ("18K", "Y"), ("18K", "W"), ("18K", "R")]


def money(v):
    return "${:,.0f}".format(v)


def write(path, content):
    full = os.path.join(DIST, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    if BASE and full.endswith(".html"):
        content = _ATTR_RE.sub(lambda m: m.group(1) + BASE + "/", content)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def prefixed(d, keys=("image", "url")):
    """Copy of dict d with BASE prepended to path-valued keys."""
    out = dict(d)
    for k in keys:
        if BASE and isinstance(out.get(k), str) and out[k].startswith("/"):
            out[k] = BASE + out[k]
    return out


def build_collections():
    cols = {}
    for slug, c in CATEGORIES.items():
        prods = [p for p in PRODUCTS if p["collection"] == slug]
        cols[slug] = dict(slug=slug, title=c["title"], blurb=c["blurb"], seo=c["seo"], products=prods, kind=c["kind"], gender=c["gender"])
    for slug, c in VIRTUAL_COLLECTIONS.items():
        prods = [p for p in PRODUCTS if c["filt"](p)]
        cols[slug] = dict(slug=slug, title=c["title"], blurb=c["blurb"], seo="", products=prods, kind="", gender="")
    for c in cols.values():
        c["count"] = len(c["products"])
        c["url"] = f"/collections/{c['slug']}/"
        c["products"] = featured_first(c["products"])
    return cols


def featured_first(prods):
    def key(p):
        return (0 if "Best seller" in p["badges"] else 1 if "New" in p["badges"] else 2 if p.get("compare_at") else 3)
    return sorted(prods, key=key)


def facets(prods):
    def count(keyfn):
        d = {}
        for p in prods:
            k = keyfn(p)
            if k:
                d[k] = d.get(k, 0) + 1
        return d
    price = []
    for label, lo, hi in PRICE_BUCKETS:
        n = sum(1 for p in prods if lo <= p["price"] < hi)
        if n:
            price.append(dict(label=label, value=f"{lo}-{hi}", count=n))
    color = [dict(label=COLOR_NAMES.get(k, k), value=k, count=v) for k, v in sorted(count(lambda p: p["color"] if p["color"] in COLOR_NAMES else "").items())]
    purity = [dict(label=PURITY_LABELS.get(k, k), value=k, count=v) for k, v in sorted(count(lambda p: p["purity"]).items())]
    stone = [dict(label=STONE_LABELS.get(k, k), value=k, count=v) for k, v in sorted(count(lambda p: p["stone"] or "none").items(), key=lambda kv: -kv[1])]
    ptype = [dict(label=TYPE_LABELS.get(k, k), value=k, count=v) for k, v in sorted(count(lambda p: p["ptype"]).items(), key=lambda kv: -kv[1])]
    out = [("Price", "price", price), ("Type", "type", ptype), ("Metal color", "color", color), ("Purity", "purity", purity), ("Stones", "stone", stone)]
    return [dict(title=t, name=n, options=o) for t, n, o in out if len(o) > 1]


def diamond_inventory(n=420, seed=7):
    rnd = random.Random(seed)
    shapes = ["Round", "Oval", "Cushion", "Emerald", "Princess", "Pear", "Radiant", "Marquise", "Asscher", "Heart"]
    weights = [30, 18, 10, 10, 6, 8, 6, 4, 4, 3]
    colors = list("DEFGHIJK")
    cfac = {"D": 1.35, "E": 1.25, "F": 1.15, "G": 1.0, "H": .9, "I": .8, "J": .7, "K": .6}
    clar = ["FL", "IF", "VVS1", "VVS2", "VS1", "VS2", "SI1", "SI2"]
    kfac = {"FL": 1.55, "IF": 1.4, "VVS1": 1.25, "VVS2": 1.15, "VS1": 1.05, "VS2": 1.0, "SI1": .85, "SI2": .72}
    cuts = ["Excellent", "Very Good", "Good"]
    out = []
    for i in range(n):
        lab = rnd.random() < 0.55
        shape = rnd.choices(shapes, weights)[0]
        band = rnd.random()
        ct = rnd.uniform(0.3, 1.0) if band < .4 else rnd.uniform(1.0, 2.5) if band < .8 else rnd.uniform(2.5, 6.0)
        ct = round(ct, 2)
        color = rnd.choices(colors, [8, 12, 16, 18, 16, 12, 10, 8])[0]
        clarity = rnd.choices(clar, [2, 4, 8, 12, 18, 20, 20, 16])[0]
        cut = rnd.choices(cuts, [60, 30, 10] if shape == "Round" else [45, 40, 15])[0]
        sf = 1.0 if shape == "Round" else 0.85
        if lab:
            ppc = 980 * ct ** 0.45 * cfac[color] * kfac[clarity] * sf
        else:
            ppc = 4100 * ct ** 0.95 * cfac[color] * kfac[clarity] * sf
        if cut == "Very Good":
            ppc *= .93
        elif cut == "Good":
            ppc *= .84
        price = max(money_round(ppc * ct, 50 if ppc * ct >= 1000 else 10), 150)
        diam = 6.45 * ct ** (1 / 3)
        if shape == "Round":
            L, W = diam, diam
        elif shape in ("Oval", "Pear", "Marquise"):
            ratio = {"Oval": 1.38, "Pear": 1.5, "Marquise": 1.9}[shape]
            W = diam * 0.92 / math.sqrt(ratio); L = W * ratio
        else:
            ratio = {"Emerald": 1.4, "Radiant": 1.2, "Cushion": 1.05, "Princess": 1.0, "Asscher": 1.0, "Heart": 1.0}[shape]
            W = diam * 0.88 / math.sqrt(ratio); L = W * ratio
        depth = W * rnd.uniform(0.58, 0.66)
        lab_name = "IGI" if lab else ("GIA" if rnd.random() < .85 else "IGI")
        out.append(dict(id=f"D{10000 + i * 37 % 89999}", shape=shape, carat=ct, color=color, clarity=clarity, cut=cut, lab=lab,
                        origin="Lab grown" if lab else "Natural", cert=lab_name, cert_no=f"{rnd.randint(1000000000, 9999999999)}",
                        price=price, measurements=f"{L:.2f} x {W:.2f} x {depth:.2f} mm", table=rnd.randint(54, 62), depth=round(rnd.uniform(58, 64), 1),
                        fluor=rnd.choices(["None", "Faint", "Medium"], [70, 22, 8])[0]))
    return out


def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    shutil.copytree(os.path.join(ROOT, "static"), DIST, dirs_exist_ok=True)

    env = Environment(loader=FileSystemLoader(os.path.join(ROOT, "templates")), autoescape=select_autoescape(["html"]), trim_blocks=True, lstrip_blocks=True)
    env.filters["money"] = money
    cols = build_collections()
    env.globals.update(base=BASE, site=SITE, nav=NAV, secondary_nav=SECONDARY_NAV, cols=cols, categories=CATEGORIES, year=datetime.date.today().year,
                       logo_mark=Markup(svggen.logo_mark()), type_labels=TYPE_LABELS, color_names=COLOR_NAMES, stone_names=STONE_NAMES,
                       product_count=len(PRODUCTS), faq=FAQ, reviews=REVIEWS, custom_projects=CUSTOM_PROJECTS)

    def render(template, path, **ctx):
        page = ctx.pop("page")
        page.setdefault("path", path if path.endswith("/") else path)
        page.setdefault("body_class", "")
        html = env.get_template(template).render(page=page, **ctx)
        write(path.rstrip("/") + "/index.html" if path.endswith("/") else path, html)
        return path

    urls = []

    # images
    for p in PRODUCTS:
        write(p["image"], svggen.render_product(p))
    for c in CUSTOM_PROJECTS:
        write(c["image"], svggen.render_custom(c))
    for setting, _, _, _ in RING_SETTINGS:
        for shape in RING_SHAPES:
            for color in ("Y", "W", "R"):
                for size, ct in (("s", 0.8), ("m", 1.5), ("l", 2.6)):
                    write(f"/img/rings/{setting}-{shape}-{color}-{size}.svg", svggen.ring_builder_preview(setting, shape, color, ct))
    write("/favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="8" fill="#0A0E14"/><g fill="none" stroke="#BFE3FF" stroke-width="1.8"><polygon points="20,5 30,9 35,20 30,31 20,35 10,31 5,20 10,9"/><polygon points="20,12 28,20 20,28 12,20"/></g></svg>')

    # home
    home = dict(
        mens=[cols[s] for s in ("mens-chains", "mens-pendants", "mens-rings", "mens-earrings", "mens-bracelets", "mens-watches")],
        womens=[cols[s] for s in ("womens-necklaces", "womens-pendants", "womens-rings", "womens-earrings", "womens-bracelets", "womens-watches")],
    )
    urls.append(render("home.html", "/", page=dict(title="Ice Vault | Diamonds and Fine Jewelry, New York", description=SITE["tagline"] + ". Solid gold chains, diamond pendants, engagement rings, watches and custom pieces from our 47th Street workshop.", body_class="home", full_title=True), hero=Markup(svggen.hero_diamond()), home=home))

    # collections
    for c in cols.values():
        urls.append(render("collection.html", c["url"], page=dict(title=c["title"], description=c["blurb"]), col=c, facets=facets(c["products"])))

    # products
    for p in PRODUCTS:
        related = [q for q in cols[p["collection"]]["products"] if q is not p][:4]
        ld = {"@context": "https://schema.org", "@type": "Product", "name": p["title"], "image": SITE["domain"] + p["image"], "description": p["desc"], "sku": p["sku"], "brand": {"@type": "Brand", "name": "Ice Vault"},
              "offers": {"@type": "Offer", "priceCurrency": "USD", "price": p["price"], "availability": "https://schema.org/InStock", "url": SITE["domain"] + p["url"]}}
        urls.append(render("product.html", p["url"], page=dict(title=p["title"], description=p["desc"][:155]), p=p, related=related, col=cols[p["collection"]], jsonld=Markup(json.dumps(ld)),
                           pdata=Markup(json.dumps(prefixed({k: p.get(k) for k in ("slug", "title", "price", "compare_at", "image", "url", "length", "variants", "sku")})))))

    # custom + tools
    urls.append(render("custom.html", "/custom/", page=dict(title="Custom jewelry", description="Start a custom jewelry project with Ice Vault. Pendants, rings, chains and bracelets designed with you and made on 47th Street.")))
    urls.append(render("gallery.html", "/custom/gallery/", page=dict(title="Past custom projects", description="Custom pendants, rings and chains made for Ice Vault clients.")))
    urls.append(render("ring-builder.html", "/ring-builder/", page=dict(title="Engagement ring builder", description="Choose a setting, a metal and a diamond. See the price as you build."), settings=RING_SETTINGS, shapes=RING_SHAPES, metals=RING_METALS))
    urls.append(render("diamond-search.html", "/diamond-search/", page=dict(title="Diamond search", description="Search natural and lab-grown diamonds by shape, carat, color, clarity and price.")))
    write("/diamonds.json", json.dumps(diamond_inventory()))

    # info pages
    simple = [
        ("about.html", "/about/", "About Ice Vault", "Ice Vault is a diamond and jewelry workshop on 47th Street in New York. Our story, our bench and our promise."),
        ("contact.html", "/contact/", "Contact", "Call, text, email or visit Ice Vault at 26 W 47th St, New York."),
        ("financing.html", "/financing/", "Financing and layaway", "0% financing for 12 months and in-house layaway with 25% down."),
        ("shipping.html", "/shipping-returns/", "Shipping and returns", "Free insured shipping in the US, worldwide shipping, and 30-day returns on stock pieces."),
        ("faq.html", "/faq/", "Questions and answers", "Answers about gold purity, diamonds, custom work, financing, returns and shipping."),
        ("reviews.html", "/reviews/", "Client reviews", "What Ice Vault clients say about their chains, rings and custom pieces."),
        ("appointment.html", "/appointment/", "Book an appointment", "Book a visit to the Ice Vault showroom on 47th Street or a video call from the bench."),
        ("sell.html", "/sell/", "Sell or trade in", "Sell your gold, diamonds and watches to Ice Vault, or trade them in for store credit with a 10% bonus."),
        ("services.html", "/services/", "Repairs, resizing and appraisals", "Ring resizing, chain repair, stone tightening, polishing and certified appraisals at Ice Vault."),
        ("privacy.html", "/privacy/", "Privacy policy", "How Ice Vault handles your information."),
        ("terms.html", "/terms/", "Terms of sale", "Ice Vault terms of sale, warranty and returns."),
        ("cart.html", "/cart/", "Your cart", "Review the pieces in your cart."),
        ("checkout.html", "/checkout/", "Request an invoice", "Send us your cart and we reply with a secure payment link."),
        ("search.html", "/search/", "Search", "Search Ice Vault chains, pendants, rings, earrings, bracelets and watches."),
    ]
    for tpl, path, title, desc in simple:
        urls.append(render(tpl, path, page=dict(title=title, description=desc)))
    render("404.html", "/404.html", page=dict(title="Page not found", description="That page does not exist."))

    # search index
    idx = [prefixed({k: p.get(k) for k in ("slug", "title", "price", "compare_at", "image", "url", "collection", "kind", "ptype", "color", "purity", "stone", "badges", "metal")}) for p in PRODUCTS]
    write("/products.json", json.dumps(idx))

    # sitemap + robots
    today = datetime.date.today().isoformat()
    sm = ['<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"<url><loc>{SITE['domain']}{u}</loc><lastmod>{today}</lastmod></url>")
    sm.append("</urlset>")
    write("/sitemap.xml", "".join(sm))
    write("/robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE['domain']}/sitemap.xml\n")
    write("/.nojekyll", "")
    print(f"built {len(urls)} pages, {len(PRODUCTS)} products -> {DIST}")


if __name__ == "__main__":
    main()
