#!/usr/bin/env python3
"""Génère LIVRE-FINAL.pdf depuis LIVRE-FINAL.md via WeasyPrint (Ardoise & Or, format KDP 6x9)."""

import re
import unicodedata
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
BORDEAUX  = "#8B1A1A"

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

/* ── PAGES DE PARTIE ──────────────────────────────────────── */
.partie-page {{
    page-break-before: always;
    page-break-after: always;
    text-align: center;
    padding-top: 2.6in;
    background: {BLANC};
}}

.partie-label {{
    font-family: 'Crimson Text', 'FreeSerif', serif;
    font-size: 10pt;
    font-weight: 600;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: {ARDOISE};
    margin-bottom: 0.6em;
}}

.partie-title {{
    font-family: 'Crimson Text', 'FreeSerif', serif;
    font-size: 20pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: {ARDOISE};
    line-height: 1.2;
    margin-bottom: 0.7em;
}}

.partie-rule {{
    width: 55%;
    margin: 0 auto;
    border-top: 1pt solid {OR_SATIN};
}}

/* ── CHAPITRES ────────────────────────────────────────────── */
h1 {{
    font-family: 'Crimson Text', 'FreeSerif', serif;
    font-size: 13pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: {BLANC};
    background: {ARDOISE};
    text-align: left;
    margin-top: 0;
    margin-bottom: 2.0em;
    margin-left: -1.2in;
    margin-right: -1.2in;
    padding: 0.7em 1.2in 0.7em 1.2in;
    page-break-before: always;
    line-height: 1.3;
    border-top: 4pt solid {OR_SATIN};
    border-bottom: 1pt solid {ARDOISE_L};
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
blockquote, blockquote.cite {{
    background: {BLANC};
    border-left: 1pt solid {OR_SATIN};
    border-top: none;
    border-bottom: none;
    margin: 1.6em 0;
    padding: 0.4em 1.2em 0.4em 1.4em;
    page-break-inside: avoid;
}}

.cite-text {{
    text-indent: 0;
    margin: 0.1em 0;
    font-style: italic;
    color: {BORDEAUX};
    font-size: 11pt;
    line-height: 1.60;
}}

.cite-author {{
    text-indent: 0;
    margin: 0.1em 0;
    font-style: italic;
    color: {GRIS_TX};
    font-size: 10.5pt;
    line-height: 1.45;
}}

blockquote p {{
    text-indent: 0;
    margin: 0.15em 0;
    color: {BORDEAUX};
    font-style: italic;
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

/* ── SOMMAIRE ─────────────────────────────────────────────── */
.toc {{
    page-break-before: always;
    page-break-after: always;
    padding-top: 0.4em;
}}

.toc-heading {{
    font-family: 'Crimson Text', 'FreeSerif', serif;
    font-size: 18pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.10em;
    color: {ARDOISE};
    text-align: center;
    margin-bottom: 1.6em;
    padding-bottom: 0.5em;
    border-bottom: 2pt solid {OR_SATIN};
}}

.toc-matter {{
    font-family: 'Crimson Text', 'FreeSerif', serif;
    font-size: 10pt;
    font-style: italic;
    color: {ARDOISE};
    margin: 0.5em 0;
    display: block;
    width: 100%;
}}

.toc-matter a {{
    color: {ARDOISE};
    text-decoration: none;
    display: block;
    width: 100%;
}}

.toc-matter a::after {{
    content: leader('.') target-counter(attr(href url), page);
    font-style: normal;
    font-size: 9.5pt;
    color: {OR_SATIN};
}}

.toc-partie {{
    font-family: 'Crimson Text', 'FreeSerif', serif;
    font-size: 8.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    color: {OR_SATIN};
    margin-top: 1.3em;
    margin-bottom: 0.25em;
    padding-top: 0.55em;
    border-top: 0.5pt solid {OR_SATIN};
}}

.toc-partie-label {{
    font-weight: 700;
}}

.toc-partie-name {{
    font-weight: 400;
    letter-spacing: 0.04em;
    text-transform: none;
    font-size: 9pt;
}}

.toc-chapter {{
    font-family: 'EB Garamond', 'FreeSerif', serif;
    font-size: 10pt;
    color: {GRIS_TX};
    margin: 0.18em 0;
    padding-left: 0.6em;
    line-height: 1.35;
    display: block;
    width: 100%;
}}

.toc-chapter a {{
    color: {GRIS_TX};
    text-decoration: none;
    display: block;
    width: 100%;
}}

.toc-chapter a::after {{
    content: leader('.') target-counter(attr(href url), page);
    font-size: 9.5pt;
    color: {ARDOISE};
}}

.toc-chap-num {{
    color: {ARDOISE};
    font-variant: small-caps;
    font-weight: 600;
}}
"""

def make_slug(text):
    """Génère un slug ASCII pour les IDs d'ancres HTML."""
    nfkd = unicodedata.normalize('NFD', text)
    s = ''.join(c for c in nfkd if unicodedata.category(c) != 'Mn')
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s-]", '', s)
    s = re.sub(r'[\s-]+', '-', s.strip())
    return s[:60]

def build_toc(md_text: str) -> str:
    """Construit le HTML du sommaire depuis la liste des titres H1."""
    items = []
    for line in md_text.split('\n'):
        m = re.match(r'^# (.+)$', line)
        if not m:
            continue
        title = m.group(1).strip()
        if title.lower() == 'sommaire':
            continue
        items.append(title)

    parts = [
        '<div class="toc">',
        '<div class="toc-heading">Sommaire</div>',
    ]

    for title in items:
        slug = make_slug(title)
        partie_m = re.match(r'^(PARTIE\s+[IVX]+)\s+[—–]\s+(.+)$', title)
        chapter_m = re.match(r'^(Chapitre\s+\d+)\s+[—–]\s+(.+)$', title)

        if partie_m:
            label = partie_m.group(1)
            name = partie_m.group(2)
            pslug = make_slug(f"{label} {name}")
            parts.append(
                f'<div class="toc-partie">'
                f'<span class="toc-partie-label">{label} — </span>'
                f'<span class="toc-partie-name">{name}</span>'
                f'</div>'
            )
        elif chapter_m:
            num = chapter_m.group(1)
            name = chapter_m.group(2)
            parts.append(
                f'<div class="toc-chapter">'
                f'<a href="#{slug}">'
                f'<span class="toc-chap-num">{num}</span>'
                f' — {name}'
                f'</a>'
                f'</div>'
            )
        else:
            parts.append(
                f'<div class="toc-matter"><a href="#{slug}">{title}</a></div>'
            )

    parts.append('</div>')
    return '\n'.join(parts)

def inline_md(s):
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', s)
    return s

def convert_encadre(m):
    block = m.group(1)
    title = None
    rows = []
    for line in block.split('\n'):
        s = line.strip()
        if not s:
            continue
        tm = re.match(r'^\*\*(.+?)\*\*$', s)
        letters = [c for c in tm.group(1) if c.isalpha()] if tm else []
        upper_title = tm and bool(letters) and sum(1 for c in letters if c.isupper()) / len(letters) > 0.5
        if tm and upper_title:
            title = tm.group(1)
        elif s.startswith('- '):
            rows.append(inline_md(s[2:]))
        else:
            rows.append(inline_md(s))
    th = f'<thead><tr><th class="enc-th">{title}</th></tr></thead>' if title else ''
    tds = ''.join(f'<tr><td class="enc-td">{r}</td></tr>' for r in rows)
    return f'\n<table class="enc">\n{th}\n<tbody>\n{tds}\n</tbody>\n</table>\n'

def convert_partie(m):
    label = m.group(1).strip()   # "PARTIE I"
    title = m.group(2).strip()   # "L'AFRIQUE AVANT LA DOMINATION"
    slug = make_slug(f"{label} {title}")
    return (
        f'\n<div class="partie-page" id="{slug}">'
        f'<div class="partie-label">{label}</div>'
        f'<div class="partie-title">{title}</div>'
        f'<div class="partie-rule"></div>'
        f'</div>\n'
    )

def split_inline_author(s):
    """Sépare une citation « … » d'une attribution sur la même ligne.

    Reconnaît deux formes après le guillemet fermant » :
      « citation » — Auteur
      « citation » (Auteur, date)
    Retourne (citation, auteur). auteur == '' si aucune attribution inline.
    """
    m = re.match(r'^(.*»)\s*[—–]\s+(.+)$', s)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    m = re.match(r'^(.*»)\s*\((.+)\)\s*$', s)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return s.strip(), ''

def convert_blockquotes(text: str) -> str:
    lines = text.split('\n')
    out = []
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith('>'):
            group = []
            while i < len(lines) and lines[i].lstrip().startswith('>'):
                group.append(lines[i].lstrip()[1:].strip())
                i += 1
            group = [g for g in group if g]

            # Découpe le groupe en citations individuelles : chaque ligne
            # contenant une citation ouvre une unité ; une ligne « — Auteur »
            # complète l'unité courante.
            units = []  # [ [citation, auteur], ... ]
            for g in group:
                if re.match(r'^[—–-]\s', g):
                    auth = re.sub(r'^[—–-]\s*', '', g).strip()
                    if units:
                        prev = units[-1][1]
                        units[-1][1] = (prev + ' ' + auth).strip() if prev else auth
                    else:
                        units.append(['', auth])
                else:
                    quote, author = split_inline_author(g)
                    units.append([quote, author])

            out.append('')
            for quote, author in units:
                html = '<blockquote class="cite">'
                if quote:
                    html += f'<p class="cite-text">{inline_md(quote)}</p>'
                if author:
                    html += f'<p class="cite-author">— {inline_md(author)}</p>'
                html += '</blockquote>'
                out.append(html)
            out.append('')
        else:
            out.append(lines[i])
            i += 1
    return '\n'.join(out)

def preprocess(text: str) -> str:
    # 1. Générer et injecter le sommaire avant toute autre transformation
    toc_html = build_toc(text)
    text = re.sub(
        r'^# Sommaire\n.*?(?=^# )',
        toc_html + '\n\n',
        text, count=1, flags=re.DOTALL | re.MULTILINE
    )

    # 2. Convertir les pages de PARTIE (avec id)
    text = re.sub(r'^# (PARTIE\s+[IVX]+)\s+—\s+(.+)$', convert_partie, text, flags=re.MULTILINE)

    # 3. Ajouter id aux titres H1 restants (attr_list extension)
    def add_id(m):
        title = m.group(1).strip()
        slug = make_slug(title)
        return f'# {title} {{ #{slug} }}'
    text = re.sub(r'^# (.+)$', add_id, text, flags=re.MULTILINE)

    # 4. Citations, étoiles, encadrés
    text = convert_blockquotes(text)
    text = re.sub(r'^\s*★\s*★\s*★\s*$', '<div class="stars">★★★</div>', text, flags=re.MULTILINE)
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
