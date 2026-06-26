#!/usr/bin/env python3
"""Génère le DOCX complet (chapitres 1–66) depuis les sources markdown réécrites,
en réutilisant le style de append_chapters.py (FreeSerif, bandeaux ardoise/or)."""
import os, glob
from docx import Document
from docx.shared import Pt

# Réutilise toutes les fonctions de style/parsing existantes
import importlib.util
spec = importlib.util.spec_from_file_location(
    "ac", os.path.join(os.path.dirname(__file__), "append_chapters.py"))

# On ne peut pas exécuter append_chapters tel quel (il a un __main__ qui agit).
# On copie donc les helpers en les important via exec du segment fonctions.
src_path = os.path.join(os.path.dirname(__file__), "append_chapters.py")
with open(src_path, "r", encoding="utf-8") as f:
    code = f.read()
# Coupe avant la section Main
code = code.split("# ─── Main", 1)[0]
ns = {}
exec(compile(code, src_path, "exec"), ns)

add_page_break   = ns["add_page_break"]
styled_run       = ns["styled_run"]
GOLD_RGB         = ns["GOLD_RGB"]
ARDOISE_RGB      = ns["ARDOISE_RGB"]
WHITE_RGB        = ns["WHITE_RGB"]
GRIS_RGB         = ns["GRIS_RGB"]
ARDOISE          = ns["ARDOISE"]
CREAM_HEX        = ns["CREAM_HEX"]
BORDER_SZ        = ns["BORDER_SZ"]
set_cell_fill    = ns["set_cell_fill"]
set_table_borders= ns["set_table_borders"]
_parse_inner     = ns["parse_and_append"]
import re as _re
from docx.shared import Cm as _Cm

def _clean_inline(t):
    t = _re.sub(r'\*\*(.+?)\*\*', r'\1', t)
    t = _re.sub(r'\*(.+?)\*', r'\1', t)
    t = _re.sub(r'`(.+?)`', r'\1', t)
    return t.strip()

def _split_row(line):
    s = line.strip()
    if s.startswith('|'): s = s[1:]
    if s.endswith('|'):   s = s[:-1]
    return [c.strip() for c in s.split('|')]

def add_pipe_table(doc, header, rows):
    n = max(1, len(header))
    table = doc.add_table(rows=1 + len(rows), cols=n)
    set_table_borders(table, BORDER_SZ, ARDOISE)
    for c, htext in enumerate(header):
        cell = table.rows[0].cells[c]
        set_cell_fill(cell, ARDOISE)
        cell.paragraphs[0].paragraph_format.left_indent = _Cm(0.15)
        styled_run(cell.paragraphs[0], _clean_inline(htext),
                   color=WHITE_RGB, bold=True, size=9.5)
    for r, row in enumerate(rows):
        cells = row[:n] + [''] * (n - len(row))
        for c, val in enumerate(cells):
            cell = table.rows[r + 1].cells[c]
            set_cell_fill(cell, CREAM_HEX)
            cell.paragraphs[0].paragraph_format.left_indent = _Cm(0.15)
            styled_run(cell.paragraphs[0], _clean_inline(val),
                       color=GRIS_RGB, size=9)
    doc.add_paragraph()

def parse_and_append(doc, md_text):
    """Pré-traite les tableaux pipe markdown, délègue le reste au parseur de base."""
    lines = md_text.split('\n')
    i = 0
    buf = []
    def flush():
        if buf:
            _parse_inner(doc, '\n'.join(buf)); buf.clear()
    while i < len(lines):
        line = lines[i]
        if (_re.match(r'^\s*\|.*\|\s*$', line)
                and i + 1 < len(lines)
                and _re.match(r'^\s*\|[\s:|\-]+\|\s*$', lines[i+1])
                and '-' in lines[i+1]):
            flush()
            header = _split_row(line)
            j = i + 2; body = []
            while j < len(lines) and _re.match(r'^\s*\|.*\|\s*$', lines[j]):
                body.append(_split_row(lines[j])); j += 1
            add_pipe_table(doc, header, body)
            i = j; continue
        buf.append(line); i += 1
    flush()

# ─── Page de titre ────────────────────────────────────────────────────────────
doc = Document()
# Marges raisonnables conservées du gabarit Word par défaut

# Titre
for _ in range(6):
    doc.add_paragraph()
p = doc.add_paragraph(); p.alignment = 1
styled_run(p, "LA PAIX, ON PEUT L'ÉVITER", color=ARDOISE_RGB, bold=True, size=28, caps=True)
p = doc.add_paragraph(); p.alignment = 1
styled_run(p, "★★★", color=GOLD_RGB, size=18)
p = doc.add_paragraph(); p.alignment = 1
styled_run(p,
    "De Berlin à l'Alliance des États du Sahel — "
    "anatomie d'une domination et d'une rupture",
    color=ARDOISE_RGB, italic=True, size=14)

# ─── Chapitres 1–66 ───────────────────────────────────────────────────────────
chapter_dir = "/home/user/tts-docs/content/3.livre/"
files = sorted(
    glob.glob(os.path.join(chapter_dir, "[0-9]*.md")),
    key=lambda x: int(os.path.basename(x).split(".")[0]))

print(f"Assemblage de {len(files)} chapitres...")
for filepath in files:
    num = int(os.path.basename(filepath).split(".")[0])
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2].strip()
    add_page_break(doc)
    parse_and_append(doc, content)
    print(f"  ✓ {num}: {os.path.basename(filepath)[:55]}")

out = "/home/user/tts-docs/la-paix-on-peut-leviter.docx"
doc.save(out)
print(f"\nSaved: {out}  ({os.path.getsize(out)/1024:.1f} KB)")
