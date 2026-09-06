"""Catalog data: navigation, categories and products.

Products are built from small seed lists so titles read like a real
Diamond District inventory. Edit the seed tables to change stock.
"""
import re

# ---------------------------------------------------------------- helpers
GOLD_RATE = {"10K": 58, "14K": 79, "18K": 101, "21K": 118, "22K": 124}
SILVER_RATE = 3.2

COLOR_NAMES = {"Y": "Yellow Gold", "W": "White Gold", "R": "Rose Gold", "T": "Two-Tone Gold", "S": "Sterling Silver"}
STONE_NAMES = {
    "": "", "dia": "Diamond", "lab": "Lab Diamond", "blk": "Black Diamond",
    "eme": "Emerald", "rub": "Ruby", "sap": "Sapphire", "opal": "Opal", "multi": "Multi-Color Diamond",
}


def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s


def money_round(x, step=10):
    return int(round(x / step) * step)


def metal_label(purity, color):
    if color == "S":
        return ".925 Silver"
    return f"{purity} {COLOR_NAMES[color]}"


def base_metal(purity, color, grams):
    if color == "S":
        return grams * SILVER_RATE + 40
    return grams * GOLD_RATE[purity]


# ---------------------------------------------------------------- categories
CATEGORIES = {
    # men's
    "mens-chains": dict(title="Men's Chains", gender="mens", kind="chains",
        blurb="Solid and hollow gold chains from 2mm to 12mm. Miami Cuban, rope, Franco, tennis and box links, made and finished in our 47th Street workshop.",
        seo="Every chain in this collection is stamped, weighed and appraised before it ships. Solid links are cast from 10K, 14K or 18K gold and hand polished. Hollow links give you the same look at a lower weight. If you do not see the width or length you want, call the concierge and we will make it."),
    "mens-pendants": dict(title="Men's Pendants", gender="mens", kind="pendants",
        blurb="Crosses, medallions, initials, dog tags and custom charms, set with natural or lab diamonds. Every pendant ships with a matching chain option.",
        seo="Pendants are cast in-house and set by hand. Diamond pendants use VS clarity stones unless the listing says otherwise."),
    "mens-rings": dict(title="Men's Rings", gender="mens", kind="rings",
        blurb="Signets, bands, Cuban link rings, eternity rings and statement diamond rings in gold and platinum.",
        seo="Rings are made to your size. Standard sizes ship in 2 to 5 business days. Half sizes and sizes above 13 take one extra week."),
    "mens-earrings": dict(title="Men's Earrings", gender="mens", kind="earrings",
        blurb="Diamond studs, clusters, baguettes and hoops. Sold as pairs, singles on request.",
        seo="Studs use screw backs by default. Ask for push backs if you prefer them."),
    "mens-bracelets": dict(title="Men's Bracelets", gender="mens", kind="bracelets",
        blurb="Cuban, tennis, rope and ID bracelets in solid gold, with or without diamonds.",
        seo="Bracelets are sized to your wrist. Send us a measurement and we will adjust the length at no charge."),
    "mens-watches": dict(title="Men's Watches", gender="mens", kind="watches",
        blurb="Pre-owned and unworn luxury watches, inspected by our watchmaker and sold with a two-year Ice Vault warranty.",
        seo="Every watch is authenticated in-house. Box and papers are listed when present."),
    # women's
    "womens-necklaces": dict(title="Women's Necklaces", gender="womens", kind="chains",
        blurb="Tennis necklaces, thin Cuban links, paperclip chains and diamond stations in 14K and 18K gold.",
        seo="Necklaces come in 16, 18 and 20 inch lengths. Custom lengths are made on request."),
    "womens-pendants": dict(title="Women's Pendants", gender="womens", kind="pendants",
        blurb="Hearts, initials, crosses, evil eyes and pear drops, set with diamonds and colored stones.",
        seo="Each pendant includes an 18 inch cable chain. Upgrade to a Cuban or paperclip chain at checkout."),
    "womens-rings": dict(title="Women's Rings", gender="womens", kind="rings",
        blurb="Engagement rings, eternity bands, stacking rings and cocktail rings with natural and lab diamonds.",
        seo="Engagement rings can be built to order with our ring builder. Choose your setting, metal and diamond."),
    "womens-earrings": dict(title="Women's Earrings", gender="womens", kind="earrings",
        blurb="Studs, hoops, huggies, drops and clusters in gold and diamonds.",
        seo="Studs come with screw backs. Hoops and huggies use hinged snap closures."),
    "womens-bracelets": dict(title="Women's Bracelets", gender="womens", kind="bracelets",
        blurb="Tennis bracelets, bangles, thin Cuban links and charm bracelets.",
        seo="Tennis bracelets are made in 6.5, 7 and 7.5 inch lengths. Tell us your wrist size and we will fit it."),
    "womens-watches": dict(title="Women's Watches", gender="womens", kind="watches",
        blurb="Ladies' luxury watches, inspected, serviced and covered by our two-year warranty.",
        seo="Diamond bezels and dials are factory unless the listing says aftermarket."),
}

# collections that are built from filters rather than a category
VIRTUAL_COLLECTIONS = {
    "men": dict(title="All Men's Jewelry", blurb="Every chain, pendant, ring, earring, bracelet and watch for men.", filt=lambda p: p["gender"] == "mens"),
    "women": dict(title="All Women's Jewelry", blurb="Every necklace, pendant, ring, earring, bracelet and watch for women.", filt=lambda p: p["gender"] == "womens"),
    "watches": dict(title="Watches", blurb="Luxury watches for men and women, authenticated and covered by our two-year warranty.", filt=lambda p: p["kind"] == "watches"),
    "best-sellers": dict(title="Best Sellers", blurb="The pieces our clients buy most.", filt=lambda p: "Best seller" in p["badges"]),
    "new-arrivals": dict(title="New Arrivals", blurb="Fresh from the bench this month.", filt=lambda p: "New" in p["badges"]),
    "sale": dict(title="Fall Sale", blurb="Select pieces up to 15% off with code ICE15 at checkout.", filt=lambda p: p.get("compare_at")),
    "under-1000": dict(title="Under $1,000", blurb="Solid gold and diamond pieces under one thousand dollars.", filt=lambda p: p["price"] < 1000),
    "gold-chains": dict(title="Gold Chains", blurb="Every solid and hollow gold chain we make, for men and women.", filt=lambda p: p["kind"] == "chains" and p["color"] != "S"),
    "engagement": dict(title="Engagement Rings", blurb="Solitaires, halos and three-stone rings, ready to ship or built to order.", filt=lambda p: p.get("engagement")),
    "diamond-jewelry": dict(title="Diamond Jewelry", blurb="Every piece set with natural or lab-grown diamonds.", filt=lambda p: p["stone"] in ("dia", "lab", "blk", "multi")),
    "silver": dict(title="Silver Jewelry", blurb="Sterling silver pieces from our workshop.", filt=lambda p: p["color"] == "S"),
    "cuban": dict(title="Miami Cuban Pieces", blurb="Cuban link chains, bracelets and rings.", filt=lambda p: "cuban" in p["ptype"]),
    "gifts-under-500": dict(title="Gifts Under $500", blurb="Small gold and silver pieces that ship in two days.", filt=lambda p: p["price"] < 500),
}

