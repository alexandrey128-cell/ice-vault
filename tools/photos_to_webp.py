"""Convert static/img/photos/*.jpg to .webp (quality 80) and delete the jpg. Run with .venv/bin/python."""
import os, sys
from PIL import Image
base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'img', 'photos')
n = 0
for name in sorted(os.listdir(base)):
    if not name.endswith('.jpg'):
        continue
    src = os.path.join(base, name)
    dst = src[:-4] + '.webp'
    if not os.path.exists(dst):
        with Image.open(src) as im:
            im = im.convert('RGB')
            im.save(dst, 'WEBP', quality=80, method=4)
        n += 1
    os.remove(src)
print(n, 'converted')
