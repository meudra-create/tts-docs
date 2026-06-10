#!/usr/bin/env python3
"""
Formatage professionnel de la page de titre et des épigraphes.
"""

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

CHEMIN = '/home/user/tts-docs/LA_PAIX_ON_PEUT_L_EVITER_CORRIGE.docx'
OUTPUT = CHEMIN

doc = Document(CHEMIN)
paras = doc.paragraphs

print("=== FORMATAGE PAGE DE TITRE ===")

# ── [2] Série/éditeur : Alliance des États du Sahel
p = paras[2]
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in p.runs:
    run.font.name = 'Garamond'
    run.font.size = 139700  # 11pt
    run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)
    run.font.bold = False
    run.font.italic = True
pf = p.paragraph_format
pf.space_before = Pt(48)
pf.space_after = Pt(6)
print(f"[2] Alliance des États du Sahel → Garamond 11pt italique centré")

# ── [3] Titre PARTIE 1 : LA PAIX,
p = paras[3]
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in p.runs:
    run.font.name = 'Garamond'
    run.font.size = 406400  # 32pt
    run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)
    run.font.bold = True
pf = p.paragraph_format
pf.space_before = Pt(24)
pf.space_after = Pt(0)
print(f"[3] LA PAIX, → Garamond 32pt gras centré")

# ── [4] Titre PARTIE 2 : ON PEUT L'ÉVITER
p = paras[4]
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in p.runs:
    run.font.name = 'Garamond'
    run.font.size = 406400  # 32pt
    run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)
    run.font.bold = True
pf = p.paragraph_format
pf.space_before = Pt(0)
pf.space_after = Pt(18)
print(f"[4] ON PEUT L'ÉVITER → Garamond 32pt gras centré")

# ── [6] Sous-titre
p = paras[6]
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in p.runs:
    run.font.name = 'Garamond'
    run.font.size = 165100  # 13pt
    run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)
    run.font.bold = False
    run.font.italic = True
pf = p.paragraph_format
pf.space_before = Pt(6)
pf.space_after = Pt(60)

# Bordure dorée dessous
pPr = p._p.find(qn('w:pPr'))
if pPr is None:
    pPr = OxmlElement('w:pPr')
    p._p.insert(0, pPr)
if pPr.find(qn('w:pBdr')) is None:
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '12')
    bottom.set(qn('w:color'), 'C8A951')
    pBdr.append(bottom)
    pPr.append(pBdr)
print(f"[6] Géopolitique... → Garamond 13pt italique centré + bordure gold")

# ── [21] Auteur
p = paras[21]
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in p.runs:
    run.font.name = 'Garamond'
    run.font.size = 190500  # 15pt
    run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)
    run.font.bold = True
pf = p.paragraph_format
pf.space_before = Pt(60)
pf.space_after = Pt(4)
print(f"[21] BEN-H2O → Garamond 15pt gras centré")

# ── [22] Année
p = paras[22]
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in p.runs:
    run.font.name = 'Garamond'
    run.font.size = 139700  # 11pt
    run.font.color.rgb = RGBColor(0x7B, 0x1E, 0x1E)  # bordeaux
    run.font.bold = False
pf = p.paragraph_format
pf.space_before = Pt(2)
pf.space_after = Pt(2)
print(f"[22] — 2026 — → Garamond 11pt bordeaux centré")

# ── ÉPIGRAPHES [26-37] : s'assurer qu'elles démarrent sur une nouvelle page
p_epi = paras[26]
pf = p_epi.paragraph_format
pf.page_break_before = True
pf.space_before = Pt(48)
print(f"[26] Épigraphes → saut de page avant")

# ── Vérification finale : compter les paragraphes avec retrait
indent_count = sum(
    1 for p in paras
    if p.paragraph_format.first_line_indent is not None
    and p.paragraph_format.first_line_indent > 0
)
print(f"\n✓ {indent_count} paragraphes avec retrait de première ligne")

doc.save(OUTPUT)
print(f"✓ Sauvegardé : {OUTPUT}")
