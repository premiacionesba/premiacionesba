"""Genera miniaturas WebP livianas para la grilla del catálogo.

Uso (desde la raíz del repo):  python herramientas/miniaturas.py
Lee fotos/*.jpg y escribe fotos/mini/<id>.webp (solo las que faltan o cambiaron).
Si una foto no tiene miniatura, la web usa la foto grande igual: no se rompe nada.
"""
from pathlib import Path
from PIL import Image

SRC = Path("fotos")
DST = SRC / "mini"
LADO = 720       # px del lado de la miniatura
RECORTE = 0.10   # recorta 10% de cada borde (el producto queda más grande)

DST.mkdir(exist_ok=True)
for f in sorted(SRC.glob("*.jpg")):
    out = DST / (f.stem + ".webp")
    if out.exists() and out.stat().st_mtime >= f.stat().st_mtime:
        continue
    im = Image.open(f).convert("RGB")
    w, h = im.size
    m = int(min(w, h) * RECORTE)
    im = im.crop((m, m, w - m, h - m)).resize((LADO, LADO), Image.LANCZOS)
    im.save(out, "WEBP", quality=78, method=6)
    print("ok", out)
