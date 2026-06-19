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
OR_SATIN  = "#A07820"
CREME     = "#F2EDE0"
CREME_BD  = "#D6CEB8"
GRIS_TX   = "#3A3A3A"
GRIS_SUB  = "#5A5A5A"

CSS_STYLES = f"""
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
    background: {BLANC};
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
    color: {GRIS_SUB};
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
    color: {BLANC};
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
    background: {BLANC};
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

    print("Génération PDF — thème Ardoise & Or...")
    doc = HTML(string=html, base_url=str(Path(__file__).parent))
    css = CSS(string=CSS_STYLES)
    doc.write_pdf(str(OUT), stylesheets=[css])

    size_kb = OUT.stat().st_size // 1024
    print(f"PDF généré: {OUT.name} — {size_kb} Ko")

if __name__ == "__main__":
    main()