PRICE_BUCKETS = [
    ("Under $500", 0, 500), ("$500 to $1,000", 500, 1000), ("$1,000 to $2,500", 1000, 2500),
    ("$2,500 to $5,000", 2500, 5000), ("$5,000 to $10,000", 5000, 10000), ("$10,000 and up", 10000, 10**9),
]

# ---------------------------------------------------------------- navigation
NAV = [
    dict(label="Men's", href="/collections/men/", cols=[
        dict(title="Chains", href="/collections/mens-chains/", links=[
            ("Miami Cuban", "/collections/mens-chains/?type=cuban"), ("Rope", "/collections/mens-chains/?type=rope"),
            ("Tennis", "/collections/mens-chains/?type=tennis"), ("Franco", "/collections/mens-chains/?type=franco"),
            ("Box", "/collections/mens-chains/?type=box"), ("Figaro", "/collections/mens-chains/?type=figaro")]),
        dict(title="Pendants", href="/collections/mens-pendants/", links=[
            ("Crosses", "/collections/mens-pendants/?type=cross"), ("Medallions", "/collections/mens-pendants/?type=medallion"),
            ("Initials", "/collections/mens-pendants/?type=initial"), ("Dog tags", "/collections/mens-pendants/?type=dogtag"),
            ("Custom pendants", "/custom/")]),
        dict(title="Rings", href="/collections/mens-rings/", links=[
            ("Signet", "/collections/mens-rings/?type=signet"), ("Bands", "/collections/mens-rings/?type=band"),
            ("Cuban link", "/collections/mens-rings/?type=cuban-ring"), ("Eternity", "/collections/mens-rings/?type=eternity"),
            ("Black diamond", "/collections/mens-rings/?stone=blk")]),
        dict(title="Earrings", href="/collections/mens-earrings/", links=[
            ("Studs", "/collections/mens-earrings/?type=studs"), ("Clusters", "/collections/mens-earrings/?type=cluster"),
            ("Baguette", "/collections/mens-earrings/?type=baguette"), ("Hoops", "/collections/mens-earrings/?type=hoops"),
            ("Singles", "/collections/mens-earrings/?type=single")]),
        dict(title="Bracelets", href="/collections/mens-bracelets/", links=[
            ("Cuban", "/collections/mens-bracelets/?type=cuban-b"), ("Tennis", "/collections/mens-bracelets/?type=tennis-b"),
            ("Rope", "/collections/mens-bracelets/?type=rope-b"), ("ID bracelets", "/collections/mens-bracelets/?type=id")]),
        dict(title="More", href="/collections/men/", links=[
            ("Watches", "/collections/mens-watches/"), ("Best sellers", "/collections/best-sellers/"),
            ("New arrivals", "/collections/new-arrivals/"), ("Under $1,000", "/collections/under-1000/"),
            ("Sale", "/collections/sale/")]),
    ]),
    dict(label="Women's", href="/collections/women/", cols=[
        dict(title="Necklaces", href="/collections/womens-necklaces/", links=[
            ("Tennis", "/collections/womens-necklaces/?type=tennis"), ("Cuban", "/collections/womens-necklaces/?type=cuban"),
            ("Paperclip", "/collections/womens-necklaces/?type=paperclip"), ("Rope", "/collections/womens-necklaces/?type=rope")]),
        dict(title="Pendants", href="/collections/womens-pendants/", links=[
            ("Hearts", "/collections/womens-pendants/?type=heart"), ("Initials", "/collections/womens-pendants/?type=initial"),
            ("Crosses", "/collections/womens-pendants/?type=cross"), ("Drops", "/collections/womens-pendants/?type=drop")]),
        dict(title="Rings", href="/collections/womens-rings/", links=[
            ("Engagement", "/collections/engagement/"), ("Eternity bands", "/collections/womens-rings/?type=eternity"),
            ("Halo", "/collections/womens-rings/?type=halo"), ("Stacking", "/collections/womens-rings/?type=band"),
            ("Ring builder", "/ring-builder/")]),
        dict(title="Earrings", href="/collections/womens-earrings/", links=[
            ("Studs", "/collections/womens-earrings/?type=studs"), ("Hoops", "/collections/womens-earrings/?type=hoops"),
            ("Drops", "/collections/womens-earrings/?type=drops"), ("Clusters", "/collections/womens-earrings/?type=cluster")]),
        dict(title="Bracelets", href="/collections/womens-bracelets/", links=[
            ("Tennis", "/collections/womens-bracelets/?type=tennis-b"), ("Bangles", "/collections/womens-bracelets/?type=bangle"),
            ("Cuban", "/collections/womens-bracelets/?type=cuban-b")]),
        dict(title="More", href="/collections/women/", links=[
            ("Watches", "/collections/womens-watches/"), ("Gifts under $500", "/collections/gifts-under-500/"),
            ("New arrivals", "/collections/new-arrivals/"), ("Sale", "/collections/sale/")]),
    ]),
    dict(label="Custom", href="/custom/", cols=[
        dict(title="Design with us", href="/custom/", links=[
            ("Start a custom project", "/custom/"), ("Engagement ring builder", "/ring-builder/"),
            ("Diamond search", "/diamond-search/"), ("Past projects", "/custom/gallery/")]),
        dict(title="Services", href="/services/", links=[
            ("Repairs and resizing", "/services/"), ("Appraisals", "/services/"),
            ("Sell or trade in", "/sell/"), ("Book an appointment", "/appointment/")]),
    ]),
    dict(label="Watches", href="/collections/watches/", cols=[
        dict(title="Watches", href="/collections/watches/", links=[
            ("Men's", "/collections/mens-watches/"), ("Women's", "/collections/womens-watches/"),
            ("Sell your watch", "/sell/")]),
    ]),
]

SECONDARY_NAV = [
    ("Sale", "/collections/sale/"), ("Best sellers", "/collections/best-sellers/"), ("New arrivals", "/collections/new-arrivals/"),
    ("Gold chains", "/collections/gold-chains/"), ("Engagement", "/collections/engagement/"),
    ("Diamond search", "/diamond-search/"), ("Ring builder", "/ring-builder/"),
]

# ---------------------------------------------------------------- products
PRODUCTS = []
_seen = set()


