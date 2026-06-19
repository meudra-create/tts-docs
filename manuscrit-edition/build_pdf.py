#!/usr/bin/env python3
"""Génère LIVRE-FINAL.pdf depuis LIVRE-FINAL.md via WeasyPrint (Sahel Rouge theme, format KDP 6x9)."""

import re
import markdown
from weasyprint import HTML, CSS
from pathlib import Path

SRC = Path(__file__).parent / "LIVRE-FINAL.md"
OUT = Path(__file__).parent / "LIVRE-FINAL.pdf"

ROUGE   = "#8B1A1A"
OR      = "#D4A017"
NOIR    = "#0A0A0A"
IVOIRE  = "#F5F0E8"

CSS_STYLES = f"""
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&display=swap');

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
    line-height: 1.5;
    color: {NOIR};
    background: white;
    text-align: justify;
    hyphens: auto;
}}

h1 {{
    font-size: 22pt;
    font-weight: 700;
    color: {ROUGE};
    text-align: center;
    margin-top: 2em;
    margin-bottom: 0.5em;
    page-break-before: always;
    border-bottom: 3pt solid {OR};
    padding-bottom: 0.3em;
}}

h2 {{
    font-size: 14pt;
    font-weight: 600;
    color: {ROUGE};
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    border-left: 4pt solid {OR};
    padding-left: 0.4em;
}}

h3 {{
    font-size: 12pt;
    font-weight: 600;
    color: {ROUGE};
    margin-top: 1.2em;
    margin-bottom: 0.3em;
}}

p {{
    margin: 0.4em 0 0.6em 0;
    text-indent: 1.2em;
}}

p:first-of-type, h1 + p, h2 + p, h3 + p, blockquote + p, hr + p {{
    text-indent: 0;
}}

blockquote {{
    background: {IVOIRE};
    border-left: 4pt solid {OR};
    margin: 1em 0.5em;
    padding: 0.6em 0.8em;
    font-style: italic;
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
    margin-bottom: 0.3em;
    line-height: 1.4;
}}

em {{
    font-style: italic;
}}

strong {{
    font-weight: 700;
    color: {ROUGE};
}}

hr {{
    border: none;
    border-top: 1pt solid {OR};
    margin: 1.5em auto;
    width: 60%;
}}

.stars {{
    text-align: center;
    color: {OR};
    font-size: 14pt;
    margin: 1em 0;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 10pt;
    page-break-inside: avoid;
}}

th {{
    background: {ROUGE};
    color: {IVOIRE};
    padding: 0.4em 0.6em;
    text-align: left;
    font-weight: 600;
}}

td {{
    border: 0.5pt solid #ccc;
    padding: 0.35em 0.6em;
    vertical-align: top;
}}

tr:nth-child(even) td {{
    background: {IVOIRE};
}}

.encadre {{
    background: {IVOIRE};
    border: 1.5pt solid {OR};
    border-radius: 3pt;
    padding: 0.8em 1em;
    margin: 1em 0;
    page-break-inside: avoid;
}}

code {{
    font-family: monospace;
    font-size: 9pt;
    background: #f0f0f0;
    padding: 0.1em 0.3em;
}}

a {{
    color: {ROUGE};
    text-decoration: none;
}}
"""

def preprocess(text: str) -> str:
    """Transformations pré-conversion: étoiles, encadrés, etc."""
    # ★ ★ ★ → classe .stars
    text = re.sub(r'^\s*★\s*★\s*★\s*$', '<div class="stars">★ ★ ★</div>', text, flags=re.MULTILINE)
    # ---ENCADRE--- blocks → div.encadre
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

    print("Génération PDF via WeasyPrint...")
    doc = HTML(string=html, base_url=str(Path(__file__).parent))
    css = CSS(string=CSS_STYLES)
    doc.write_pdf(str(OUT), stylesheets=[css])

    size_kb = OUT.stat().st_size // 1024
    print(f"PDF généré: {OUT.name} — {size_kb} Ko")

if __name__ == "__main__":
    main()
