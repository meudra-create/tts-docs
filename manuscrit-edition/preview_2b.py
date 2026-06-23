#!/usr/bin/env python3
"""Preview thème Atlas Stratégique 2b — fond blanc, ardoise bleu."""

from weasyprint import HTML, CSS
from pathlib import Path
import fitz

OUT_PDF = Path("/tmp/preview_2b.pdf")
OUT_PNG = Path("/home/user/tts-docs/manuscrit-edition/preview_2b.png")

BLEU     = "#2558A7"
BLEU_CLR = "#3A72C4"
GRIS_TX  = "#1A1A2E"
GRIS_SUB = "#4A4A5A"
BLANC    = "#FFFFFF"
GRIS_BG  = "#F4F6FA"
GRIS_MID = "#D8DCE8"
ROUGE_A  = "#C0392B"

CSS_2B = f"""
@import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Montserrat:wght@400;600;700&display=swap');

@page {{
    size: 6in 9in;
    margin-top: 0.75in;
    margin-bottom: 0.70in;
    margin-left: 0.80in;
    margin-right: 0.60in;
}}

body {{
    font-family: 'Libre Baskerville', 'FreeSerif', Georgia, serif;
    font-size: 11pt;
    line-height: 1.58;
    color: {GRIS_TX};
    background: {BLANC};
    text-align: justify;
    hyphens: auto;
}}

h1 {{
    font-family: 'Montserrat', 'FreeSans', sans-serif;
    font-size: 18pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: {BLANC};
    background: {BLEU};
    text-align: left;
    margin-top: 0;
    margin-bottom: 1.4em;
    margin-left: -0.80in;
    margin-right: -0.60in;
    padding: 0.75em 0.80in 0.65em 0.80in;
    page-break-before: always;
    border-top: 5pt solid {BLEU_CLR};
}}

h2 {{
    font-family: 'Montserrat', 'FreeSans', sans-serif;
    font-size: 12pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: {BLEU};
    margin-top: 1.8em;
    margin-bottom: 0.5em;
    border-bottom: 1.5pt solid {BLEU};
    padding-bottom: 0.2em;
}}

h3 {{
    font-family: 'Libre Baskerville', serif;
    font-size: 11.5pt;
    font-weight: 700;
    font-style: italic;
    color: {GRIS_SUB};
    margin-top: 1.3em;
    margin-bottom: 0.3em;
}}

p {{
    margin: 0.3em 0 0.55em 0;
    text-indent: 1.2em;
}}

p:first-of-type, h1 + p, h2 + p, h3 + p, blockquote + p, hr + p {{
    text-indent: 0;
}}

blockquote {{
    background: {GRIS_BG};
    border-left: 4pt solid {BLEU};
    margin: 1.2em 0.3em;
    padding: 0.7em 1em;
    font-style: italic;
    color: {GRIS_SUB};
    page-break-inside: avoid;
}}

blockquote p {{
    text-indent: 0;
    margin: 0.2em 0;
}}

ul, ol {{
    margin: 0.5em 0 0.5em 1.5em;
    padding: 0;
}}

li {{
    margin-bottom: 0.35em;
    line-height: 1.5;
}}

em {{
    font-style: italic;
}}

strong {{
    font-weight: 700;
    color: {BLEU};
}}

hr {{
    border: none;
    border-top: 1pt solid {GRIS_MID};
    margin: 2em auto;
    width: 40%;
}}

.stars {{
    text-align: center;
    color: {BLEU_CLR};
    font-size: 14pt;
    margin: 1.2em 0;
    letter-spacing: 0.4em;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 10pt;
    page-break-inside: avoid;
}}

th {{
    background: {BLEU};
    color: {BLANC};
    padding: 0.4em 0.6em;
    text-align: left;
    font-weight: 700;
    font-family: 'Montserrat', sans-serif;
    letter-spacing: 0.03em;
}}

td {{
    border: 0.5pt solid {GRIS_MID};
    padding: 0.35em 0.6em;
    vertical-align: top;
}}

tr:nth-child(even) td {{
    background: {GRIS_BG};
}}

.encadre {{
    background: {GRIS_BG};
    border: 1.5pt solid {GRIS_MID};
    border-left: 5pt solid {BLEU};
    padding: 0.8em 1em;
    margin: 1em 0;
    page-break-inside: avoid;
}}

a {{
    color: {BLEU};
    text-decoration: none;
}}
"""

HTML_PREVIEW = f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><title>Atlas Stratégique 2b Preview</title></head>
<body>

<h1>Chapitre I — La géopolitique des possibles</h1>

