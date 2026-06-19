#!/usr/bin/env python3
"""Génère LIVRE-FINAL.pdf depuis LIVRE-FINAL.md via WeasyPrint (Ardoise & Or, format KDP 6x9)."""

import re
import markdown
from weasyprint import HTML, CSS
from pathlib import Path

SRC = Path(__file__).parent / "LIVRE-FINAL.md"
OUT = Path(__file__).parent / "LIVRE-FINAL.pdf"

BLANC     = "#FFFFFF"
ARDOISE   = "#2C3A4A"
ARDOISE_L = "#3D5068"
OR_SATIN  = "#A07820"
OR_CLAIR  = "#C9A24A"
CREME     = "#F4EFE4"
CREME_BD  = "#D8CEBC"
GRIS_TX   = "#2E2E2E"
GRIS_SUB  = "#555555"

CSS_STYLES = f"""
@import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;0,700;1,400;1,600&family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&display=swap');

/* ── MISE EN PAGE ─────────────────────────────────────────── */
@page {{
    size: 6in 9in;
    margin-top: 0.80in;
    margin-bottom: 0.90in;
    margin-left: 0.80in;
    margin-right: 0.60in;

    @bottom-center {{
        content: "— " counter(page) " —";
        font-family: 'Crimson Text', 'FreeSerif', serif;
        font-size: 9pt;
        color: #A8A8A0;
        letter-spacing: 0.15em;
    }}
}}

@page :left {{
    margin-left: 0.60in;
    margin-right: 0.80in;
}}

@page :blank {{
    @bottom-center {{ content: ''; }}
}}

/* ── CORPS ────────────────────────────────────────────────── */
body {{
    font-family: 'EB Garamond', 'FreeSerif', Georgia, serif;
    font-size: 11.5pt;
    line-height: 1.63;
    color: {GRIS_TX};
    background: {BLANC};
    text-align: justify;
    hyphens: auto;
}}

/* ── CHAPITRES ────────────────────────────────────────────── */
h1 {{
    font-family: 'Crimson Text', 'FreeSerif', serif;
    font-size: 21pt;
    font-weight: 600;
    color: {BLANC};
    background: {ARDOISE};
    text-align: left;
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
}}

/* ── SECTIONS ─────────────────────────────────────────────── */
h2 {{
    font-family: 'Crimson Text', 'FreeSerif', serif;
    font-size: 10.5pt;
    font-weight: 600;
    font-variant: small-caps;
    letter-spacing: 0.16em;
    text-transform: lowercase;
    color: {ARDOISE};
    margin-top: 2.4em;
    margin-bottom: 0.75em;
    padding-bottom: 0.35em;
    border-bottom: 1pt solid {OR_SATIN};
}}

/* ── SOUS-SECTIONS ────────────────────────────────────────── */
h3 {{
    font-family: 'EB Garamond', serif;
    font-size: 11.5pt;
    font-weight: 500;
    font-style: italic;
    color: {OR_SATIN};
    margin-top: 1.7em;
    margin-bottom: 0.35em;
}}

/* ── PARAGRAPHES ──────────────────────────────────────────── */
p {{
    margin: 0 0 0 0;
    text-indent: 1.4em;
    orphans: 3;
    widows: 3;
}}

p + p {{
    margin-top: 0.1em;
}}

p:first-of-type,
h1 + p, h2 + p, h3 + p,
blockquote + p, hr + p, .stars + p, .encadre + p {{
    text-indent: 0;
}}

/* ── CITATIONS EN EXERGUE ─────────────────────────────────── */
blockquote {{
    background: {BLANC};
    border-left: 3pt solid {OR_SATIN};
    border-top: 0.5pt solid {CREME_BD};
    border-bottom: 0.5pt solid {CREME_BD};
    margin: 1.6em 0;
    padding: 0.9em 1.2em 0.9em 1.5em;
    font-style: italic;
    color: {GRIS_SUB};
    page-break-inside: avoid;
    font-size: 11pt;
    line-height: 1.58;
}}

blockquote p {{
    text-indent: 0;
    margin: 0.15em 0;
    color: {GRIS_SUB};
}}

/* ── LISTES ───────────────────────────────────────────────── */
ul, ol {{
    margin: 0.6em 0 0.6em 1.5em;
    padding: 0;
}}

li {{
    margin-bottom: 0.4em;
    line-height: 1.56;
}}

/* ── EMPHASE ──────────────────────────────────────────────── */
em {{
    font-style: italic;
}}

strong {{
    font-weight: 600;
    color: {ARDOISE};
}}

/* ── SÉPARATEUR ───────────────────────────────────────────── */
hr {{
    border: none;
    border-top: 0.5pt solid {CREME_BD};
    margin: 2.4em auto;
    width: 30%;
}}

/* ── ÉTOILES (séparateur de section) ─────────────────────── */
.stars {{
    text-align: center;
    color: {OR_SATIN};
    font-size: 13pt;
    margin: 2.0em 0;
    letter-spacing: 1.0em;
    page-break-after: avoid;
}}

/* ── TABLEAUX ─────────────────────────────────────────────── */
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1.5em 0;
    font-size: 10pt;
    page-break-inside: avoid;
}}

th {{
    background: {ARDOISE};
    color: {BLANC};
    padding: 0.55em 0.8em;
    text-align: left;
    font-weight: 600;
    font-family: 'Crimson Text', serif;
    font-variant: small-caps;
    letter-spacing: 0.07em;
    font-size: 10.5pt;
    border-bottom: 2.5pt solid {OR_SATIN};
}}

td {{
    border-bottom: 0.5pt solid {CREME_BD};
    padding: 0.45em 0.8em;
    vertical-align: top;
}}

tr:nth-child(even) td {{
    background: {CREME};
}}

tr:last-child td {{
    border-bottom: 1pt solid {ARDOISE};
}}

/* ── ENCADRÉS (format table) ──────────────────────────────── */
table.enc {{
    width: 100%;
    border-collapse: collapse;
    margin: 1.8em 0;
    page-break-inside: avoid;
    border: 1pt solid {ARDOISE};
    font-size: 10.5pt;
}}

.enc-th {{
    background: {ARDOISE};
    color: {BLANC};
    text-align: left;
    font-family: 'Crimson Text', 'FreeSerif', serif;
    font-size: 9.5pt;
    font-weight: 700;
    font-style: normal;
    font-variant: normal;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    padding: 0.65em 1.0em;
    border: none;
    line-height: 1.3;
}}

.enc-td {{
    background: {CREME};
    border-top: 0.5pt solid {CREME_BD};
    padding: 0.55em 1.0em;
    vertical-align: top;
    line-height: 1.52;
    text-indent: 0;
}}

/* ── CODE ─────────────────────────────────────────────────── */
code {{
    font-family: monospace;
    font-size: 9pt;
    background: {CREME};
    padding: 0.1em 0.3em;
}}

/* ── LIENS ────────────────────────────────────────────────── */
a {{
    color: {OR_SATIN};
    text-decoration: none;
}}
"""

