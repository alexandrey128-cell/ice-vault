"""Procedural SVG renders for products, custom projects, the hero diamond and the logo mark."""
import math
import random

METALS = {
    "Y": ("#FFF6C2", "#EFCB5A", "#BD8E22", "#7E5A16"),
    "W": ("#FFFFFF", "#E2E8EF", "#A9B4C0", "#68737F"),
    "R": ("#FFE8DD", "#EDB39E", "#C67C64", "#8A4F3F"),
    "S": ("#FFFFFF", "#DDE3EA", "#9BA5B0", "#5F6973"),
    "T": ("#FFF6C2", "#EFCB5A", "#BD8E22", "#7E5A16"),
    "Steel": ("#FFFFFF", "#D9DFE6", "#9AA4AF", "#5C6670"),
}
STONES = {
    "dia": ("#FFFFFF", "#E4F3FF", "#9CC7EA"),
    "lab": ("#FFFFFF", "#E4F3FF", "#9CC7EA"),
    "blk": ("#7B838E", "#2B3038", "#0B0D11"),
    "eme": ("#B9F5D5", "#22B86E", "#0A5A37"),
    "rub": ("#FFC1C9", "#DC2442", "#6B0A1C"),
    "sap": ("#B7CDFF", "#2F62DC", "#112A6E"),
    "opal": ("#FFFFFF", "#E1EEFF", "#F5D6FF"),
    "": ("#FFFFFF", "#E4F3FF", "#9CC7EA"),
}
MULTI = ["rub", "sap", "eme", "dia", "Y"]


def _metal(color):
    return METALS.get(color, METALS["Y"])


def defs(color, stone="", seed=0):
    h, m, s, d = _metal(color)
    out = [f'<linearGradient id="m" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{h}"/><stop offset=".42" stop-color="{m}"/><stop offset=".78" stop-color="{s}"/><stop offset="1" stop-color="{d}"/></linearGradient>',
           f'<linearGradient id="mr" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{h}"/><stop offset=".45" stop-color="{m}"/><stop offset=".8" stop-color="{s}"/><stop offset="1" stop-color="{d}"/></linearGradient>',
           f'<linearGradient id="md" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{s}"/><stop offset="1" stop-color="{d}"/></linearGradient>',
           '<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="10" stdDeviation="10" flood-color="#000" flood-opacity=".5"/></filter>',
           '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2"/></filter>']
    # white metal for two tone accents
    wh = METALS["W"]
    out.append(f'<linearGradient id="mw" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{wh[0]}"/><stop offset=".45" stop-color="{wh[1]}"/><stop offset=".8" stop-color="{wh[2]}"/><stop offset="1" stop-color="{wh[3]}"/></linearGradient>')
    for key, (a, b, c) in STONES.items():
        k = key or "none"
        out.append(f'<radialGradient id="s-{k}" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="{a}"/><stop offset=".55" stop-color="{b}"/><stop offset="1" stop-color="{c}"/></radialGradient>')
    out.append('<radialGradient id="s-Y" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="#FFF9D6"/><stop offset=".55" stop-color="#F3D35E"/><stop offset="1" stop-color="#A67C12"/></radialGradient>')
    return "<defs>" + "".join(out) + "</defs>"


def svg(body, color, stone="", size=600):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}" role="img">'
            f'{defs(color, stone)}<g filter="url(#sh)">{body}</g></svg>')


# ------------------------------------------------------------ path sampling
def bezier(p0, p1, p2, t):
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
    return x, y


def sample_curve(fn, n=600):
    pts = [fn(i / n) for i in range(n + 1)]
    acc = [0.0]
    for i in range(1, len(pts)):
        acc.append(acc[-1] + math.dist(pts[i - 1], pts[i]))
    return pts, acc


def along(fn, spacing, start=0.0, n=600):
    """Yield (x, y, angle_deg) at equal arc-length spacing along fn(t)."""
    pts, acc = sample_curve(fn, n)
    total = acc[-1]
    d = start
    i = 0
    out = []
    while d <= total:
        while i < len(acc) - 1 and acc[i + 1] < d:
            i += 1
        j = min(i + 1, len(pts) - 1)
        seg = acc[j] - acc[i] or 1
        f = (d - acc[i]) / seg
        x = pts[i][0] + (pts[j][0] - pts[i][0]) * f
        y = pts[i][1] + (pts[j][1] - pts[i][1]) * f
        k0, k1 = max(i - 3, 0), min(i + 3, len(pts) - 1)
        ang = math.degrees(math.atan2(pts[k1][1] - pts[k0][1], pts[k1][0] - pts[k0][0]))
        out.append((x, y, ang))
        d += spacing
    return out


def necklace_curve(depth=930, top=70, x0=95, x1=505):
    return lambda t: bezier((x0, top), (300, depth), (x1, top), t)


def loop_curve(cx=300, cy=300, rx=205, ry=150):
    return lambda t: (cx + rx * math.cos(2 * math.pi * t - math.pi / 2), cy + ry * math.sin(2 * math.pi * t - math.pi / 2))


def v_curve(x0=120, x1=480, top=60, cy=250):
    """Thin pendant chain: two lines meeting at the bail."""
    return [lambda t: (x0 + (300 - x0) * t, top + (cy - top) * t), lambda t: (x1 + (300 - x1) * t, top + (cy - top) * t)]