def add(**p):
    p.setdefault("badges", [])
    p.setdefault("stone", "")
    p.setdefault("variants", {})
    p.setdefault("specs", [])
    p["metal"] = metal_label(p["purity"], p["color"])
    if p["stone"]:
        p["stone_name"] = STONE_NAMES[p["stone"]]
    slug = slugify(p["title"])
    n = 2
    while slug in _seen:
        slug = f"{slugify(p['title'])}-{n}"; n += 1
    _seen.add(slug)
    p["slug"] = slug
    p["sku"] = f"IV{10000 + len(PRODUCTS) * 7 % 89999:05d}"
    p["url"] = f"/products/{slug}/"
    p["image"] = f"/img/products/{slug}.svg"
    p["kind"] = CATEGORIES[p["collection"]]["kind"]
    p["gender"] = CATEGORIES[p["collection"]]["gender"]
    PRODUCTS.append(p)
    return p


LENGTHS_M = [18, 20, 22, 24, 26, 30]
LENGTHS_W = [16, 18, 20]
RING_SIZES_M = [8, 9, 10, 11, 12, 13]
RING_SIZES_W = [4, 5, 6, 7, 8]


def chain(name, ptype, purity, color, width, length, solid=True, stone="", collection="mens-chains", badges=(), k=None, desc=None, compare=False):
    k = k if k is not None else (0.077 if solid else 0.026)
    grams = round(k * width ** 2 * length, 1)
    grams = max(grams, 1.2)
    price = base_metal(purity, color, grams) * 1.35 + 120
    if stone in ("dia", "lab"):
        ct = round(width * length * 0.045, 2)
        price += ct * (1400 if stone == "dia" else 420)
    price = money_round(price, 10 if price < 1500 else 50)
    style = "Solid" if solid else "Hollow"
    title = f"{purity if color != 'S' else '.925'} {COLOR_NAMES[color] if color != 'S' else 'Silver'} {style} {name} {width}mm {length} Inches"
    if stone:
        title = f"{purity} {COLOR_NAMES[color]} {STONE_NAMES[stone]} {name} {width}mm {length} Inches"
    lengths = LENGTHS_W if collection == "womens-necklaces" else LENGTHS_M
    p = add(title=title, ptype=ptype, purity=purity, color=color, width=width, length=length, grams=grams,
            price=price, stone=stone, collection=collection, badges=list(badges),
            variants={"Length": [f"{l} in" for l in lengths], "Color": [COLOR_NAMES[c] for c in ("Y", "W", "R")] if color != "S" and color != "T" else []},
            specs=[("Metal", metal_label(purity, color)), ("Construction", style + " links"), ("Width", f"{width} mm"),
                   ("Length", f"{length} inches"), ("Weight", f"{grams} grams, may vary"), ("Clasp", "Box clasp with safety lock" if width >= 4 else "Lobster clasp")],
            desc=desc or f"{name} links at {width}mm. {style} construction, hand polished, stamped {purity if color != 'S' else '925'}. {length} inches sits {'at the collarbone' if length <= 20 else 'below the collarbone' if length <= 22 else 'at mid chest'}. Wear it alone or layer it with a pendant.")
    if compare:
        p["compare_at"] = money_round(price * 1.15, 10)
    return p


def pendant(name, ptype, purity, color, grams, stone="", ct=0.0, collection="mens-pendants", badges=(), letter="", desc=None, compare=False, chain_in=22):
    price = base_metal(purity, color, grams) * 1.4 + 180
    if stone in ("dia", "lab", "blk", "multi"):
        price += ct * {"dia": 1500, "lab": 450, "blk": 300, "multi": 1300}[stone]
    elif stone:
        price += ct * 500
    price = money_round(price, 10 if price < 1500 else 50)
    metal = metal_label(purity, color)
    st = f" {STONE_NAMES[stone]}" if stone else ""
    title = f"{metal}{st} {name}" + (f" {ct} Ct" if ct else "")
    specs = [("Metal", metal), ("Weight", f"{grams} grams"), ("Height", f"{round(18 + grams * 1.1)} mm")]
    if ct:
        specs.append(("Stone weight", f"{ct} carats total"))
        specs.append(("Clarity", "VS1 to VS2" if stone in ("dia", "lab") else "Eye clean"))
    specs.append(("Chain", f"{chain_in} inch chain included"))
    p = add(title=title, ptype=ptype, purity=purity, color=color, grams=grams, price=price, stone=stone, ct=ct, letter=letter,
            collection=collection, badges=list(badges), variants={"Chain": ["Pendant only", "Cable chain", "Rope chain", "Cuban chain"]},
            specs=specs, desc=desc or f"{name} cast in {metal}{', set with ' + str(ct) + ' carats of ' + STONE_NAMES[stone].lower() + 's' if ct else ''}. Comes with a {chain_in} inch chain. Bail fits chains up to 5mm.")
    if compare:
        p["compare_at"] = money_round(price * 1.15, 10)
    return p


def ring(name, ptype, purity, color, grams, stone="", ct=0.0, collection="mens-rings", badges=(), engagement=False, shape="round", desc=None, compare=False):
    price = base_metal(purity, color, grams) * 1.45 + 160
    if stone in ("dia", "lab", "blk", "multi"):
        rate = {"dia": 2600 if engagement else 1500, "lab": 600 if engagement else 450, "blk": 300, "multi": 1300}[stone]
        price += ct * rate * (1.6 if ct >= 1.5 and stone == "dia" else 1)
    elif stone:
        price += ct * 550
    price = money_round(price, 10 if price < 1500 else 50)
    metal = metal_label(purity, color)
    st = f" {STONE_NAMES[stone]}" if stone else ""
    title = f"{metal}{st} {name}" + (f" {ct} Ct" if ct else "")
    sizes = RING_SIZES_W if collection == "womens-rings" else RING_SIZES_M
    specs = [("Metal", metal), ("Weight", f"{grams} grams")]
    if ct:
        specs += [("Center stone", f"{ct} ct {shape}" if engagement else f"{ct} ct total"), ("Clarity", "VS1 to VS2"), ("Color", "F to G")]
    specs.append(("Band width", f"{round(2 + grams / 4)} mm"))
    p = add(title=title, ptype=ptype, purity=purity, color=color, grams=grams, price=price, stone=stone, ct=ct, shape=shape,
            collection=collection, badges=list(badges), engagement=engagement,
            variants={"Size": [str(s) for s in sizes], "Color": [COLOR_NAMES[c] for c in ("Y", "W", "R")] if color not in ("S", "T") else []},
            specs=specs, desc=desc or f"{name} in {metal}. Made to your size. {'Center stone certified by GIA or IGI. ' if engagement else ''}Comfort fit inside. Ships in a wooden ring box.")
    if compare:
        p["compare_at"] = money_round(price * 1.15, 10)
    return p