def convert_encadre(m):
    block = m.group(1)
    title = None
    rows = []
    for line in block.split('\n'):
        s = line.strip()
        if not s:
            continue
        tm = re.match(r'^\*\*(.+?)\*\*$', s)
        if tm and 'ENCADRÉ' in tm.group(1):
            title = tm.group(1)
        elif s.startswith('- '):
            rows.append(s[2:])
        else:
            rows.append(s)
    th = f'<thead><tr><th class="enc-th">{title}</th></tr></thead>' if title else ''
    tds = ''.join(f'<tr><td class="enc-td">{r}</td></tr>' for r in rows)
    return f'\n<table class="enc">\n{th}\n<tbody>\n{tds}\n</tbody>\n</table>\n'

def preprocess(text: str) -> str:
    text = re.sub(r'^\s*★\s*★\s*★\s*$', '<div class="stars">★ ★ ★</div>', text, flags=re.MULTILINE)
    text = re.sub(r'---ENCADRE---\n(.*?)---FIN---', convert_encadre, text, flags=re.DOTALL)
    return text

def md_to_html(md_text: str) -> str:
    md_text = preprocess(md_text)
    extensions = ['extra', 'tables', 'nl2br', 'smarty']
    body = markdown.markdown(md_text, extensions=extensions)
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>La paix, on peut l'éviter</title>
</head>
<body>
{body}
</body>
</html>"""

def main():
    print("Lecture du manuscrit...")
    md_text = SRC.read_text(encoding="utf-8")

    print("Conversion Markdown → HTML...")
    html = md_to_html(md_text)

    print("Génération PDF — thème Ardoise & Or (enrichi)...")
    doc = HTML(string=html, base_url=str(Path(__file__).parent))
    css = CSS(string=CSS_STYLES)
    doc.write_pdf(str(OUT), stylesheets=[css])

    size_kb = OUT.stat().st_size // 1024
    print(f"PDF généré: {OUT.name} — {size_kb} Ko")

if __name__ == "__main__":
    main()
