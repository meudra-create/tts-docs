#!/usr/bin/env python3
"""Preview thème Ivoire & Ardoise — fond ivoire, or satiné, Crimson Text + EB Garamond."""

from weasyprint import HTML, CSS
from pathlib import Path
import fitz, struct, zlib

OUT_PDF = Path("/tmp/preview_ivoire.pdf")
OUT_PNG = Path("/home/user/tts-docs/manuscrit-edition/preview_ivoire.png")

IVOIRE    = "#FFFFFF"
ARDOISE   = "#2C3A4A"
OR_SATIN  = "#A07820"
CREME     = "#F2EDE0"
CREME_BD  = "#D6CEB8"
GRIS_TX   = "#3A3A3A"
GRIS_SUB  = "#5A5A5A"
BLANC     = "#FFFFFF"

CSS_IVOIRE = f"""
@import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;0,700;1,400;1,600&family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&display=swap');

@page {{
    size: 6in 9in;
    margin-top: 0.75in;
    margin-bottom: 0.70in;
    margin-left: 0.80in;
    margin-right: 0.60in;
}}

@page :left {{
    margin-left: 0.60in;
    margin-right: 0.80in;
}}

body {{
    font-family: 'EB Garamond', 'FreeSerif', Georgia, serif;
    font-size: 11.5pt;
    line-height: 1.60;
    color: {GRIS_TX};
    background: {IVOIRE};
    text-align: justify;
    hyphens: auto;
}}

h1 {{
    font-family: 'Crimson Text', 'FreeSerif', serif;
    font-size: 22pt;
    font-weight: 600;
    font-style: normal;
    color: {ARDOISE};
    text-align: left;
    margin-top: 0;
    margin-bottom: 0.3em;
    padding-bottom: 0.4em;
    border-bottom: 1pt solid {OR_SATIN};
    page-break-before: always;
    letter-spacing: 0.01em;
}}

h1 + p {{
    margin-top: 1.2em;
    text-indent: 0;
}}

h2 {{
    font-family: 'Crimson Text', 'FreeSerif', serif;
    font-size: 10.5pt;
    font-weight: 600;
    font-variant: small-caps;
    letter-spacing: 0.12em;
    text-transform: lowercase;
    color: {ARDOISE};
    margin-top: 2em;
    margin-bottom: 0.6em;
    border-bottom: 0.5pt solid {CREME_BD};
    padding-bottom: 0.25em;
}}

h3 {{
    font-family: 'EB Garamond', serif;
    font-size: 11.5pt;
    font-weight: 500;
    font-style: italic;
    color: {OR_SATIN};
    margin-top: 1.4em;
    margin-bottom: 0.3em;
}}

p {{
    margin: 0.25em 0 0.5em 0;
    text-indent: 1.3em;
}}

p:first-of-type, h1 + p, h2 + p, h3 + p, blockquote + p, hr + p {{
    text-indent: 0;
}}

blockquote {{
    background: {CREME};
    border-left: 2pt solid {OR_SATIN};
    margin: 1.4em 0.5em;
    padding: 0.75em 1em;
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
    line-height: 1.55;
}}

em {{
    font-style: italic;
}}

strong {{
    font-weight: 600;
    color: {ARDOISE};
}}

hr {{
    border: none;
    border-top: 0.5pt solid {CREME_BD};
    margin: 2em auto;
    width: 35%;
}}

.stars {{
    text-align: center;
    color: {OR_SATIN};
    font-size: 14pt;
    margin: 1.4em 0;
    letter-spacing: 0.5em;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1.2em 0;
    font-size: 10pt;
    page-break-inside: avoid;
    background: {CREME};
}}

th {{
    background: {ARDOISE};
    color: {IVOIRE};
    padding: 0.45em 0.7em;
    text-align: left;
    font-weight: 600;
    font-family: 'Crimson Text', serif;
    font-variant: small-caps;
    letter-spacing: 0.06em;
    font-size: 10.5pt;
}}

td {{
    border: 0.5pt solid {CREME_BD};
    padding: 0.4em 0.7em;
    vertical-align: top;
    background: {CREME};
}}

tr:nth-child(even) td {{
    background: {IVOIRE};
}}

.encadre {{
    background: {CREME};
    border: 1pt solid {CREME_BD};
    border-left: 3pt solid {OR_SATIN};
    padding: 0.85em 1.1em;
    margin: 1.2em 0;
    page-break-inside: avoid;
}}

code {{
    font-family: monospace;
    font-size: 9pt;
    background: {CREME};
    padding: 0.1em 0.3em;
}}

a {{
    color: {OR_SATIN};
    text-decoration: none;
}}
"""