def earrings(name, ptype, purity, color, grams, stone="", ct=0.0, collection="mens-earrings", badges=(), desc=None, compare=False):
    price = base_metal(purity, color, grams) * 1.4 + 120
    if stone in ("dia", "lab", "blk", "multi"):
        price += ct * {"dia": 1600, "lab": 480, "blk": 300, "multi": 1300}[stone]
    elif stone:
        price += ct * 500
    price = money_round(price, 10 if price < 1500 else 50)
    metal = metal_label(purity, color)
    st = f" {STONE_NAMES[stone]}" if stone else ""
    title = f"{metal}{st} {name}" + (f" {ct} Ct" if ct else "")
    specs = [("Metal", metal), ("Weight", f"{grams} grams per pair"), ("Backs", "Screw backs" if "Stud" in name or "Cluster" in name else "Hinged snap")]
    if ct:
        specs += [("Stone weight", f"{ct} carats total"), ("Clarity", "VS1 to VS2")]
    p = add(title=title, ptype=ptype, purity=purity, color=color, grams=grams, price=price, stone=stone, ct=ct,
            collection=collection, badges=list(badges), variants={"Sold as": ["Pair", "Single"], "Color": [COLOR_NAMES[c] for c in ("Y", "W", "R")] if color not in ("S", "T") else []},
            specs=specs, desc=desc or f"{name} in {metal}. Sold as a pair. Singles on request.")
    if compare:
        p["compare_at"] = money_round(price * 1.15, 10)
    return p


def bracelet(name, ptype, purity, color, width, length, solid=True, stone="", collection="mens-bracelets", badges=(), k=None, ct=0.0, desc=None, compare=False):
    k = k if k is not None else (0.077 if solid else 0.026)
    grams = max(round(k * width ** 2 * length, 1), 1.5)
    price = base_metal(purity, color, grams) * 1.4 + 140
    if stone in ("dia", "lab"):
        ct = ct or round(width * length * 0.06, 2)
        price += ct * (1500 if stone == "dia" else 450)
    price = money_round(price, 10 if price < 1500 else 50)
    metal = metal_label(purity, color)
    style = "Solid" if solid else "Hollow"
    title = f"{metal}{' ' + STONE_NAMES[stone] if stone else ''} {name} {width}mm {length} Inches"
    sizes = ["6.5 in", "7 in", "7.5 in"] if collection == "womens-bracelets" else ["7.5 in", "8 in", "8.5 in", "9 in"]
    specs = [("Metal", metal), ("Construction", style + " links"), ("Width", f"{width} mm"), ("Length", f"{length} inches"), ("Weight", f"{grams} grams, may vary"), ("Clasp", "Box clasp with safety lock" if width >= 5 else "Lobster clasp")]
    if ct:
        specs.append(("Stone weight", f"{ct} carats total"))
    p = add(title=title, ptype=ptype, purity=purity, color=color, width=width, length=length, grams=grams, price=price, stone=stone, ct=ct,
            collection=collection, badges=list(badges), variants={"Length": sizes, "Color": [COLOR_NAMES[c] for c in ("Y", "W", "R")] if color not in ("S", "T") else []},
            specs=specs, desc=desc or f"{name} at {width}mm, {length} inches. {style} construction. We adjust the length to your wrist at no charge.")
    if compare:
        p["compare_at"] = money_round(price * 1.15, 10)
    return p


def watch(title, price, dial, case_mm, ref, year, metal="Stainless steel", bracelet="Oyster", papers=True, collection="mens-watches", badges=(), color="W", purity="", diamonds=False, compare=False):
    p = add(title=title, ptype="watch", purity=purity or "Steel", color=color, price=money_round(price, 50), collection=collection, badges=list(badges),
            dial=dial, case_mm=case_mm, stone="dia" if diamonds else "",
            specs=[("Reference", ref), ("Year", str(year)), ("Case", f"{case_mm} mm {metal}"), ("Dial", dial), ("Bracelet", bracelet), ("Movement", "Automatic"), ("Box and papers", "Yes" if papers else "Box only"), ("Warranty", "2 years, Ice Vault")],
            desc=f"{title}. Inspected and timed by our watchmaker. {'Full set with box and papers.' if papers else 'Comes with box and Ice Vault warranty card.'} Two year warranty on the movement.")
    p["metal"] = metal
    if compare:
        p["compare_at"] = money_round(price * 1.12, 50)
    return p


# ---- men's chains
chain("Miami Cuban Link Chain", "cuban", "14K", "Y", 2.6, 22, badges=["Best seller"])
chain("Miami Cuban Link Chain", "cuban", "14K", "Y", 4, 22, badges=["Best seller"])
chain("Miami Cuban Link Chain", "cuban", "14K", "Y", 6, 24)
chain("Miami Cuban Link Chain", "cuban", "14K", "W", 5, 22, badges=["New"])
chain("Miami Cuban Link Chain", "cuban", "10K", "Y", 8, 24, compare=True)
chain("Miami Cuban Link Chain", "cuban", "18K", "Y", 10, 24)
chain("Miami Cuban Link Chain", "cuban", "14K", "R", 3, 20)
chain("Miami Cuban Link Chain", "cuban", "14K", "Y", 12, 26, stone="dia", badges=["New"])
chain("Miami Cuban Link Chain", "cuban", "14K", "Y", 7, 22, stone="lab")
chain("Rope Chain", "rope", "10K", "Y", 2.5, 22, solid=False, badges=["Best seller"])
chain("Rope Chain", "rope", "10K", "Y", 4, 24, solid=False)
chain("Rope Chain", "rope", "14K", "Y", 3, 22, badges=["Best seller"])
chain("Rope Chain", "rope", "14K", "Y", 5, 24)
chain("Rope Chain", "rope", "14K", "W", 2, 20, compare=True)
chain("Diamond Cut Rope Chain", "rope", "18K", "Y", 4, 24)
chain("Tennis Chain", "tennis", "14K", "W", 3, 20, stone="dia", badges=["Best seller"])
chain("Tennis Chain", "tennis", "14K", "Y", 4, 22, stone="dia")
chain("Tennis Chain", "tennis", "14K", "W", 5, 22, stone="lab", badges=["New"])
chain("Tennis Chain", "tennis", "10K", "Y", 3, 20, stone="lab", compare=True)
chain("Franco Chain", "franco", "14K", "Y", 2, 22, badges=["Best seller"])
chain("Franco Chain", "franco", "14K", "T", 3, 24)
chain("Franco Chain", "franco", "10K", "Y", 4, 24, solid=False)
chain("Round Box Chain", "box", "14K", "Y", 3, 22)
chain("Round Box Chain", "box", "14K", "W", 2, 20, compare=True)
chain("Figaro Chain", "figaro", "14K", "Y", 4, 22)
chain("Figaro Chain", "figaro", "10K", "Y", 6, 24, solid=False)
chain("Figaro Chain", "figaro", "14K", "Y", 3, 20, badges=["New"])
chain("Moon Cut Bead Chain", "box", "14K", "Y", 2.5, 22)
chain("Miami Cuban Link Chain", "cuban", "925", "S", 6, 22, k=0.06, compare=True)
chain("Rope Chain", "rope", "925", "S", 4, 24, k=0.05)

