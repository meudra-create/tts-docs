#!/usr/bin/env python3
"""
Uniformisation des citations et attributions — modèle photo 1 :
- Citation «...»   : barre bordeaux + texte italique couleur #7B1E1E
- Attribution —... : italique, couleur #7B1E1E, pas de barre
"""

from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

CHEMIN = '/home/user/tts-docs/LA_PAIX_ON_PEUT_L_EVITER_CORRIGE.docx'
BORDEAUX = RGBColor(0x7B, 0x1E, 0x1E)

doc = Document(CHEMIN)
paras = doc.paragraphs

cit_count = attr_count = 0

for p in paras:
    txt = p.text.strip()
    if not txt:
        continue

    # ── Citations «...» ──────────────────────────────────────
    if txt.startswith('«'):
        for run in p.runs:
            run.font.italic    = True
            run.font.color.rgb = BORDEAUX   # texte bordeaux comme la barre
        cit_count += 1

    # ── Attributions — ... ───────────────────────────────────
    elif (txt.startswith('—') or txt.startswith('–')) \
            and p.style.name not in ('Heading 1', 'Heading 2'):
        for run in p.runs:
            run.font.italic    = True
            run.font.color.rgb = BORDEAUX   # même couleur que la citation
        attr_count += 1

doc.save(CHEMIN)
print(f"✓ {cit_count} citations  : italique, couleur #7B1E1E")
print(f"✓ {attr_count} attributions : italique, couleur #7B1E1E")
print(f"✓ Sauvegardé : {CHEMIN}")