<p>L'Alliance des États du Sahel n'est pas née du vide. Elle est le produit d'une longue sédimentation de
frustrations accumulées, de promesses non tenues et d'un sentiment diffus que l'ordre international
existant n'offrait aux États africains qu'une souveraineté de façade.</p>

<p>Comprendre ce phénomène exige de sortir des grilles de lecture habituelles. Les transitions politiques
qui ont secoué le Mali, le Burkina Faso et le Niger entre 2020 et 2023 ne sont pas de simples
pronunciamientos militaires de plus dans une longue série de coups d'État africains.</p>

<h2>I. L'architecture de la dépendance</h2>

<p>Le mécanisme est d'une redoutable efficacité. Les États postcoloniaux ont hérité d'institutions
conçues pour maximiser les transferts de ressources vers les métropoles, non pour favoriser le
développement endogène de leurs populations.</p>

<blockquote>
<p>« Nous ne sommes pas contre la France, nous sommes contre la Françafrique. Ce sont deux choses
très différentes. » — Ibrahim Traoré, discours à Ouagadougou, mars 2023</p>
</blockquote>

<p>Cette distinction, que le président burkinabè s'est employé à marteler, résume l'ambiguïté
fondamentale du moment. Il ne s'agit pas d'un simple anti-occidentalisme primaire, mais d'une
critique structurelle des mécanismes de domination économique et politique.</p>

<h3>Les instruments du contrôle monétaire</h3>

<p>Le franc CFA constitue sans doute l'exemple le plus emblématique de cette architecture de
dépendance. Créé en 1945 par décret français, il lie encore aujourd'hui quatorze États africains
à une politique monétaire décidée à Paris — formellement à Francfort depuis l'arrimage à l'euro,
mais dans une zone d'influence demeurée française.</p>

<hr>

<h2>II. La rupture comme méthode</h2>

<p>Face à ce constat, les nouvelles autorités des trois États sahéliens ont fait le choix de la rupture
accélérée plutôt que de la réforme progressive. Cette stratégie comporte des risques considérables,
mais elle répond à une logique politique interne difficilement contestable.</p>

<div class="encadre">
<strong>Point de méthode :</strong> Les sources utilisées dans ce chapitre combinent des documents
officiels des gouvernements de transition, des analyses d'instituts de recherche indépendants et
des témoignages de terrain collectés entre 2022 et 2024. Les positions pro-gouvernementales
sont explicitement signalées.
</div>

<p>La vitesse de la rupture avec les partenaires traditionnels — France, CEDEAO, organisations
de Bretton Woods — a surpris les observateurs. En moins de dix-huit mois, l'ensemble de
l'architecture sécuritaire, diplomatique et économique héritée de la Françafrique a été remise
en cause.</p>

</body>
</html>"""

print("Génération PDF preview 2b...")
doc = HTML(string=HTML_PREVIEW, base_url="/tmp")
css = CSS(string=CSS_2B)
doc.write_pdf(str(OUT_PDF), stylesheets=[css])
print(f"PDF: {OUT_PDF}")

print("Conversion PDF → PNG (3 pages)...")
pdf = fitz.open(str(OUT_PDF))
pages_to_render = min(len(pdf), 3)

imgs = []
for i in range(pages_to_render):
    page = pdf[i]
    mat = fitz.Matrix(2.5, 2.5)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    imgs.append(pix)

# Assemble vertical strip
total_h = sum(p.height for p in imgs) + (len(imgs) - 1) * 20
max_w = max(p.width for p in imgs)

import struct, zlib

def png_chunk(name, data):
    c = zlib.crc32(name + data) & 0xFFFFFFFF
    return struct.pack('>I', len(data)) + name + data + struct.pack('>I', c)

def save_composite_png(imgs, path):
    w = max_w
    h = total_h
    gap = 20
    composite = bytearray(h * w * 3)
    # fill white
    for i in range(len(composite)):
        composite[i] = 255
    y_off = 0
    for pix in imgs:
        for row in range(pix.height):
            src = pix.samples[row * pix.width * 3:(row + 1) * pix.width * 3]
            dst_start = (y_off + row) * w * 3
            composite[dst_start:dst_start + len(src)] = src
        y_off += pix.height + gap

    # encode as PNG
    raw_rows = bytearray()
    for row in range(h):
        raw_rows.append(0)
        raw_rows.extend(composite[row * w * 3:(row + 1) * w * 3])
    compressed = zlib.compress(bytes(raw_rows), 6)

    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(png_chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)))
        f.write(png_chunk(b'IDAT', compressed))
        f.write(png_chunk(b'IEND', b''))

save_composite_png(imgs, str(OUT_PNG))
print(f"Preview: {OUT_PNG}")