# ---- men's pendants
pendant("Cross Pendant", "cross", "14K", "Y", 6.4, badges=["Best seller"])
pendant("Cross Pendant", "cross", "14K", "Y", 8.1, stone="dia", ct=1.2, badges=["Best seller"])
pendant("Cross Pendant", "cross", "14K", "W", 9.5, stone="lab", ct=2.4, badges=["New"])
pendant("Cross Pendant", "cross", "10K", "Y", 5.2, stone="lab", ct=0.6, compare=True)
pendant("Cross Pendant", "cross", "925", "S", 7.0, stone="", compare=True)
pendant("Round Medallion Pendant", "medallion", "14K", "Y", 12.5, badges=["Best seller"])
pendant("Round Medallion Pendant", "medallion", "14K", "Y", 16.0, stone="dia", ct=2.1)
pendant("Round Medallion Pendant", "medallion", "18K", "Y", 21.0, stone="dia", ct=3.4, badges=["New"])
pendant("Round Medallion Pendant", "medallion", "14K", "W", 14.0, stone="blk", ct=2.0)
pendant("Initial Pendant", "initial", "14K", "Y", 5.5, letter="A", badges=["Best seller"])
pendant("Initial Pendant", "initial", "14K", "Y", 7.2, stone="dia", ct=0.9, letter="J")
pendant("Initial Pendant", "initial", "14K", "W", 7.2, stone="lab", ct=0.9, letter="M", compare=True)
pendant("Initial Pendant", "initial", "10K", "Y", 4.8, letter="D")
pendant("Dog Tag Pendant", "dogtag", "14K", "Y", 11.0)
pendant("Dog Tag Pendant", "dogtag", "14K", "Y", 14.0, stone="dia", ct=1.8, badges=["New"])
pendant("Dog Tag Pendant", "dogtag", "925", "S", 12.0, compare=True)
pendant("Lion Head Medallion Pendant", "medallion", "14K", "Y", 18.0, stone="eme", ct=0.4)
pendant("Star Pendant", "star", "14K", "Y", 8.5, stone="dia", ct=1.1)
pendant("Star Pendant", "star", "14K", "W", 8.5, stone="multi", ct=1.1, badges=["New"])

# ---- men's rings
ring("Signet Ring", "signet", "14K", "Y", 9.5, badges=["Best seller"])
ring("Signet Ring", "signet", "14K", "Y", 11.0, stone="dia", ct=0.5)
ring("Signet Ring", "signet", "10K", "Y", 8.0, stone="blk", ct=0.4, compare=True)
ring("Signet Ring", "signet", "925", "S", 10.0, compare=True)
ring("Miami Cuban Link Ring", "cuban-ring", "14K", "Y", 8.5, badges=["Best seller"])
ring("Miami Cuban Link Ring", "cuban-ring", "14K", "Y", 9.0, stone="dia", ct=0.8, badges=["New"])
ring("Miami Cuban Link Ring", "cuban-ring", "14K", "W", 9.0, stone="lab", ct=0.8)
ring("Eternity Band", "eternity", "14K", "Y", 6.0, stone="dia", ct=1.5)
ring("Eternity Band", "eternity", "14K", "W", 6.0, stone="lab", ct=1.5, compare=True)
ring("Eternity Band", "eternity", "14K", "Y", 6.5, stone="blk", ct=1.6)
ring("Wedding Band", "band", "14K", "Y", 7.0, badges=["Best seller"])
ring("Wedding Band", "band", "18K", "W", 7.5)
ring("Wedding Band", "band", "14K", "R", 6.0)
ring("Beveled Band", "band", "10K", "Y", 5.5, compare=True)
ring("Cluster Ring", "halo", "14K", "Y", 10.0, stone="dia", ct=2.2, badges=["New"])
ring("Cluster Ring", "halo", "14K", "W", 10.0, stone="lab", ct=2.2)
ring("Solitaire Ring", "solitaire", "14K", "Y", 8.0, stone="sap", ct=1.4, shape="oval")
ring("Solitaire Ring", "solitaire", "14K", "Y", 8.0, stone="rub", ct=1.2, shape="oval")

# ---- men's earrings
earrings("Round Diamond Studs", "studs", "14K", "W", 1.6, stone="dia", ct=0.5, badges=["Best seller"])
earrings("Round Diamond Studs", "studs", "14K", "W", 2.0, stone="dia", ct=1.0, badges=["Best seller"])
earrings("Round Diamond Studs", "studs", "14K", "W", 2.6, stone="dia", ct=2.0)
earrings("Round Diamond Studs", "studs", "14K", "Y", 2.0, stone="lab", ct=1.0, badges=["New"])
earrings("Round Diamond Studs", "studs", "14K", "W", 3.2, stone="lab", ct=4.0)
earrings("Round Diamond Studs", "studs", "14K", "W", 4.0, stone="lab", ct=10.0)
earrings("Round Diamond Studs", "studs", "10K", "Y", 1.4, stone="lab", ct=0.5, compare=True)
earrings("Cluster Studs", "cluster", "14K", "Y", 2.4, stone="dia", ct=1.0)
earrings("Cluster Studs", "cluster", "14K", "W", 2.4, stone="lab", ct=1.0, compare=True)
earrings("Baguette Studs", "baguette", "14K", "Y", 2.2, stone="dia", ct=0.8, badges=["New"])
earrings("Baguette Studs", "baguette", "14K", "W", 2.2, stone="lab", ct=0.8)
earrings("Huggie Hoops", "hoops", "14K", "Y", 3.0, badges=["Best seller"])
earrings("Huggie Hoops", "hoops", "14K", "Y", 3.4, stone="dia", ct=0.4)
earrings("Black Diamond Studs", "studs", "14K", "Y", 2.0, stone="blk", ct=1.0)
earrings("Single Diamond Stud", "single", "14K", "W", 1.0, stone="dia", ct=0.5)
earrings("Cross Dangle Studs", "cross-e", "14K", "Y", 2.8, stone="dia", ct=0.3, compare=True)

# ---- men's bracelets
bracelet("Miami Cuban Link Bracelet", "cuban-b", "14K", "Y", 6, 8, badges=["Best seller"])
bracelet("Miami Cuban Link Bracelet", "cuban-b", "14K", "Y", 8, 8.5)
bracelet("Miami Cuban Link Bracelet", "cuban-b", "14K", "W", 5, 8, badges=["New"])
bracelet("Miami Cuban Link Bracelet", "cuban-b", "10K", "Y", 10, 8.5, compare=True)
bracelet("Miami Cuban Link Bracelet", "cuban-b", "14K", "Y", 8, 8, stone="dia")
bracelet("Miami Cuban Link Bracelet", "cuban-b", "14K", "Y", 6, 8, stone="lab", badges=["New"])
bracelet("Tennis Bracelet", "tennis-b", "14K", "W", 3, 8, stone="dia", badges=["Best seller"])
bracelet("Tennis Bracelet", "tennis-b", "14K", "Y", 4, 8, stone="dia")
bracelet("Tennis Bracelet", "tennis-b", "14K", "W", 5, 8.5, stone="lab", compare=True)
bracelet("Rope Bracelet", "rope-b", "14K", "Y", 4, 8, badges=["Best seller"])
bracelet("Rope Bracelet", "rope-b", "10K", "Y", 5, 8.5, solid=False)
bracelet("ID Bracelet", "id", "14K", "Y", 8, 8.5)
bracelet("ID Bracelet", "id", "14K", "Y", 10, 8.5, stone="dia", ct=1.5, badges=["New"])
bracelet("Franco Bracelet", "franco-b", "14K", "Y", 3, 8, compare=True)
bracelet("Miami Cuban Link Bracelet", "cuban-b", "925", "S", 8, 8.5, k=0.06)