HTML_PREVIEW = f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><title>Ivoire & Ardoise Preview</title></head>
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
critique structurelle des mécanismes de domination économique et politique hérités de soixante
ans de postcolonialisme.</p>

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
sont explicitement signalées comme telles.
</div>

<p>La vitesse de la rupture avec les partenaires traditionnels — France, CEDEAO, organisations
de Bretton Woods — a surpris les observateurs. En moins de dix-huit mois, l'ensemble de
l'architecture sécuritaire, diplomatique et économique héritée de la Françafrique a été remise
en cause de façon méthodique.</p>

<h2>III. Les acteurs de la transition</h2>

<table>
<tr><th>État</th><th>Chef de transition</th><th>Date du coup</th><th>Partenaire pivot</th></tr>
<tr><td>Mali</td><td>Col. Assimi Goïta</td><td>Août 2020 / Mai 2021</td><td>Russie / Wagner</td></tr>
<tr><td>Burkina Faso</td><td>Capt. Ibrahim Traoré</td><td>Septembre 2022</td><td>Russie / AES</td></tr>
<tr><td>Niger</td><td>Gén. Abdourahamane Tiani</td><td>Juillet 2023</td><td>AES / Chine</td></tr>
</table>

<p>Ces trois transitions partagent une même grammaire politique : légitimation par la rupture avec
la tutelle française, appel à une souveraineté pleine et entière, réorientation des partenariats
vers des puissances non-occidentales.</p>

</body>
</html>"""

print("Génération PDF preview Ivoire & Ardoise...")
doc = HTML(string=HTML_PREVIEW, base_url="/tmp")
css = CSS(string=CSS_IVOIRE)
doc.write_pdf(str(OUT_PDF), stylesheets=[css])
print(f"PDF: {OUT_PDF} ({OUT_PDF.stat().st_size // 1024} Ko)")

print("Conversion PDF → PNG...")
pdf = fitz.open(str(OUT_PDF))
pages_to_render = min(len(pdf), 3)

imgs = []
for i in range(pages_to_render):
    page = pdf[i]
    mat = fitz.Matrix(2.5, 2.5)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    imgs.append(pix)

gap = 24
total_h = sum(p.height for p in imgs) + (len(imgs) - 1) * gap
max_w = max(p.width for p in imgs)

def png_chunk(name, data):
    c = zlib.crc32(name + data) & 0xFFFFFFFF
    return struct.pack('>I', len(data)) + name + data + struct.pack('>I', c)

composite = bytearray(total_h * max_w * 3)
for i in range(len(composite)):
    composite[i] = 255  # fond blanc

y_off = 0
for pix in imgs:
    for row in range(pix.height):
        src = pix.samples[row * pix.width * 3:(row + 1) * pix.width * 3]
        dst_start = (y_off + row) * max_w * 3
        composite[dst_start:dst_start + len(src)] = src
    y_off += pix.height + gap

raw_rows = bytearray()
for row in range(total_h):
    raw_rows.append(0)
    raw_rows.extend(composite[row * max_w * 3:(row + 1) * max_w * 3])
compressed = zlib.compress(bytes(raw_rows), 6)

with open(str(OUT_PNG), 'wb') as f:
    f.write(b'\x89PNG\r\n\x1a\n')
    f.write(png_chunk(b'IHDR', struct.pack('>IIBBBBB', max_w, total_h, 8, 2, 0, 0, 0)))
    f.write(png_chunk(b'IDAT', compressed))
    f.write(png_chunk(b'IEND', b''))

print(f"Preview: {OUT_PNG}")
