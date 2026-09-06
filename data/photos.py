"""Photo pools (Pexels ids) and the rules that assign them to products.

Pexels license: free for commercial use, no attribution required. Files live in static/img/photos/<id>-<w>.jpg.
"""
import hashlib

POOLS = {
    "chain-cuban-gold": [12155925, 14111400, 26866389, 25724432, 10581731],
    "chain-cuban-white": [16109176, 16109171, 16124758, 16124717, 16109298, 16109266, 16109263],
    "chain-rope-gold": [14111396, 11936873, 26246207, 14111397],
    "chain-rope-white": [16109322, 16109320, 16124724],
    "chain-rope-rose": [14111397, 14111396],
    "chain-tennis": [36189601, 12427695, 24815712, 20141640],
    "chain-other-gold": [10581731, 14111400, 4573790, 26246210, 12155925],
    "chain-silver": [16109176, 16109322, 16124724, 16109320],
    "necklace-women-gold": [28900494, 10120273, 30985153, 6604737, 13924051, 18923968, 13660667, 12194265, 12194380],
    "necklace-women-diamond": [36189601, 12427695, 36599395, 20838859, 24815712],
    "necklace-paperclip": [10120273, 26246210, 13924051, 18923968],
    "necklace-station": [12427695, 12194265, 24815712],
    "necklace-rose": [14111397, 30985153, 13660667],
    "pendant-cross-gold": [6576196, 9022813, 10630343, 9173457, 9173459],
    "pendant-cross-white": [13580633, 12133990, 10407446, 5629377],
    "pendant-medallion": [10217938, 29736434, 29736431, 29736433, 4295007, 6604737],
    "pendant-initial": [34444210, 4889719, 29502933, 33452872, 15967444],
    "pendant-dogtag": [15967441, 15947214, 15967440, 29003596],
    "pendant-star": [4595723, 29193421, 18157530],
    "pendant-women-heart": [13292938, 29193422, 13292955],
    "pendant-women-initial": [4735890, 21235048, 7273395, 7273388],
    "pendant-women-drop": [10944923, 10215179, 18157530, 18157532],
    "pendant-women-eye": [29502933, 34444209, 35933227],
    "pendant-women-cross": [9173459, 9022813, 6576196],
    "pendant-women-medallion": [6604737, 4889719, 29736434],
    "ring-signet": [8433597, 28933799, 30653285, 20429577, 17261921],
    "ring-band-men": [28933799, 30206324, 37488824, 21928764, 5009521, 13340660],
    "ring-cuban": [18716104, 30541171, 13524236, 17261921],
    "ring-eternity": [3091638, 18716104, 31728281, 33222151, 30541187],
    "ring-solitaire": [2732096, 2849742, 15351782, 30162861, 4544718, 12427696],
    "ring-halo": [2735981, 32988751, 5737315, 10976653, 31087451],
    "ring-three-stone": [12427696, 8306529, 10361481, 10976653],
    "ring-band-women": [33222151, 30541187, 5009521, 35205571, 13895021],
    "ring-cocktail": [10361481, 10361483, 32988751, 30162861],
    "earring-studs-white": [5370657, 28389454, 35961143, 5370644, 7479508],
    "earring-studs-gold": [28389453, 35961143, 5737290, 17368722],
    "earring-cluster": [5737290, 10976654, 5370644],
    "earring-baguette": [35933224, 28389454, 5370643],
    "earring-hoops": [26592836, 12194345, 20033873, 38909373, 12144978, 18075559, 15785528, 12194348],
    "earring-drops": [7981566, 2849743, 7541801, 31605846],
    "earring-cross": [29193421, 29193422],
    "earring-black": [35961143, 5370643],
    "bracelet-cuban-gold": [38827895, 12194323, 28933800, 10341191, 14509641],
    "bracelet-cuban-white": [16109309, 16124735, 9649313, 16109171],
    "bracelet-tennis": [20141640, 5370647, 31757022, 33343009, 10030284, 12194332],
    "bracelet-rope": [12194323, 14509676, 3641059],
    "bracelet-id": [11476471, 15491661, 38827915],
    "bracelet-bangle": [38827895, 37485309, 37485307, 32874211, 38827915],
    "bracelet-silver": [9649313, 16124735],
    "watch-steel": [9561300, 38796256, 10414755, 37322602, 190819, 33511755],
    "watch-gold": [3809175, 25052866, 14569229],
    "watch-two-tone": [3809175, 14569229],
    "watch-women": [4276458, 37050003, 3419331, 19766307, 16587541],
    "watch-diamond": [37322602, 3809175],
    "diamonds": [8395024, 5362404, 5442447, 39017189, 13648409],
    "workshop": [11041197, 23232400, 5912127, 37250032, 8327602, 1050321, 37401950, 6263104, 30904849, 15955333, 6262835],
    "look-women": [20838859, 30985153, 36189601, 10120273, 28900494],
    "look-men": [21370302, 27857542, 26866389, 9742272, 16109292],
}

# Editorial photos used by name in templates. Downloaded at banner size.
FEATURES = {
    "hero": 12155925,
    "look-men": 21370302,
    "look-women": 20838859,
    "engagement": 2732096,
    "workshop": 11041197,
    "custom-hero": 37250032,
    "diamonds": 8395024,
    "about": 23232400,
    "showroom": 29043373,
    "builder": 2735981,
    "sketch": 37401950,
    "loupe": 5912127,
    "torch": 15955333,
    "polish": 6262835,
    "watchmaker": 8327602,
    "mega-men": 16109292,
    "mega-women": 30985153,
}