# ---- men's watches
watch("Rolex Datejust 36mm Silver Stick Dial Fluted Jubilee", 6900, "Silver", 36, "16014", 1988, metal="Stainless steel", bracelet="Jubilee", papers=False, badges=["Best seller"])
watch("Rolex Datejust 41mm Blue Dial Oystersteel", 14800, "Blue", 41, "126334", 2022, metal="Stainless steel", bracelet="Oyster")
watch("Rolex Submariner Date Black Dial", 15900, "Black", 41, "126610LN", 2023, badges=["New"])
watch("Rolex GMT-Master II Black Blue Bezel", 19500, "Black", 40, "126710BLNR", 2021, bracelet="Jubilee")
watch("Rolex Day-Date 40 Champagne Dial Yellow Gold", 42500, "Champagne", 40, "228238", 2020, metal="18K yellow gold", bracelet="President", color="Y", purity="18K")
watch("Audemars Piguet Royal Oak 41mm Blue Dial", 38900, "Blue", 41, "15500ST", 2021, bracelet="Integrated steel")
watch("Patek Philippe Nautilus 5711 Blue Dial", 115000, "Blue", 40, "5711/1A", 2019, bracelet="Integrated steel", papers=True)
watch("Cartier Santos Large Silver Dial", 7400, "Silver", 39.8, "WSSA0018", 2022, bracelet="Steel with QuickSwitch", compare=True)
watch("Omega Speedmaster Moonwatch Black Dial", 6200, "Black", 42, "310.30.42.50.01.001", 2023)
watch("Rolex Datejust 41mm Green Dial Two-Tone", 16800, "Green", 41, "126333", 2022, metal="Steel and yellow gold", bracelet="Jubilee", color="T", purity="18K", badges=["New"])
watch("Rolex Datejust 41 Iced Diamond Bezel and Dial", 24500, "Diamond pave", 41, "126334", 2021, diamonds=True, badges=["Best seller"])
watch("Tudor Black Bay 58 Black Dial", 3400, "Black", 39, "M79030N", 2022, compare=True)

# ---- women's necklaces
chain("Tennis Necklace", "tennis", "14K", "W", 2.5, 16, stone="dia", collection="womens-necklaces", badges=["Best seller"])
chain("Tennis Necklace", "tennis", "14K", "Y", 3, 18, stone="dia", collection="womens-necklaces")
chain("Tennis Necklace", "tennis", "14K", "W", 3, 18, stone="lab", collection="womens-necklaces", badges=["New"])
chain("Tennis Necklace", "tennis", "14K", "W", 2, 16, stone="lab", collection="womens-necklaces", compare=True)
chain("Miami Cuban Link Necklace", "cuban", "14K", "Y", 3, 18, collection="womens-necklaces", badges=["Best seller"])
chain("Miami Cuban Link Necklace", "cuban", "14K", "Y", 4, 16, collection="womens-necklaces")
chain("Miami Cuban Link Necklace", "cuban", "14K", "R", 2.5, 18, collection="womens-necklaces", compare=True)
chain("Paperclip Necklace", "paperclip", "14K", "Y", 3, 18, solid=False, k=0.04, collection="womens-necklaces", badges=["Best seller"])
chain("Paperclip Necklace", "paperclip", "14K", "W", 4, 20, solid=False, k=0.04, collection="womens-necklaces")
chain("Paperclip Necklace", "paperclip", "14K", "Y", 5, 18, solid=False, k=0.04, collection="womens-necklaces", badges=["New"])
chain("Rope Necklace", "rope", "14K", "Y", 2, 18, collection="womens-necklaces")
chain("Rope Necklace", "rope", "14K", "Y", 1.5, 16, collection="womens-necklaces", compare=True)
chain("Diamond Station Necklace", "station", "14K", "Y", 1.5, 18, stone="dia", k=0.02, collection="womens-necklaces", badges=["New"])
chain("Diamond Station Necklace", "station", "14K", "W", 1.5, 16, stone="lab", k=0.02, collection="womens-necklaces")
chain("Franco Necklace", "franco", "14K", "Y", 1.5, 18, collection="womens-necklaces", compare=True)
chain("Round Box Necklace", "box", "925", "S", 1.5, 18, collection="womens-necklaces", compare=True)

# ---- women's pendants
pendant("Heart Pendant", "heart", "14K", "Y", 3.2, collection="womens-pendants", badges=["Best seller"], chain_in=18)
pendant("Heart Pendant", "heart", "14K", "R", 4.0, stone="dia", ct=0.5, collection="womens-pendants", chain_in=18)
pendant("Heart Pendant", "heart", "14K", "W", 4.0, stone="lab", ct=0.5, collection="womens-pendants", badges=["New"], chain_in=18)
pendant("Initial Pendant", "initial", "14K", "Y", 2.4, letter="S", collection="womens-pendants", badges=["Best seller"], chain_in=18)
pendant("Initial Pendant", "initial", "14K", "Y", 3.1, stone="dia", ct=0.3, letter="E", collection="womens-pendants", chain_in=18)
pendant("Initial Pendant", "initial", "14K", "R", 3.1, stone="lab", ct=0.3, letter="K", collection="womens-pendants", compare=True, chain_in=18)
pendant("Cross Pendant", "cross", "14K", "Y", 2.8, collection="womens-pendants", chain_in=18)
pendant("Cross Pendant", "cross", "14K", "W", 3.4, stone="dia", ct=0.35, collection="womens-pendants", badges=["Best seller"], chain_in=18)
pendant("Pear Drop Pendant", "drop", "14K", "W", 2.6, stone="dia", ct=0.75, collection="womens-pendants", badges=["New"], chain_in=18)
pendant("Pear Drop Pendant", "drop", "14K", "Y", 2.6, stone="sap", ct=1.0, collection="womens-pendants", chain_in=18)
pendant("Pear Drop Pendant", "drop", "14K", "Y", 2.6, stone="eme", ct=0.9, collection="womens-pendants", compare=True, chain_in=18)
pendant("Evil Eye Pendant", "eye", "14K", "Y", 2.9, stone="sap", ct=0.2, collection="womens-pendants", badges=["Best seller"], chain_in=18)
pendant("Evil Eye Pendant", "eye", "14K", "W", 2.9, stone="dia", ct=0.25, collection="womens-pendants", chain_in=18)
pendant("Round Medallion Pendant", "medallion", "14K", "Y", 5.5, collection="womens-pendants", chain_in=18)
pendant("Star Pendant", "star", "14K", "Y", 2.5, stone="dia", ct=0.2, collection="womens-pendants", compare=True, chain_in=18)
pendant("Heart Pendant", "heart", "925", "S", 3.5, collection="womens-pendants", compare=True, chain_in=18)

