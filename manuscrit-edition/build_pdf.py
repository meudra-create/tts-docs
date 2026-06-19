#!/usr/bin/env python3
"""Génère LIVRE-FINAL.pdf depuis LIVRE-FINAL.md via WeasyPrint (Nuit de Bamako, format KDP 6x9)."""

import re
import markdown
from weasyprint import HTML, CSS
from pathlib import Path

SRC = Path(__file__).parent / "LIVRE-FINAL.md"
OUT = Path(__file__).parent / "LIVRE-FINAL.pdf"

GRAPHITE  = "#121212"
INDIGO    = "#4A5CFF"
OR_CHAUD  = "#E8C547"
BLANC     = "#FFFFFF"
NUIT      = "#0D1020"
GRIS_DOUX = "#F2F2F0"
GRIS_MID  = "#E0E0DC"

CSS_STYLES = f"""
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;600;700&family=EB+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&display=swap');

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
    font-family: 'EB Garamond', 'FreeSans', 'Liberation Sans', serif;
    font-size: 11pt;
    line-height: 1.55;
    color: {GRAPHITE};
    background: {BLANC};
    text-align: justify;
    hyphens: auto;
}}

h1 {{
    font-family: 'Oswald', 'FreeSans', sans-serif;
    font-size: 20pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: {OR_CHAUD};
    background: {GRAPHITE};
    text-align: left;
    margin-top: 0;
    margin-bottom: 1.2em;
    margin-left: -0.80in;
    margin-right: -0.60in;
    padding: 0.7em 0.80in 0.6em 0.80in;
    page-break-before: always;
    border-bottom: 3pt solid {INDIGO};
}}

h2 {{
    font-family: 'Oswald', 'FreeSans', sans-serif;
    font-size: 13pt;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: {INDIGO};
    margin-top: 1.6em;
    margin-bottom: 0.5em;
    border-left: 4pt solid {OR_CHAUD};
    padding-left: 0.45em;
}}

h3 {{
    font-family: 'EB Garamond', serif;
    font-size: 12pt;
    font-weight: 700;
    font-style: italic;
    color: {INDIGO};
    margin-top: 1.2em;
    margin-bottom: 0.3em;
}}

p {{
    margin: 0.35em 0 0.55em 0;
    text-indent: 1.2em;
}}

p:first-of-type, h1 + p, h2 + p, h3 + p, blockquote + p, hr + p {{
    text-indent: 0;
}}

blockquote {{
    background: {NUIT};
    border-left: 4pt solid {INDIGO};
    margin: 1.2em 0.3em;
    padding: 0.7em 0.9em;
    font-style: italic;
    color: #D4D0C8;
    page-break-inside: avoid;
}}

blockquote p {{
    text-indent: 0;
    margin: 0.2em 0;
    color: #D4D0C8;
}}

ul, ol {{
    margin: 0.5em 0 0.5em 1.5em;
    padding: 0;
}}

li {{
    margin-bottom: 0.3em;
    line-height: 1.4;
}}

em {{
    font-style: italic;
}}

strong {{
    font-weight: 700;
    color: {INDIGO};
}}

hr {{
    border: none;
    border-top: 1.5pt solid {OR_CHAUD};
    margin: 1.8em auto;
    width: 50%;
}}

.stars {{
    text-align: center;
    color: {OR_CHAUD};
    font-size: 15pt;
    margin: 1.2em 0;
    letter-spacing: 0.3em;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 10pt;
    page-break-inside: avoid;
}}

th {{
    background: {GRAPHITE};
    color: {OR_CHAUD};
    padding: 0.4em 0.6em;
    text-align: left;
    font-weight: 600;
    font-family: 'Oswald', sans-serif;
    letter-spacing: 0.04em;
}}

td {{
    border: 0.5pt solid {GRIS_MID};
    padding: 0.35em 0.6em;
    vertical-align: top;
}}

tr:nth-child(even) td {{
    background: {GRIS_DOUX};
}}

.encadre {{
    background: {GRIS_DOUX};
    border: 2pt solid {INDIGO};
    border-left: 5pt solid {OR_CHAUD};
    padding: 0.8em 1em;
    margin: 1em 0;
    page-break-inside: avoid;
}}

code {{
    font-family: monospace;
    font-size: 9pt;
    background: {GRIS_DOUX};
    padding: 0.1em 0.3em;
}}

a {{
    color: {INDIGO};
    text-decoration: none;
}}
"""

def preprocess(text: str) -> str:
    text = re.sub(r'^\s*★\s*★\s*★\s*$', '<div class="stars">★ ★ ★</div>', text, flags=re.MULTILINE)
    text = re.sub(r'^---ENCADRE---\s*$', '<div class="encadre">\n', text, flags=re.MULTILINE)
    text = re.sub(r'^---FIN---\s*$', '</div>\n', text, flags=re.MULTILINE)
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

    print("Génération PDF — thème Nuit de Bamako...")
    doc = HTML(string=html, base_url=str(Path(__file__).parent))
    css = CSS(string=CSS_STYLES)
    doc.write_pdf(str(OUT), stylesheets=[css])

    size_kb = OUT.stat().st_size // 1024
    print(f"PDF généré: {OUT.name} — {size_kb} Ko")

if __name__ == "__main__":
    main()