RING_SETTING_PHOTOS = {
    "solitaire": 2732096, "hidden-halo": 15351782, "halo": 2735981, "three-stone": 12427696, "pave": 3091638, "cathedral": 2849742,
}

SIZES = {"card": 640, "large": 1280, "banner": 1920}


def photo(pid, size="card"):
    return f"/img/photos/{pid}-{SIZES[size]}.jpg"


def _pool_for(p):
    kind, t, color, stone = p["kind"], p["ptype"], p["color"], p.get("stone", "")
    white = color in ("W", "S")
    if kind == "chains":
        if p["gender"] == "womens":
            if t == "tennis" or stone in ("dia", "lab"):
                return "necklace-women-diamond"
            if t == "paperclip":
                return "necklace-paperclip"
            if t == "station":
                return "necklace-station"
            if color == "R":
                return "necklace-rose"
            return "necklace-women-gold"
        if color == "S":
            return "chain-silver"
        if t == "tennis":
            return "chain-tennis"
        if t == "cuban":
            return "chain-cuban-white" if white else "chain-cuban-gold"
        if t == "rope":
            return "chain-rope-white" if white else "chain-rope-rose" if color == "R" else "chain-rope-gold"
        return "chain-cuban-white" if white else "chain-other-gold"
    if kind == "pendants":
        if p["gender"] == "womens":
            return {"heart": "pendant-women-heart", "initial": "pendant-women-initial", "drop": "pendant-women-drop", "eye": "pendant-women-eye",
                    "cross": "pendant-women-cross", "medallion": "pendant-women-medallion", "star": "pendant-star"}.get(t, "pendant-women-initial")
        if t == "cross":
            return "pendant-cross-white" if white else "pendant-cross-gold"
        return {"medallion": "pendant-medallion", "initial": "pendant-initial", "dogtag": "pendant-dogtag", "star": "pendant-star"}.get(t, "pendant-medallion")
    if kind == "rings":
        if p["gender"] == "womens":
            if p.get("engagement"):
                return {"solitaire": "ring-solitaire", "halo": "ring-halo", "three-stone": "ring-three-stone"}.get(t, "ring-solitaire")
            if t == "solitaire":
                return "ring-cocktail"
            if t == "eternity":
                return "ring-eternity"
            if t == "signet":
                return "ring-signet"
            return "ring-band-women"
        return {"signet": "ring-signet", "cuban-ring": "ring-cuban", "eternity": "ring-eternity", "band": "ring-band-men", "halo": "ring-cuban", "solitaire": "ring-cocktail"}.get(t, "ring-signet")
    if kind == "earrings":
        if stone == "blk":
            return "earring-black"
        return {"studs": "earring-studs-white" if white else "earring-studs-gold", "single": "earring-studs-white", "cluster": "earring-cluster",
                "baguette": "earring-baguette", "hoops": "earring-hoops", "drops": "earring-drops", "cross-e": "earring-cross"}.get(t, "earring-studs-white")
    if kind == "bracelets":
        if color == "S":
            return "bracelet-silver"
        return {"cuban-b": "bracelet-cuban-white" if white else "bracelet-cuban-gold", "tennis-b": "bracelet-tennis", "rope-b": "bracelet-rope",
                "id": "bracelet-id", "bangle": "bracelet-bangle", "franco-b": "bracelet-cuban-gold", "paperclip-b": "bracelet-rope"}.get(t, "bracelet-cuban-gold")
    if kind == "watches":
        if p["gender"] == "womens":
            return "watch-women"
        if stone:
            return "watch-diamond"
        if color == "T":
            return "watch-two-tone"
        if color == "Y":
            return "watch-gold"
        return "watch-steel"
    return "workshop"


def assign_photos(products, custom_projects):
    """Give every product 3 photos from its pool, rotated so neighbours differ."""
    counters = {}
    for p in products:
        pool_name = _pool_for(p)
        pool = POOLS[pool_name]
        start = counters.get(pool_name, 0)
        counters[pool_name] = start + 1
        ids = [pool[(start + k) % len(pool)] for k in range(min(3, len(pool)))]
        p["pool"] = pool_name
        p["photos"] = [dict(id=i, card=photo(i, "card"), large=photo(i, "large")) for i in ids]
        p["image"] = p["photos"][0]["card"]
        p["image_large"] = p["photos"][0]["large"]
    custom_pools = {"medallion": "pendant-medallion", "signet": "ring-signet", "dogtag": "pendant-dogtag", "id": "bracelet-id", "cross": "pendant-cross-gold",
                    "initial": "pendant-initial", "solitaire": "ring-cocktail", "cuban": "chain-cuban-gold", "halo": "ring-halo", "eye": "pendant-women-eye", "star": "pendant-star"}
    seen = {}
    for c in custom_projects:
        pool = POOLS[custom_pools.get(c["ptype"], "workshop")]
        n = seen.get(c["ptype"], 0)
        seen[c["ptype"]] = n + 1
        c["image"] = photo(pool[(n + 1) % len(pool)], "card")
        c["image_large"] = photo(pool[(n + 1) % len(pool)], "large")


def all_downloads():
    """(id, width) pairs needed on disk."""
    out = set()
    for ids in POOLS.values():
        for i in ids:
            out.add((i, SIZES["card"]))
            out.add((i, SIZES["large"]))
    for i in FEATURES.values():
        out.add((i, SIZES["banner"]))
        out.add((i, SIZES["large"]))
        out.add((i, SIZES["card"]))
    for i in RING_SETTING_PHOTOS.values():
        out.add((i, SIZES["card"]))
        out.add((i, SIZES["large"]))
    return sorted(out)