# ---- women's rings
ring("Solitaire Engagement Ring", "solitaire", "14K", "W", 3.2, stone="dia", ct=1.0, collection="womens-rings", engagement=True, badges=["Best seller"], shape="round")
ring("Solitaire Engagement Ring", "solitaire", "14K", "Y", 3.2, stone="dia", ct=1.5, collection="womens-rings", engagement=True, shape="oval")
ring("Solitaire Engagement Ring", "solitaire", "18K", "W", 3.4, stone="dia", ct=2.0, collection="womens-rings", engagement=True, shape="round", badges=["New"])
ring("Solitaire Engagement Ring", "solitaire", "14K", "W", 3.2, stone="lab", ct=2.0, collection="womens-rings", engagement=True, shape="oval", badges=["Best seller"])
ring("Solitaire Engagement Ring", "solitaire", "14K", "Y", 3.2, stone="lab", ct=3.0, collection="womens-rings", engagement=True, shape="emerald")
ring("Hidden Halo Engagement Ring", "halo", "14K", "W", 3.6, stone="dia", ct=1.2, collection="womens-rings", engagement=True, shape="cushion")
ring("Halo Engagement Ring", "halo", "14K", "W", 3.8, stone="lab", ct=1.5, collection="womens-rings", engagement=True, shape="round", compare=True)
ring("Three Stone Engagement Ring", "three-stone", "14K", "Y", 3.9, stone="dia", ct=1.8, collection="womens-rings", engagement=True, shape="oval", badges=["New"])
ring("Three Stone Engagement Ring", "three-stone", "18K", "W", 4.0, stone="lab", ct=2.5, collection="womens-rings", engagement=True, shape="emerald")
ring("Eternity Band", "eternity", "14K", "W", 2.8, stone="dia", ct=1.0, collection="womens-rings", badges=["Best seller"])
ring("Eternity Band", "eternity", "14K", "Y", 2.8, stone="lab", ct=1.0, collection="womens-rings")
ring("Eternity Band", "eternity", "14K", "R", 2.6, stone="dia", ct=0.6, collection="womens-rings", compare=True)
ring("Stacking Band", "band", "14K", "Y", 1.8, collection="womens-rings", badges=["Best seller"])
ring("Stacking Band", "band", "14K", "R", 1.8, collection="womens-rings")
ring("Stacking Band", "band", "14K", "W", 2.0, stone="dia", ct=0.15, collection="womens-rings", badges=["New"])
ring("Cocktail Ring", "solitaire", "14K", "Y", 5.0, stone="eme", ct=2.0, collection="womens-rings", shape="emerald")
ring("Cocktail Ring", "solitaire", "14K", "W", 5.0, stone="sap", ct=2.2, collection="womens-rings", shape="oval", compare=True)
ring("Cocktail Ring", "solitaire", "14K", "Y", 5.0, stone="rub", ct=1.6, collection="womens-rings", shape="cushion")
ring("Signet Ring", "signet", "14K", "Y", 4.5, collection="womens-rings", compare=True)

# ---- women's earrings
earrings("Round Diamond Studs", "studs", "14K", "W", 1.2, stone="dia", ct=0.5, collection="womens-earrings", badges=["Best seller"])
earrings("Round Diamond Studs", "studs", "14K", "W", 1.6, stone="dia", ct=1.0, collection="womens-earrings", badges=["Best seller"])
earrings("Round Diamond Studs", "studs", "14K", "Y", 1.6, stone="lab", ct=1.0, collection="womens-earrings")
earrings("Round Diamond Studs", "studs", "14K", "W", 2.4, stone="lab", ct=2.0, collection="womens-earrings", badges=["New"])
earrings("Round Diamond Studs", "studs", "14K", "W", 2.0, stone="dia", ct=1.5, collection="womens-earrings", compare=True)
earrings("Huggie Hoops", "hoops", "14K", "Y", 1.8, collection="womens-earrings", badges=["Best seller"])
earrings("Huggie Hoops", "hoops", "14K", "Y", 2.0, stone="dia", ct=0.3, collection="womens-earrings")
earrings("Large Hoops", "hoops", "14K", "Y", 4.2, collection="womens-earrings", badges=["New"])
earrings("Large Hoops", "hoops", "14K", "W", 4.2, collection="womens-earrings", compare=True)
earrings("Pear Drop Earrings", "drops", "14K", "W", 2.6, stone="dia", ct=1.2, collection="womens-earrings")
earrings("Pear Drop Earrings", "drops", "14K", "Y", 2.6, stone="sap", ct=1.4, collection="womens-earrings", badges=["New"])
earrings("Cluster Studs", "cluster", "14K", "W", 1.8, stone="dia", ct=0.6, collection="womens-earrings")
earrings("Cluster Studs", "cluster", "14K", "Y", 1.8, stone="lab", ct=0.6, collection="womens-earrings", compare=True)
earrings("Baguette Studs", "baguette", "14K", "W", 1.6, stone="dia", ct=0.5, collection="womens-earrings")
earrings("Huggie Hoops", "hoops", "925", "S", 2.0, collection="womens-earrings", compare=True)

# ---- women's bracelets
bracelet("Tennis Bracelet", "tennis-b", "14K", "W", 2.5, 7, stone="dia", collection="womens-bracelets", badges=["Best seller"])
bracelet("Tennis Bracelet", "tennis-b", "14K", "Y", 3, 7, stone="dia", collection="womens-bracelets")
bracelet("Tennis Bracelet", "tennis-b", "14K", "W", 3, 7, stone="lab", collection="womens-bracelets", badges=["New"])
bracelet("Tennis Bracelet", "tennis-b", "14K", "W", 2, 6.5, stone="lab", collection="womens-bracelets", compare=True)
bracelet("Miami Cuban Link Bracelet", "cuban-b", "14K", "Y", 4, 7, collection="womens-bracelets", badges=["Best seller"])
bracelet("Miami Cuban Link Bracelet", "cuban-b", "14K", "R", 3, 7, collection="womens-bracelets")
bracelet("Bangle", "bangle", "14K", "Y", 4, 7, k=0.05, collection="womens-bracelets", badges=["Best seller"])
bracelet("Bangle", "bangle", "14K", "Y", 5, 7, stone="dia", ct=1.2, k=0.05, collection="womens-bracelets", badges=["New"])
bracelet("Bangle", "bangle", "14K", "W", 3, 7, k=0.05, collection="womens-bracelets", compare=True)
bracelet("Paperclip Bracelet", "paperclip-b", "14K", "Y", 4, 7, solid=False, k=0.04, collection="womens-bracelets")
bracelet("Rope Bracelet", "rope-b", "14K", "Y", 2, 7, collection="womens-bracelets", compare=True)
bracelet("Bangle", "bangle", "925", "S", 4, 7, k=0.05, collection="womens-bracelets", compare=True)