# ------------------------------------------------------------ primitives
def gem(x, y, r, kind="dia", i=0, facets=True):
    if kind == "multi":
        kind = MULTI[i % len(MULTI)]
    k = kind or "none"
    out = [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="url(#s-{k})" stroke="#0A0E14" stroke-opacity=".35" stroke-width="{max(r*0.08,0.6):.2f}"/>']
    if facets and r >= 5:
        lines = []
        for a in range(0, 360, 45):
            ax, ay = x + r * 0.96 * math.cos(math.radians(a)), y + r * 0.96 * math.sin(math.radians(a))
            lines.append(f'M{x:.1f},{y:.1f}L{ax:.1f},{ay:.1f}')
        out.append(f'<path d="{"".join(lines)}" stroke="#fff" stroke-opacity=".28" stroke-width="{max(r*0.05,0.5):.2f}" fill="none"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*0.5:.1f}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="{max(r*0.05,0.5):.2f}"/>')
    out.append(f'<circle cx="{x - r*0.35:.1f}" cy="{y - r*0.38:.1f}" r="{r*0.22:.1f}" fill="#fff" fill-opacity=".85"/>')
    return "".join(out)


def stone_shape(x, y, w, h, shape, kind="dia"):
    """Fancy cut center stones. Returns svg."""
    k = kind if kind in STONES else "dia"
    st = f'fill="url(#s-{k})" stroke="#0A0E14" stroke-opacity=".35" stroke-width="1.2"'
    hl = f'<ellipse cx="{x - w*0.22:.1f}" cy="{y - h*0.28:.1f}" rx="{w*0.14:.1f}" ry="{h*0.1:.1f}" fill="#fff" fill-opacity=".8"/>'
    if shape == "round":
        return gem(x, y, w / 2, kind)
    if shape == "oval":
        body = f'<ellipse cx="{x}" cy="{y}" rx="{w/2:.1f}" ry="{h/2:.1f}" {st}/><ellipse cx="{x}" cy="{y}" rx="{w/4:.1f}" ry="{h/4:.1f}" fill="none" stroke="#fff" stroke-opacity=".35"/>'
    elif shape == "emerald":
        c = w * 0.18
        pts = f'{x-w/2+c},{y-h/2} {x+w/2-c},{y-h/2} {x+w/2},{y-h/2+c} {x+w/2},{y+h/2-c} {x+w/2-c},{y+h/2} {x-w/2+c},{y+h/2} {x-w/2},{y+h/2-c} {x-w/2},{y-h/2+c}'
        body = f'<polygon points="{pts}" {st}/><rect x="{x-w*0.3:.1f}" y="{y-h*0.3:.1f}" width="{w*0.6:.1f}" height="{h*0.6:.1f}" fill="none" stroke="#fff" stroke-opacity=".35"/><rect x="{x-w*0.15:.1f}" y="{y-h*0.15:.1f}" width="{w*0.3:.1f}" height="{h*0.3:.1f}" fill="none" stroke="#fff" stroke-opacity=".3"/>'
    elif shape == "cushion":
        body = f'<rect x="{x-w/2:.1f}" y="{y-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{w*0.3:.1f}" {st}/><rect x="{x-w/4:.1f}" y="{y-h/4:.1f}" width="{w/2:.1f}" height="{h/2:.1f}" rx="{w*0.15:.1f}" fill="none" stroke="#fff" stroke-opacity=".35"/>'
    elif shape == "pear":
        body = f'<path d="M{x},{y-h/2} C{x+w*0.75},{y-h*0.1} {x+w/2},{y+h/2} {x},{y+h/2} C{x-w/2},{y+h/2} {x-w*0.75},{y-h*0.1} {x},{y-h/2}Z" {st}/>'
    elif shape == "marquise":
        body = f'<path d="M{x},{y-h/2} C{x+w*0.85},{y-h*0.2} {x+w*0.85},{y+h*0.2} {x},{y+h/2} C{x-w*0.85},{y+h*0.2} {x-w*0.85},{y-h*0.2} {x},{y-h/2}Z" {st}/>'
    elif shape == "princess":
        body = f'<rect x="{x-w/2:.1f}" y="{y-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="2" {st}/><path d="M{x-w/2},{y-h/2}L{x+w/2},{y+h/2}M{x+w/2},{y-h/2}L{x-w/2},{y+h/2}" stroke="#fff" stroke-opacity=".3"/>'
    elif shape == "heart":
        body = f'<path d="M{x},{y+h/2} C{x-w*0.9},{y-h*0.1} {x-w*0.35},{y-h*0.75} {x},{y-h*0.2} C{x+w*0.35},{y-h*0.75} {x+w*0.9},{y-h*0.1} {x},{y+h/2}Z" {st}/>'
    elif shape == "radiant":
        c = w * 0.15
        pts = f'{x-w/2+c},{y-h/2} {x+w/2-c},{y-h/2} {x+w/2},{y-h/2+c} {x+w/2},{y+h/2-c} {x+w/2-c},{y+h/2} {x-w/2+c},{y+h/2} {x-w/2},{y+h/2-c} {x-w/2},{y-h/2+c}'
        body = f'<polygon points="{pts}" {st}/><path d="M{x-w/2+c},{y-h/2}L{x},{y}L{x+w/2-c},{y-h/2}M{x-w/2+c},{y+h/2}L{x},{y}L{x+w/2-c},{y+h/2}M{x-w/2},{y-h/2+c}L{x},{y}L{x-w/2},{y+h/2-c}M{x+w/2},{y-h/2+c}L{x},{y}L{x+w/2},{y+h/2-c}" stroke="#fff" stroke-opacity=".3" fill="none"/>'
    else:
        return gem(x, y, w / 2, kind)
    return body + hl


def prongs(x, y, r, n=4, color_grad="m"):
    out = []
    for i in range(n):
        a = math.radians(45 + i * (360 / n))
        px, py = x + r * math.cos(a), y + r * math.sin(a)
        out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{max(r*0.16,2):.1f}" fill="url(#{color_grad})" stroke="#0A0E14" stroke-opacity=".4" stroke-width=".8"/>')
    return "".join(out)


def link_ellipse(x, y, ang, L, W, thick, grad="m"):
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f})">'
            f'<ellipse rx="{L/2:.1f}" ry="{W/2:.1f}" fill="none" stroke="#0A0E14" stroke-opacity=".55" stroke-width="{thick+2.5:.1f}"/>'
            f'<ellipse rx="{L/2:.1f}" ry="{W/2:.1f}" fill="none" stroke="url(#{grad})" stroke-width="{thick:.1f}"/>'
            f'<ellipse rx="{L/2:.1f}" ry="{W/2:.1f}" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="{thick*0.22:.1f}" transform="translate(0,{-thick*0.28:.1f})" stroke-dasharray="{L*0.6:.0f} {L*1.4:.0f}"/>'
            f'</g>')


# ------------------------------------------------------------ chain styles
def cuban_links(curve, width_mm, stone="", start=0.0, thick_scale=1.0):
    W = 16 + min(width_mm, 8) * 4.2   # link width px, capped so 10mm+ chains stay readable
    L = W * 1.7
    thick = W * 0.36 * thick_scale
    pts = along(curve, L * 0.58, start)
    out = []
    for i, (x, y, a) in enumerate(pts):
        grad = "m" if i % 2 == 0 else "mr"
        out.append(link_ellipse(x, y, a, L, W, thick, grad))
        if stone:
            r = max(thick * 0.28, 1.6)
            for k in (-1, 1):
                out.append(gem(x + k * L * 0.28 * math.cos(math.radians(a)) - W * 0.5 * math.sin(math.radians(a)) * 0,
                                 y + k * L * 0.28 * math.sin(math.radians(a)), r, stone, i, facets=False))
    return "".join(out)


