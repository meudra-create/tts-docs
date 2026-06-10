#!/usr/bin/env python3
"""
Appliquer formatage professionnel aux titres de sections liminaires/finales.
Ces titres sont en style Normal mais doivent avoir l'aspect PARTIE.
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

# Titres liminaires à formatter comme des PARTIE (Garamond 19pt #1A1A2E gras centré)
# PAS les entrées du sommaire [47-155]
LIMINAIRE_INDICES = [39, 46, 135, 144, 867]

fixed = 0
for i in LIMINAIRE_INDICES:
    p = paras[i]
    print(f"[{i}] Avant : style={p.style.name!r}, txt={p.text[:50]!r}")

    # Centrer
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Espacement
    pf = p.paragraph_format
    pf.space_before = Pt(24)
    pf.space_after = Pt(18)
    pf.keep_with_next = True

    # Appliquer police aux runs
    for run in p.runs:
        run.font.name = 'Garamond'
        run.font.size = 215900  # 17pt — légèrement inférieur aux PARTIE (19pt)
        run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)
        run.font.bold = True

    # Ajouter bordure dorée en bas (comme Heading 1)
    pPr = p._p.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr')
        p._p.insert(0, pPr)

    old_border = pPr.find(qn('w:pBdr'))
    if old_border is None:
        pBdr = OxmlElement('w:pBdr')
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single')
        bottom.set(qn('w:sz'), '8')
        bottom.set(qn('w:space'), '8')
        bottom.set(qn('w:color'), 'C8A951')
        pBdr.append(bottom)
        pPr.append(pBdr)

    print(f"  → formaté : Garamond 17pt #1A1A2E gras centré, bordure gold")
    fixed += 1

# Formatter aussi les titres inline dans le front-matter (titre, sous-titre, auteur)
print(f"\n=== FRONT-MATTER TITLE PAGE [0-25] ===")
for i in range(min(25, len(paras))):
    p = paras[i]
    txt = p.text.strip()
    if not txt:
        continue
    print(f"[{i:3d}] style={p.style.name!r:20s} | {txt[:60]!r}")

doc.save(OUTPUT)
print(f"\n✓ {fixed} sections liminaires formatées")
print(f"✓ Sauvegardé : {OUTPUT}")