# ---- women's watches
watch("Rolex Datejust 31mm Silver Dial Jubilee", 9800, "Silver", 31, "278274", 2022, bracelet="Jubilee", collection="womens-watches", badges=["Best seller"])
watch("Rolex Lady-Datejust 28mm Pink Dial Two-Tone", 12400, "Pink", 28, "279173", 2021, metal="Steel and yellow gold", bracelet="Jubilee", collection="womens-watches", color="T", purity="18K")
watch("Cartier Tank Must Large Silver Dial", 3600, "Silver", 33.7, "WSTA0041", 2023, metal="Stainless steel", bracelet="Leather strap", collection="womens-watches", badges=["New"])
watch("Cartier Panthere Small Two-Tone", 8900, "Silver", 22, "W2PN0006", 2022, metal="Steel and yellow gold", bracelet="Integrated", collection="womens-watches", color="T", purity="18K")
watch("Rolex Datejust 31mm Diamond Dial and Bezel", 21500, "Diamond pave", 31, "278384RBR", 2022, bracelet="Jubilee", collection="womens-watches", diamonds=True, badges=["Best seller"])
watch("Omega Constellation 29mm Mother of Pearl", 4900, "Mother of pearl", 29, "131.10.29.20.55.001", 2021, collection="womens-watches", compare=True)
watch("Audemars Piguet Royal Oak 34mm Silver Dial", 29500, "Silver", 34, "77350ST", 2021, bracelet="Integrated steel", collection="womens-watches")

# ---------------------------------------------------------------- custom gallery
CUSTOM_PROJECTS = [
    dict(title="Bear pendant with pave body", ptype="medallion", color="Y", stone="dia", ct=11.5, price=18500, blurb="14K yellow gold, 11.5 carats of round diamonds, 6 weeks."),
    dict(title="Family crest signet", ptype="signet", color="Y", stone="", ct=0, price=3200, blurb="18K yellow gold, hand engraved, 3 weeks."),
    dict(title="Portrait pendant", ptype="dogtag", color="W", stone="dia", ct=4.2, price=9800, blurb="14K white gold with a hand-cut enamel portrait, 5 weeks."),
    dict(title="Custom name plate", ptype="id", color="Y", stone="dia", ct=2.0, price=5400, blurb="14K yellow gold ID bracelet, block letters in pave, 4 weeks."),
    dict(title="Two-tone rosary", ptype="cross", color="T", stone="dia", ct=3.0, price=7600, blurb="14K two-tone gold, 3 carats, 4 weeks."),
    dict(title="Letter K with baguettes", ptype="initial", color="W", stone="dia", ct=2.6, price=6200, blurb="14K white gold, baguette and round mix, 4 weeks.", letter="K"),
    dict(title="Emerald cocktail ring", ptype="solitaire", color="Y", stone="eme", ct=3.1, price=14800, blurb="18K yellow gold with a 3.1 carat Colombian emerald, 5 weeks."),
    dict(title="Spinning medallion", ptype="medallion", color="Y", stone="multi", ct=6.0, price=12900, blurb="14K yellow gold with a rotating center in multi-color diamonds, 7 weeks."),
    dict(title="Iced Cuban with black diamonds", ptype="cuban", color="Y", stone="blk", ct=14.0, price=21000, blurb="14K yellow gold 10mm, 14 carats of black diamonds, 8 weeks."),
    dict(title="Oval halo in rose gold", ptype="halo", color="R", stone="dia", ct=2.0, price=15600, blurb="18K rose gold, 2 carat oval, 4 weeks."),
    dict(title="Blue sapphire evil eye", ptype="eye", color="Y", stone="sap", ct=0.8, price=2900, blurb="14K yellow gold with sapphires and diamonds, 3 weeks."),
    dict(title="Star with initials", ptype="star", color="W", stone="dia", ct=2.2, price=6900, blurb="14K white gold, VS diamonds, 4 weeks."),
]
for i, c in enumerate(CUSTOM_PROJECTS):
    c["slug"] = slugify(c["title"])
    c["image"] = f"/img/custom/{c['slug']}.svg"
    c.setdefault("letter", "")
    c["purity"] = "14K"

# ---------------------------------------------------------------- reviews
REVIEWS = [
    dict(name="Marcus T.", city="Brooklyn", stars=5, text="Bought a 6mm Cuban for my brother. It came in three days with the appraisal and weighs exactly what the listing said."),
    dict(name="Priya R.", city="Jersey City", stars=5, text="They built my engagement ring from the ring builder. The render matched the ring. My fiancée cried."),
    dict(name="Dre W.", city="Bronx", stars=5, text="Custom pendant took five weeks like they said. Every stone is tight. I have sent four people here."),
    dict(name="Elena K.", city="Manhattan", stars=5, text="Tennis bracelet was resized in the shop while I waited. No charge. That is why I keep coming back."),
    dict(name="Jordan L.", city="Queens", stars=4, text="Watch arrived running a few seconds fast. They regulated it for free the same week. Good people."),
    dict(name="Sam O.", city="Long Island", stars=5, text="Traded in an old chain toward a new rope. Fair number, no games, done in twenty minutes."),
]

FAQ = [
    ("Is the gold real?", "Yes. Every gold piece is stamped 10K, 14K or 18K and tested on an XRF machine before it leaves the shop. Silver is stamped 925."),
    ("Are the diamonds natural or lab-grown?", "Both. Each listing says which. Natural diamonds over 0.5 carats come with a GIA or IGI report. Lab-grown diamonds come with an IGI report."),
    ("Do you make custom pieces?", "Yes. Custom is most of what we do. Start a project online or come to the shop. Most pieces take 3 to 8 weeks."),
    ("Can I finance?", "Yes. We offer 0% financing for 12 months on approved credit, and an in-house layaway plan with 25% down."),
    ("What is your return policy?", "Stock pieces can be returned within 30 days in new condition for a full refund. Custom and resized pieces are final sale."),
    ("Do you ship outside the US?", "Yes. We ship worldwide with full insurance. Duties are paid by the buyer."),
    ("Do you buy gold, diamonds and watches?", "Yes. Bring your pieces to the shop or send photos. We pay in cash, wire or store credit at a 10% bonus."),
    ("Can I see the piece before I buy?", "Yes. Book an appointment and we will have it on the counter when you arrive. We can also video call you from the bench."),
]
