"""Site-wide settings. Edit this file to change contact details everywhere."""

SITE = {
    "name": "Ice Vault",
    "legal_name": "Ice Vault NYC LLC",
    "tagline": "Diamonds and fine jewelry, made in the Diamond District",
    "domain": "https://icevaultnyc.com",
    "phone_display": "(212) 555-0147",
    "phone_tel": "+12125550147",
    "sms_tel": "+12125550147",
    "email": "concierge@icevaultnyc.com",
    "email_business": "partners@icevaultnyc.com",
    "address_line1": "26 W 47th St, Suite 402",
    "address_line2": "New York, NY 10036",
    "address_short": "26 W 47th St, New York",
    "map_lat": 40.7573,
    "map_lon": -73.9800,
    "hours": [
        ("Monday to Friday", "10:00 am to 6:30 pm"),
        ("Saturday", "11:00 am to 5:00 pm"),
        ("Sunday", "By appointment"),
    ],
    "socials": {
        "Instagram": "https://instagram.com/icevaultnyc",
        "TikTok": "https://tiktok.com/@icevaultnyc",
        "YouTube": "https://youtube.com/@icevaultnyc",
    },
    # Leave empty to send forms by email (mailto). Set to a Formspree/Basin URL to POST.
    "form_endpoint": "",
    "promo": {
        "active": True,
        "label": "Fall sale",
        "text": "Up to 15% off select pieces with code",
        "code": "ICE15",
        "collection": "sale",
    },
    "wire_discount_pct": 3,
    "financing_months": 12,
    "founded": 2014,
}