def rope(curve, width_mm, start=0.0):
    w = 10 + width_mm * 4.2
    pts, _ = sample_curve(curve, 200)
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    out = [f'<path d="{d}" fill="none" stroke="#0A0E14" stroke-opacity=".6" stroke-width="{w+3:.1f}" stroke-linecap="round"/>',
           f'<path d="{d}" fill="none" stroke="url(#md)" stroke-width="{w:.1f}" stroke-linecap="round"/>']
    for i, (x, y, a) in enumerate(along(curve, w * 0.42, start)):
        ang = a + 58
        dx, dy = math.cos(math.radians(ang)) * w * 0.5, math.sin(math.radians(ang)) * w * 0.5
        out.append(f'<line x1="{x-dx:.1f}" y1="{y-dy:.1f}" x2="{x+dx:.1f}" y2="{y+dy:.1f}" stroke="url(#m)" stroke-width="{w*0.3:.1f}" stroke-linecap="round"/>')
        out.append(f'<line x1="{x-dx*0.7:.1f}" y1="{y-dy*0.7:.1f}" x2="{x+dx*0.2:.1f}" y2="{y+dy*0.2:.1f}" stroke="#fff" stroke-opacity=".35" stroke-width="{w*0.09:.1f}" stroke-linecap="round"/>')
    return "".join(out)


def tennis(curve, width_mm, stone="dia", start=0.0):
    s = 12 + width_mm * 4.2
    out = []
    for i, (x, y, a) in enumerate(along(curve, s * 1.02, start)):
        out.append(f'<g transform="translate({x:.1f},{y:.1f}) rotate({a:.1f})"><rect x="{-s/2:.1f}" y="{-s/2:.1f}" width="{s:.1f}" height="{s:.1f}" rx="{s*0.18:.1f}" fill="url(#m)" stroke="#0A0E14" stroke-opacity=".5" stroke-width="1.2"/></g>')
        out.append(gem(x, y, s * 0.38, stone, i, facets=s > 16))
    return "".join(out)


