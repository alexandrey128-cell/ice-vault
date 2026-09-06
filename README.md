# Ice Vault

Static website for Ice Vault, a diamond and jewelry business in New York's Diamond District.
Built with Python and Jinja2. No database, no Node. Product images are generated SVG renders.

## Build and preview

    python3 build.py
    python3 -m http.server 8080 -d dist

Open http://localhost:8080.

## Edit

- `config.py` holds the name, phone, email, address, hours, promo code and financing terms. Change them once, every page updates.
- `data/catalog.py` holds the navigation, categories and products. Add or remove products there.
- `templates/` holds the page layouts. `static/css/site.css` holds the styles. `static/js/` holds the cart, filters, ring builder and diamond search.
- `svggen.py` draws the product images.

## Forms

Forms open the visitor's email app with the details filled in. To send them to a service instead,
set `form_endpoint` in `config.py` to a Formspree or Basin URL.

## Deploy

Every push to `main` builds the site and publishes it to GitHub Pages through `.github/workflows/pages.yml`.
To build for a sub-folder by hand:

    BASE=/ice-vault SITE_URL=https://example.github.io/ice-vault python3 build.py

## Replace before launch

- Phone, email and address in `config.py` are placeholders.
- Product photos are generated renders. Swap `dist/img/products/*.svg` for real photos by changing `image` paths in the catalog.
- Reviews in `data/catalog.py` are sample text.
