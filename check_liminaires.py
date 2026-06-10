#!/usr/bin/env python3
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

CHEMIN = '/home/user/tts-docs/LA_PAIX_ON_PEUT_L_EVITER_CORRIGE.docx'
doc = Document(CHEMIN)
paras = doc.paragraphs

# Afficher tous les paragraphes de style Heading 1 et 2 + leurs indices
print("=== HEADINGS DANS LE DOCUMENT ===")
for i, p in enumerate(paras):
    s = p.style.name
    if s in ('Heading 1', 'Heading 2'):
        pf = p.paragraph_format
        pbr = pf.page_break_before
        print(f"[{i:4d}] {s:12s} pageBreak={pbr} | {p.text[:70]!r}")

print("\n=== PARAGRAPHES [0–50] (front-matter) ===")
for i, p in enumerate(paras[:50]):
    s = p.style.name
    txt = p.text.strip()
    if txt:
        print(f"[{i:3d}] style={s!r:25s} | {txt[:60]!r}")