def box_links(curve, width_mm, start=0.0, franco=False):
    s = 12 + width_mm * 4.5
    out = []
    for i, (x, y, a) in enumerate(along(curve, s * 0.95, start)):
        grad = "m" if i % 2 == 0 else "mr"
        rot = a + (45 if franco and i % 2 else 0)
        out.append(f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot:.1f})"><rect x="{-s/2:.1f}" y="{-s/2:.1f}" width="{s:.1f}" height="{s:.1f}" rx="{s*0.22:.1f}" fill="url(#{grad})" stroke="#0A0E14" stroke-opacity=".55" stroke-width="1.4"/><rect x="{-s*0.3:.1f}" y="{-s*0.3:.1f}" width="{s*0.6:.1f}" height="{s*0.6:.1f}" rx="{s*0.12:.1f}" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="1"/></g>')
    return "".join(out)


def figaro(curve, width_mm, start=0.0):
    W = 14 + width_mm * 4.4
    thick = W * 0.34
    pattern = [1, 1, 1, 2.4]
    pts, acc = sample_curve(curve)
    total = acc[-1]
    out = []
    d = start
    i = 0
    idx = 0
    while d < total:
        Lm = pattern[idx % 4]
        L = W * 1.5 * Lm
        (x, y, a), = along(lambda t, f=curve: f(t), 10 ** 9, d)[:1] or [(0, 0, 0)]
        out.append(link_ellipse(x, y, a, L, W, thick, "m" if idx % 2 else "mr"))
        d += L * 0.62
        idx += 1
    return "".join(out)


def paperclip(curve, width_mm, start=0.0):
    W = 14 + width_mm * 3.2
    L = W * 2.6
    thick = W * 0.3
    out = []
    for i, (x, y, a) in enumerate(along(curve, L * 0.62, start)):
        grad = "m" if i % 2 == 0 else "mr"
        out.append(f'<g transform="translate({x:.1f},{y:.1f}) rotate({a:.1f})"><rect x="{-L/2:.1f}" y="{-W/2:.1f}" width="{L:.1f}" height="{W:.1f}" rx="{W/2:.1f}" fill="none" stroke="#0A0E14" stroke-opacity=".55" stroke-width="{thick+2.5:.1f}"/><rect x="{-L/2:.1f}" y="{-W/2:.1f}" width="{L:.1f}" height="{W:.1f}" rx="{W/2:.1f}" fill="none" stroke="url(#{grad})" stroke-width="{thick:.1f}"/></g>')
    return "".join(out)


def station(curve, width_mm, stone="dia", start=0.0):
    pts, _ = sample_curve(curve, 200)
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    out = [f'<path d="{d}" fill="none" stroke="#0A0E14" stroke-opacity=".5" stroke-width="5"/>', f'<path d="{d}" fill="none" stroke="url(#m)" stroke-width="3"/>']
    for i, (x, y, a) in enumerate(along(curve, 62, start + 20)):
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="url(#m)" stroke="#0A0E14" stroke-opacity=".5"/>')
        out.append(gem(x, y, 8.5, stone, i))
    return "".join(out)


def cable(curve, start=0.0, size=7):
    out = []
    for i, (x, y, a) in enumerate(along(curve, size * 0.9, start)):
        out.append(link_ellipse(x, y, a + (0 if i % 2 else 90) * 0, size * 1.6, size, size * 0.35, "m" if i % 2 else "mr"))
    return "".join(out)


def thin_chain(kind="cable"):
    return "".join(cable(c, 0, 7) for c in v_curve())


CHAINS = {
    "cuban": lambda c, w, st: cuban_links(c, w, st),
    "rope": lambda c, w, st: rope(c, w),
    "tennis": lambda c, w, st: tennis(c, w, st or "dia"),
    "franco": lambda c, w, st: box_links(c, w, franco=True),
    "box": lambda c, w, st: box_links(c, w),
    "figaro": lambda c, w, st: figaro(c, w),
    "paperclip": lambda c, w, st: paperclip(c, w),
    "station": lambda c, w, st: station(c, w, st or "dia"),
}


def clasp(x, y, w):
    return f'<rect x="{x-w*0.9:.1f}" y="{y-w*0.55:.1f}" width="{w*1.8:.1f}" height="{w*1.1:.1f}" rx="{w*0.2:.1f}" fill="url(#m)" stroke="#0A0E14" stroke-opacity=".55" stroke-width="1.5"/><rect x="{x-w*0.5:.1f}" y="{y-w*0.2:.1f}" width="{w:.1f}" height="{w*0.4:.1f}" rx="2" fill="#0A0E14" fill-opacity=".35"/>'


# ------------------------------------------------------------ pendants
def pendant_body(ptype, color, stone, ct, letter, cx=300, cy=400, scale=1.0):
    out = []
    pave = stone in ("dia", "lab", "blk", "multi") and ct > 0
    S = scale
    if ptype == "cross":
        w, h, t = 120 * S, 175 * S, 34 * S
        out.append(f'<rect x="{cx-t/2}" y="{cy-h/2}" width="{t}" height="{h}" rx="{t*0.25}" fill="url(#m)" stroke="#0A0E14" stroke-opacity=".55" stroke-width="2"/>')
        out.append(f'<rect x="{cx-w/2}" y="{cy-h/2+h*0.27}" width="{w}" height="{t}" rx="{t*0.25}" fill="url(#mr)" stroke="#0A0E14" stroke-opacity=".55" stroke-width="2"/>')
        out.append(f'<rect x="{cx-t/2}" y="{cy-h/2}" width="{t}" height="{h}" rx="{t*0.25}" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="1.5"/>')
        if pave:
            r = t * 0.13
            i = 0
            for yy in range(int(cy - h / 2 + r * 2), int(cy + h / 2 - r), int(r * 2.3)):
                for k in (-1, 0, 1):
                    out.append(gem(cx + k * r * 2.3, yy, r, stone, i, facets=False)); i += 1
            yy = cy - h / 2 + h * 0.27 + t / 2
            for xx in range(int(cx - w / 2 + r * 2), int(cx + w / 2 - r), int(r * 2.3)):
                if abs(xx - cx) > t / 2:
                    for k in (-1, 0, 1):
                        out.append(gem(xx, yy + k * r * 2.3, r, stone, i, facets=False)); i += 1
        bail_y = cy - h / 2
    elif ptype in ("medallion",):
        R = 105 * S
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#m)" stroke="#0A0E14" stroke-opacity=".55" stroke-width="2"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{R*0.8}" fill="url(#mr)" stroke="#0A0E14" stroke-opacity=".35" stroke-width="1.5"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{R*0.62}" fill="url(#md)" stroke="#0A0E14" stroke-opacity=".4"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{R*0.62}" fill="none" stroke="#fff" stroke-opacity=".2" stroke-width="2"/>')
        if pave:
            n = 22
            for i in range(n):
                a = 2 * math.pi * i / n
                out.append(gem(cx + R * 0.9 * math.cos(a), cy + R * 0.9 * math.sin(a), R * 0.075, stone, i, facets=False))
            out.append(gem(cx, cy, R * 0.22, stone if stone != "blk" else "dia"))
        else:
            for i in range(8):
                a = 2 * math.pi * i / 8 + math.pi / 8
                out.append(f'<line x1="{cx + R*0.64*math.cos(a):.1f}" y1="{cy + R*0.64*math.sin(a):.1f}" x2="{cx + R*0.78*math.cos(a):.1f}" y2="{cy + R*0.78*math.sin(a):.1f}" stroke="#0A0E14" stroke-opacity=".35" stroke-width="3"/>')
            if stone in ("eme", "rub", "sap"):
                out.append(gem(cx, cy, R * 0.24, stone))
        bail_y = cy - R
    elif ptype == "initial":
        out.append(f'<text x="{cx}" y="{cy+70*S}" text-anchor="middle" font-family="Georgia, \'Times New Roman\', serif" font-weight="700" font-size="{210*S}" fill="url(#m)" stroke="#0A0E14" stroke-opacity=".55" stroke-width="2">{letter or "A"}</text>')
        out.append(f'<text x="{cx}" y="{cy+70*S}" text-anchor="middle" font-family="Georgia, \'Times New Roman\', serif" font-weight="700" font-size="{210*S}" fill="none" stroke="#fff" stroke-opacity=".22" stroke-width="1.5">{letter or "A"}</text>')
        if pave:
            r = 6 * S
            i = 0
            for yy in range(int(cy - 55 * S), int(cy + 55 * S), int(r * 2.4)):
                for xx in range(int(cx - 40 * S), int(cx + 40 * S), int(r * 2.4)):
                    if (xx - cx) ** 2 / (48 * S) ** 2 + (yy - cy) ** 2 / (60 * S) ** 2 < 1:
                        out.append(gem(xx, yy, r, stone, i, facets=False)); i += 1
        bail_y = cy - 85 * S
    elif ptype == "dogtag":
        w, h = 120 * S, 200 * S
        out.append(f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="{w*0.22}" fill="url(#m)" stroke="#0A0E14" stroke-opacity=".55" stroke-width="2"/>')
        out.append(f'<rect x="{cx-w/2+8}" y="{cy-h/2+8}" width="{w-16}" height="{h-16}" rx="{w*0.18}" fill="none" stroke="#fff" stroke-opacity=".22" stroke-width="1.5"/>')
        out.append(f'<circle cx="{cx}" cy="{cy-h/2+18}" r="7" fill="#0A0E14" fill-opacity=".55"/>')
        for k in range(3):
            out.append(f'<line x1="{cx-w*0.32}" y1="{cy-20+k*22}" x2="{cx+w*0.32}" y2="{cy-20+k*22}" stroke="#0A0E14" stroke-opacity=".3" stroke-width="3" stroke-linecap="round"/>')
        if pave:
            r = 6.5 * S
            i = 0
            for yy in range(int(cy - h / 2 + 34), int(cy - 30), int(r * 2.3)):
                for xx in range(int(cx - w / 2 + 16), int(cx + w / 2 - 10), int(r * 2.3)):
                    out.append(gem(xx, yy, r, stone, i, facets=False)); i += 1
        bail_y = cy - h / 2
    elif ptype == "heart":
        w, h = 150 * S, 140 * S
        out.append(f'<path d="M{cx},{cy+h/2} C{cx-w*0.95},{cy-h*0.1} {cx-w*0.4},{cy-h*0.8} {cx},{cy-h*0.25} C{cx+w*0.4},{cy-h*0.8} {cx+w*0.95},{cy-h*0.1} {cx},{cy+h/2}Z" fill="url(#m)" stroke="#0A0E14" stroke-opacity=".55" stroke-width="2"/>')
        out.append(f'<path d="M{cx-w*0.1},{cy+h*0.28} C{cx-w*0.7},{cy-h*0.1} {cx-w*0.3},{cy-h*0.55} {cx-w*0.02},{cy-h*0.15}" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="3" stroke-linecap="round"/>')
        if pave:
            r = 6 * S
            i = 0
            for yy in range(int(cy - h * 0.4), int(cy + h * 0.35), int(r * 2.4)):
                for xx in range(int(cx - w * 0.4), int(cx + w * 0.4), int(r * 2.4)):
                    dx, dy = (xx - cx) / (w * 0.42), (yy - cy + h * 0.05) / (h * 0.4)
                    if dx * dx + dy * dy < 1:
                        out.append(gem(xx, yy, r, stone, i, facets=False)); i += 1
        bail_y = cy - h * 0.62
    elif ptype == "drop":
        out.append(f'<path d="M{cx},{cy-95*S} C{cx+92*S},{cy-10*S} {cx+70*S},{cy+85*S} {cx},{cy+85*S} C{cx-70*S},{cy+85*S} {cx-92*S},{cy-10*S} {cx},{cy-95*S}Z" fill="url(#m)" stroke="#0A0E14" stroke-opacity=".55" stroke-width="2"/>')
        out.append(stone_shape(cx, cy, 120 * S, 150 * S, "pear", stone or "dia"))
        bail_y = cy - 95 * S
    elif ptype == "eye":
        out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{125*S}" ry="{78*S}" fill="url(#m)" stroke="#0A0E14" stroke-opacity=".55" stroke-width="2"/>')
        out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{105*S}" ry="{62*S}" fill="#1B3A8F"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{56*S}" fill="#F3F7FB"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{36*S}" fill="#3D7BDA"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{16*S}" fill="#0A0E14"/>')
        out.append(f'<circle cx="{cx-8*S}" cy="{cy-8*S}" r="{6*S}" fill="#fff" fill-opacity=".9"/>')
        if pave or stone:
            n = 20
            for i in range(n):
                a = 2 * math.pi * i / n
                out.append(gem(cx + 115 * S * math.cos(a), cy + 70 * S * math.sin(a), 6 * S, "dia" if stone in ("sap", "dia") else stone, i, facets=False))
        bail_y = cy - 78 * S
    elif ptype == "star":
        R = 110 * S
        pts = []
        for i in range(10):
            r = R if i % 2 == 0 else R * 0.45
            a = -math.pi / 2 + i * math.pi / 5
            pts.append(f'{cx + r*math.cos(a):.1f},{cy + r*math.sin(a):.1f}')
        out.append(f'<polygon points="{" ".join(pts)}" fill="url(#m)" stroke="#0A0E14" stroke-opacity=".55" stroke-width="2" stroke-linejoin="round"/>')
        if pave:
            r = 6 * S
            i = 0
            for k in range(5):
                a = -math.pi / 2 + k * 2 * math.pi / 5
                for d in (0.2, 0.42, 0.64, 0.86):
                    out.append(gem(cx + R * d * math.cos(a), cy + R * d * math.sin(a), r, stone, i, facets=False)); i += 1
            out.append(gem(cx, cy, r * 1.7, stone, 3))
        bail_y = cy - R
    else:
        R = 90 * S
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#m)" stroke="#0A0E14" stroke-opacity=".55" stroke-width="2"/>')
        bail_y = cy - R
    # bail
    out.insert(0, f'<ellipse cx="{cx}" cy="{bail_y - 14*S:.1f}" rx="{13*S}" ry="{18*S}" fill="none" stroke="#0A0E14" stroke-opacity=".55" stroke-width="{11*S}"/><ellipse cx="{cx}" cy="{bail_y - 14*S:.1f}" rx="{13*S}" ry="{18*S}" fill="none" stroke="url(#m)" stroke-width="{8*S}"/>')
    return "".join(out), bail_y - 30 * S


# ------------------------------------------------------------ rings
def ring_base(cx=300, cy=330, rx=150, ry=92, thick=28, grad="m"):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#0A0E14" stroke-opacity=".6" stroke-width="{thick+3}"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="url(#{grad})" stroke-width="{thick}"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="{thick*0.2}" transform="translate(0,{-thick*0.25})" stroke-dasharray="180 900" stroke-dashoffset="-40"/>'
            f'<ellipse cx="{cx}" cy="{cy+thick*0.15}" rx="{rx}" ry="{ry}" fill="none" stroke="#0A0E14" stroke-opacity=".25" stroke-width="{thick*0.35}" stroke-dasharray="260 900" stroke-dashoffset="-560"/>')


def ring_body(ptype, color, stone, ct, shape="round", grams=6, engagement=False):
    cx, cy = 300, 330
    thick = 18 + min(grams, 12) * 1.6
    out = [ring_base(cx, cy, 150, 92, thick)]
    top = cy - 92
    if ptype == "solitaire" or (ptype == "halo") or ptype == "three-stone":
        size = 70 + min(ct, 3) * 22
        if ptype == "halo":
            n = 16
            for i in range(n):
                a = 2 * math.pi * i / n
                out.append(gem(cx + (size * 0.62 + 12) * math.cos(a), top + (size * 0.62 + 12) * math.sin(a) * 0.95, 8, stone or "dia", i, facets=False))
        if ptype == "three-stone":
            for k in (-1, 1):
                out.append(prongs(cx + k * size * 0.78, top + 6, size * 0.28))
                out.append(stone_shape(cx + k * size * 0.78, top + 6, size * 0.5, size * 0.6, shape if shape != "round" else "round", stone or "dia"))
        out.append(prongs(cx, top, size * 0.5))
        out.append(stone_shape(cx, top, size, size * (1.25 if shape in ("oval", "emerald", "pear", "marquise", "radiant") else 1), shape, stone or "dia"))
    elif ptype == "signet":
        out.append(f'<ellipse cx="{cx}" cy="{top}" rx="{72}" ry="{50}" fill="url(#mr)" stroke="#0A0E14" stroke-opacity=".55" stroke-width="2"/>')
        out.append(f'<ellipse cx="{cx}" cy="{top}" rx="{56}" ry="{37}" fill="url(#md)" stroke="#fff" stroke-opacity=".2"/>')
        if stone in ("dia", "lab", "blk", "multi"):
            for i, (dx, dy) in enumerate([(0, 0), (-28, -12), (28, -12), (-28, 12), (28, 12), (0, -22), (0, 22)]):
                out.append(gem(cx + dx, top + dy, 8, stone, i, facets=False))
        else:
            out.append(f'<text x="{cx}" y="{top+14}" text-anchor="middle" font-family="Georgia, serif" font-size="40" font-weight="700" fill="#0A0E14" fill-opacity=".45">IV</text>')
    elif ptype == "eternity":
        n = 14
        for i in range(n):
            t = 0.5 + (i / (n - 1)) * 0.5 * 0.999
            a = math.pi * (i / (n - 1))
            x, y = cx - 150 * math.cos(a), cy + 92 * math.sin(a)
            out.append(f'<rect x="{x-11}" y="{y-11}" width="22" height="22" rx="4" fill="url(#m)" stroke="#0A0E14" stroke-opacity=".5" transform="rotate({math.degrees(a)*0.4:.0f} {x} {y})"/>')
            out.append(gem(x, y, 8, stone or "dia", i, facets=False))
    elif ptype == "cuban-ring":
        out = [cuban_links(loop_curve(cx, cy, 150, 92), 6, stone, thick_scale=0.9)]
    elif ptype == "band":
        out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="150" ry="92" fill="none" stroke="#fff" stroke-opacity=".15" stroke-width="{thick*0.5}" stroke-dasharray="120 800" stroke-dashoffset="-410"/>')
        if stone in ("dia", "lab"):
            for i in range(5):
                a = math.pi * (0.3 + 0.1 * i)
                out.append(gem(cx - 150 * math.cos(a), cy + 92 * math.sin(a), 6, stone, i, facets=False))
    return "".join(out)


# ------------------------------------------------------------ earrings
def earrings_body(ptype, color, stone, ct):
    out = []
    r = 40 + min(ct, 4) * 9
    xs = (200, 400) if ptype != "single" else (300,)
    for j, x in enumerate(xs):
        y = 300
        if ptype in ("studs", "single", "drops", "cross-e"):
            out.append(f'<line x1="{x}" y1="{y+r*0.5}" x2="{x}" y2="{y+r*0.9}" stroke="url(#m)" stroke-width="5"/>')
            out.append(prongs(x, y, r * 0.98))
            out.append(gem(x, y, r, stone or "dia", j))
            if ptype == "drops":
                out.append(f'<line x1="{x}" y1="{y+r}" x2="{x}" y2="{y+r+40}" stroke="url(#m)" stroke-width="5"/>')
                out.append(stone_shape(x, y + r + 95, 70, 110, "pear", stone or "dia"))
            if ptype == "cross-e":
                body, _ = pendant_body("cross", color, stone, ct, "", x, y + r + 75, 0.42)
                out.append(body)
        elif ptype == "cluster":
            out.append(f'<circle cx="{x}" cy="{y}" r="{r*1.6}" fill="url(#m)" stroke="#0A0E14" stroke-opacity=".5" stroke-width="2"/>')
            for i in range(6):
                a = 2 * math.pi * i / 6
                out.append(gem(x + r * 1.05 * math.cos(a), y + r * 1.05 * math.sin(a), r * 0.5, stone or "dia", i))
            out.append(gem(x, y, r * 0.55, stone or "dia", 4))
        elif ptype == "baguette":
            out.append(f'<rect x="{x-r*0.85}" y="{y-r*1.4}" width="{r*1.7}" height="{r*2.8}" rx="4" fill="url(#m)" stroke="#0A0E14" stroke-opacity=".5" stroke-width="2"/>')
            out.append(stone_shape(x, y, r * 1.2, r * 2.3, "emerald", stone or "dia"))
        elif ptype == "hoops":
            big = ct == 0 and r <= 40
            rx, ry = (34, 44) if big else (44, 62)
            # huggie small vs large hoops decided by grams via ct==0
            out.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="none" stroke="#0A0E14" stroke-opacity=".6" stroke-width="{18 if big else 14}"/>')
            out.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="none" stroke="url(#m)" stroke-width="{15 if big else 11}"/>')
            out.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="3" stroke-dasharray="60 300" stroke-dashoffset="-20"/>')
            if stone:
                for i in range(7):
                    a = math.pi * (0.15 + 0.7 * i / 6)
                    out.append(gem(x + rx * math.cos(a) * 1.0, y + ry * math.sin(a), 5.5, stone, i, facets=False))
    return "".join(out)


# ------------------------------------------------------------ bracelets
def bracelet_body(ptype, color, stone, width_mm, ct=0.0):
    c = loop_curve()
    if ptype == "cuban-b":
        return cuban_links(c, width_mm * 0.9, stone) + clasp(300, 450, 14 + width_mm * 2)
    if ptype == "tennis-b":
        return tennis(c, width_mm, stone or "dia") + clasp(300, 450, 12 + width_mm * 2)
    if ptype == "rope-b":
        return rope(c, width_mm) + clasp(300, 450, 12 + width_mm * 2)
    if ptype == "franco-b":
        return box_links(c, width_mm, franco=True) + clasp(300, 450, 12 + width_mm * 2)
    if ptype == "paperclip-b":
        return paperclip(c, width_mm) + clasp(300, 450, 12 + width_mm * 2)
    if ptype == "id":
        out = [cuban_links(c, width_mm * 0.7, "")]
        w, h = 210, 26 + width_mm * 4
        out.append(f'<rect x="{300-w/2}" y="{150-h/2}" width="{w}" height="{h}" rx="{h*0.3}" fill="url(#m)" stroke="#0A0E14" stroke-opacity=".55" stroke-width="2"/>')
        out.append(f'<rect x="{300-w/2+6}" y="{150-h/2+6}" width="{w-12}" height="{h-12}" rx="{h*0.22}" fill="none" stroke="#fff" stroke-opacity=".25"/>')
        if stone:
            i = 0
            for xx in range(int(300 - w / 2 + 18), int(300 + w / 2 - 12), 15):
                for yy in range(int(150 - h / 2 + 14), int(150 + h / 2 - 8), 15):
                    out.append(gem(xx, yy, 5.5, stone, i, facets=False)); i += 1
        else:
            out.append(f'<text x="300" y="{150+7}" text-anchor="middle" font-family="Georgia, serif" font-size="22" font-weight="700" fill="#0A0E14" fill-opacity=".45" letter-spacing="4">ICE VAULT</text>')
        return "".join(out)
    if ptype == "bangle":
        t = 14 + width_mm * 5
        out = [f'<ellipse cx="300" cy="300" rx="205" ry="150" fill="none" stroke="#0A0E14" stroke-opacity=".6" stroke-width="{t+3}"/>',
               f'<ellipse cx="300" cy="300" rx="205" ry="150" fill="none" stroke="url(#m)" stroke-width="{t}"/>',
               f'<ellipse cx="300" cy="300" rx="205" ry="150" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="{t*0.25}" stroke-dasharray="300 1200" stroke-dashoffset="-140" transform="translate(0,{-t*0.22})"/>']
        if stone:
            for i in range(11):
                a = math.pi * (1.1 + 0.8 * i / 10)
                out.append(gem(300 + 205 * math.cos(a), 300 + 150 * math.sin(a), t * 0.28, stone, i, facets=False))
        return "".join(out)
    return cuban_links(c, width_mm, stone)


# ------------------------------------------------------------ watches
DIALS = {"Black": ("#2A2E35", "#0A0C10"), "Blue": ("#2F5DB8", "#0E2554"), "Silver": ("#F1F3F5", "#B7BEC7"), "Green": ("#2B8A5B", "#0C3B25"),
         "Champagne": ("#F3DFA2", "#C9A653"), "Pink": ("#F6D7DB", "#D7A1AA"), "Diamond pave": ("#F7FBFF", "#BFD5EA"), "Mother of pearl": ("#FBF7FF", "#D9CFE8")}


def watch_body(color, dial, case_mm, diamonds=False, bracelet="Oyster", two_tone=False):
    cx, cy = 300, 300
    R = 84 + min(max(case_mm - 28, 0), 14) * 2.2
    d1, d2 = DIALS.get(dial, DIALS["Black"])
    out = []
    # bracelet
    rows = 5 if "Jubilee" in bracelet or "President" in bracelet else 3
    link_h = 26
    for side in (-1, 1):
        for k in range(6):
            y = cy + side * (R + 8 + k * (link_h + 3))
            ww = (R * 1.15) - k * 5
            xs = ww / rows
            for j in range(rows):
                x = cx - ww / 2 + j * xs
                grad = "mw" if (two_tone and j in (0, rows - 1)) else ("m" if (j + k) % 2 == 0 else "mr")
                out.append(f'<rect x="{x+1:.1f}" y="{y-link_h/2 if side>0 else y-link_h/2:.1f}" width="{xs-2:.1f}" height="{link_h}" rx="5" fill="url(#{grad})" stroke="#0A0E14" stroke-opacity=".55" stroke-width="1.5"/>')
    if "Leather" in bracelet:
        out = [f'<rect x="{cx-R*0.5}" y="{cy-R-190}" width="{R}" height="190" rx="12" fill="#3B2A22" stroke="#0A0E14" stroke-opacity=".6" stroke-width="2"/>',
               f'<rect x="{cx-R*0.5}" y="{cy+R}" width="{R}" height="190" rx="12" fill="#3B2A22" stroke="#0A0E14" stroke-opacity=".6" stroke-width="2"/>']
    # crown
    out.append(f'<rect x="{cx+R+2}" y="{cy-10}" width="16" height="20" rx="4" fill="url(#m)" stroke="#0A0E14" stroke-opacity=".5"/>')
    # case
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{R+10}" fill="url(#m)" stroke="#0A0E14" stroke-opacity=".6" stroke-width="2"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#mr)" stroke="#0A0E14" stroke-opacity=".5" stroke-width="1.5"/>')
    if diamonds:
        n = 36
        for i in range(n):
            a = 2 * math.pi * i / n
            out.append(gem(cx + (R + 1) * math.cos(a), cy + (R + 1) * math.sin(a), 6, "dia", i, facets=False))
    else:
        # fluted bezel
        for i in range(48):
            a = 2 * math.pi * i / 48
            out.append(f'<line x1="{cx + (R-4)*math.cos(a):.1f}" y1="{cy + (R-4)*math.sin(a):.1f}" x2="{cx + (R+7)*math.cos(a):.1f}" y2="{cy + (R+7)*math.sin(a):.1f}" stroke="#0A0E14" stroke-opacity=".25" stroke-width="2"/>')
    # dial
    out.append(f'<radialGradient id="dial" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="{d1}"/><stop offset="1" stop-color="{d2}"/></radialGradient>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{R-10}" fill="url(#dial)" stroke="#0A0E14" stroke-opacity=".7" stroke-width="3"/>')
    if dial == "Diamond pave":
        i = 0
        for yy in range(int(cy - R + 18), int(cy + R - 14), 13):
            for xx in range(int(cx - R + 18), int(cx + R - 14), 13):
                if (xx - cx) ** 2 + (yy - cy) ** 2 < (R - 18) ** 2:
                    out.append(gem(xx, yy, 5.2, "dia", i, facets=False)); i += 1
    # indices
    light = dial in ("Black", "Blue", "Green")
    idx_fill = "url(#m)" if not light else "#E9EEF3"
    for i in range(12):
        a = 2 * math.pi * i / 12
        L = 14 if i % 3 == 0 else 10
        x1, y1 = cx + (R - 18) * math.cos(a), cy + (R - 18) * math.sin(a)
        x2, y2 = cx + (R - 18 - L) * math.cos(a), cy + (R - 18 - L) * math.sin(a)
        if i == 0 and dial != "Diamond pave":
            out.append(f'<rect x="{cx+R-38}" y="{cy-9}" width="22" height="18" rx="2" fill="#F5F7F9" stroke="#0A0E14" stroke-opacity=".5"/><text x="{cx+R-27}" y="{cy+5}" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#0A0E14">28</text>')
            continue
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{idx_fill}" stroke-width="{5 if i % 3 == 0 else 3.5}" stroke-linecap="round"/>')
    # logo mark on dial
    out.append(f'<path d="M{cx-9},{cy-R*0.55+8} L{cx},{cy-R*0.55-4} L{cx+9},{cy-R*0.55+8} L{cx},{cy-R*0.55+22}Z" fill="{idx_fill}" fill-opacity=".9"/>')
    # hands
    hand = "#E9EEF3" if light else "#2B2F36"
    out.append(f'<line x1="{cx}" y1="{cy}" x2="{cx - (R-50)*0.5:.1f}" y2="{cy - (R-50)*0.87:.1f}" stroke="{hand}" stroke-width="6" stroke-linecap="round"/>')
    out.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + (R-26)*0.87:.1f}" y2="{cy - (R-26)*0.5:.1f}" stroke="{hand}" stroke-width="4.5" stroke-linecap="round"/>')
    out.append(f'<line x1="{cx}" y1="{cy}" x2="{cx - (R-24)*0.26:.1f}" y2="{cy + (R-24)*0.97:.1f}" stroke="{hand}" stroke-width="1.5" stroke-linecap="round"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{hand}"/>')
    # crystal glare
    out.append(f'<ellipse cx="{cx-R*0.25}" cy="{cy-R*0.4}" rx="{R*0.45}" ry="{R*0.22}" fill="#fff" fill-opacity=".12" transform="rotate(-30 {cx-R*0.25} {cy-R*0.4})"/>')
    return "".join(out)


# ------------------------------------------------------------ dispatch
def render_product(p):
    kind, ptype, color, stone = p["kind"], p["ptype"], p["color"], p.get("stone", "")
    if kind == "chains":
        w = p.get("width", 3)
        body = CHAINS.get(ptype, CHAINS["cuban"])(necklace_curve(), w, stone)
        return svg(body, color, stone)
    if kind == "pendants":
        body, top = pendant_body(ptype, color, stone, p.get("ct", 0), p.get("letter", ""), 300, 400)
        chain_svg = "".join(cable(c, 0, 7) for c in v_curve(120, 480, 40, top - 4))
        return svg(chain_svg + body, color, stone)
    if kind == "rings":
        return svg(ring_body(ptype, color, stone, p.get("ct", 0), p.get("shape", "round"), p.get("grams", 6), p.get("engagement", False)), color, stone)
    if kind == "earrings":
        return svg(earrings_body(ptype, color, stone, p.get("ct", 0)), color, stone)
    if kind == "bracelets":
        return svg(bracelet_body(ptype, color, stone, p.get("width", 4), p.get("ct", 0)), color, stone)
    if kind == "watches":
        return svg(watch_body(color, p.get("dial", "Black"), p.get("case_mm", 40), bool(stone), p["specs"][4][1] if len(p["specs"]) > 4 else "Oyster", color == "T"), "Steel" if color in ("W", "S", "Steel") else color, stone)
    return svg("", color)


def render_custom(c):
    fake = dict(kind={"medallion": "pendants", "signet": "rings", "dogtag": "pendants", "id": "bracelets", "cross": "pendants", "initial": "pendants",
                      "solitaire": "rings", "cuban": "chains", "halo": "rings", "eye": "pendants", "star": "pendants"}[c["ptype"]],
                ptype=c["ptype"], color=c["color"], stone=c["stone"], ct=c["ct"], letter=c.get("letter", ""), width=10, grams=9, shape="oval",
                engagement=c["ptype"] == "halo", specs=[])
    return render_product(fake)


def ring_builder_preview(setting, shape, color, ct, stone="dia"):
    ptype = {"solitaire": "solitaire", "hidden-halo": "solitaire", "halo": "halo", "three-stone": "three-stone", "pave": "band-pave", "cathedral": "solitaire"}.get(setting, "solitaire")
    if ptype == "band-pave":
        body = ring_body("band", color, "dia", 0.3, shape, 3) + prongs(300, 238, 40 + ct * 10) + stone_shape(300, 238, 80 + ct * 20, (80 + ct * 20) * (1.25 if shape in ("oval", "emerald", "pear", "marquise", "radiant") else 1), shape, stone)
    else:
        body = ring_body(ptype, color, stone, ct, shape, 3.2, True)
    return svg(body, color, stone)


# ------------------------------------------------------------ brand
def logo_mark(size=28):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40" width="{size}" height="{size}" aria-hidden="true" class="mark">'
            '<polygon points="20,2 33,7 38,20 33,33 20,38 7,33 2,20 7,7" fill="none" stroke="currentColor" stroke-width="1.6"/>'
            '<polygon points="20,10 30,20 20,30 10,20" fill="none" stroke="currentColor" stroke-width="1.2"/>'
            '<path d="M20,2 L20,10 M33,7 L30,20 M38,20 L30,20 M33,33 L20,30 M20,38 L20,30 M7,33 L10,20 M2,20 L10,20 M7,7 L20,10" stroke="currentColor" stroke-width=".9" stroke-opacity=".7"/>'
            '</svg>')


def hero_diamond():
    """Brilliant cut, side profile. Facets alternate opacity; a light band sweeps once on load (CSS in site.css)."""
    W, H = 640, 560
    table = [(212, 92), (428, 92)]
    girdle_y = 218
    gx = [64, 128, 200, 264, 320, 376, 440, 512, 576]
    culet = (320, 508)
    facets = []
    # table
    facets.append(([(212, 92), (428, 92), (470, 150), (170, 150)], .22))
    # crown: star facets between table edge and crown mid line, then bezel facets to girdle
    mid = [(170, 150), (245, 150), (320, 150), (395, 150), (470, 150)]
    for i in range(4):
        facets.append(([mid[i], mid[i + 1], ((mid[i][0] + mid[i + 1][0]) / 2, 92) if 0 < i < 3 else mid[i + 1] if i == 3 else mid[i]], .32 if i % 2 else .18))
    # bezel facets to girdle
    for i in range(8):
        a, b = (gx[i], girdle_y), (gx[i + 1], girdle_y)
        top = mid[min(i // 2, 4)] if i % 2 == 0 else mid[min(i // 2 + 1, 4)]
        facets.append(([a, b, top], .12 + (i % 3) * .11))
    # pavilion facets fan to culet
    for i in range(8):
        a, b = (gx[i], girdle_y), (gx[i + 1], girdle_y)
        facets.append(([a, b, culet], .10 + ((i * 3) % 5) * .07))
    polys = "".join(f'<polygon points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in pts)}" fill="#BFE3FF" fill-opacity="{op:.2f}" stroke="#E6F4FF" stroke-opacity=".45" stroke-width="1"/>' for pts, op in facets)
    outline = f'<polygon points="212,92 428,92 576,218 320,508 64,218" fill="none" stroke="#E6F4FF" stroke-opacity=".7" stroke-width="1.4"/>'
    girdle = f'<line x1="64" y1="218" x2="576" y2="218" stroke="#E6F4FF" stroke-opacity=".6" stroke-width="1.4"/>'
    sweep = ('<defs><linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
             '<clipPath id="dclip"><polygon points="212,92 428,92 576,218 320,508 64,218"/></clipPath></defs>'
             '<rect class="sweep" x="-300" y="0" width="220" height="560" fill="url(#sweep)" clip-path="url(#dclip)" transform="skewX(-18)"/>')
    sparks = "".join(f'<g class="spark" style="--d:{d}s" transform="translate({x},{y})"><path d="M0,-9 L2,-2 L9,0 L2,2 L0,9 L-2,2 L-9,0 L-2,-2Z" fill="#fff"/></g>' for x, y, d in [(150, 178, 1.2), (470, 140, 2.1), (340, 300, 2.8), (240, 250, 1.7)])
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" class="hero-diamond" role="img" aria-label="Brilliant cut diamond">{sweep}{polys}{outline}{girdle}{sparks}</svg>'
