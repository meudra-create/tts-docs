#!/usr/bin/env python3
"""Preview réduction police H1 — test avec titres courts, moyens, longs."""

from weasyprint import HTML, CSS
from pathlib import Path
import fitz, struct, zlib

OUT_PDF = Path("/tmp/preview_h1.pdf")
OUT_PNG = Path("/home/user/tts-docs/manuscrit-edition/preview_h1.png")

BLANC    = "#FFFFFF"
ARDOISE  = "#2C3A4A"
ARDOISE_L= "#3D5068"
OR_SATIN = "#A07820"
CREME    = "#F4EFE4"
CREME_BD = "#D8CEBC"
GRIS_TX  = "#2E2E2E"
GRIS_SUB = "#555555"

# Test 3 tailles
for pt in [16, 15, 14]:
    CSS_TEST = f"""
@import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;0,700;1,400;1,600&family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&display=swap');

@page {{
    size: 6in 9in;
    margin-top: 0.80in;
    margin-bottom: 0.90in;
    margin-left: 0.80in;
    margin-right: 0.60in;
    @bottom-center {{
        content: "— " counter(page) " —";
        font-family: 'Crimson Text', serif;
        font-size: 9pt;
        color: #A8A8A0;
        letter-spacing: 0.15em;
    }}
}}
@page :left {{ margin-left: 0.60in; margin-right: 0.80in; }}

body {{
    font-family: 'EB Garamond', serif;
    font-size: 11.5pt;
    line-height: 1.63;
    color: {GRIS_TX};
    background: {BLANC};
}}

h1 {{
    font-family: 'Crimson Text', serif;
    font-size: {pt}pt;
    font-weight: 600;
    color: {BLANC};
    background: {ARDOISE};
    margin-top: 0;
    margin-bottom: 2.2em;
    margin-left: -0.80in;
    margin-right: -0.60in;
    padding: 1.4em 0.80in 1.2em 0.80in;
    page-break-before: always;
    line-height: 1.25;
    border-top: 4pt solid {OR_SATIN};
    border-bottom: 1pt solid {ARDOISE_L};
    letter-spacing: 0.005em;
    white-space: nowrap;
    overflow: hidden;
}}

p {{ margin: 0 0 0.5em 0; text-indent: 1.4em; }}
"""

    HTML_TEST = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"></head>
<body>
<h1>Chapitre 4 — Les résistances oubliées</h1>
<p>Guélémou, 29 septembre 1898. À l'aube, des soldats français encerclent le campement d'un vieil homme.</p>

<h1>Chapitre 24 — La jeunesse connectée, la diaspora en première ligne</h1>
<p>Dans les rues de Bamako, Ouagadougou et Niamey, une génération grandit avec un smartphone à la main.</p>

<h1>Chapitre 27 — Industrialisation et éducation: l'économie de guerre et l'arme des cerveaux</h1>
<p>Le plus long titre du livre — indicateur de ce qui peut ou non tenir sur une ligne à {pt}pt.</p>
</body></html>"""

    doc = HTML(string=HTML_TEST, base_url="/tmp")
    css = CSS(string=CSS_TEST)
    path = Path(f"/tmp/preview_h1_{pt}pt.pdf")
    doc.write_pdf(str(path), stylesheets=[css])

# Assemble 3 premiers pages de chaque en image composite
import fitz, struct, zlib

imgs = []
for pt in [16, 15, 14]:
    pdf = fitz.open(f"/tmp/preview_h1_{pt}pt.pdf")
    page = pdf[0]
    mat = fitz.Matrix(2.2, 2.2)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    imgs.append((pt, pix))

gap = 20
label_h = 0
total_h = sum(p.height for _, p in imgs) + (len(imgs)-1)*gap
max_w = max(p.width for _, p in imgs)

composite = bytearray(total_h * max_w * 3)
for i in range(len(composite)):
    composite[i] = 255

y = 0
for pt, pix in imgs:
    for row in range(pix.height):
        src = pix.samples[row*pix.width*3:(row+1)*pix.width*3]
        dst = (y+row)*max_w*3
        composite[dst:dst+len(src)] = src
    y += pix.height + gap

def png_chunk(name, data):
    import zlib, struct
    c = zlib.crc32(name+data) & 0xFFFFFFFF
    return struct.pack('>I',len(data))+name+data+struct.pack('>I',c)

raw = bytearray()
for row in range(total_h):
    raw.append(0)
    raw.extend(composite[row*max_w*3:(row+1)*max_w*3])
comp = zlib.compress(bytes(raw),6)

with open(str(OUT_PNG),'wb') as f:
    f.write(b'\x89PNG\r\n\x1a\n')
    f.write(png_chunk(b'IHDR', struct.pack('>IIBBBBB', max_w, total_h, 8, 2, 0, 0, 0)))
    f.write(png_chunk(b'IDAT', comp))
    f.write(png_chunk(b'IEND', b''))

print(f"Preview: {OUT_PNG}")
