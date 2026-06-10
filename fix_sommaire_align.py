#!/usr/bin/env python3
"""
Réalignement complet du sommaire :
- Supprime les espaces/tabs en tête de texte
- Force w:ind w:left en XML directement (plus fiable que paragraph_format)
- PARTIE  : left=0,   sp_before=240 twips (12pt), bold=True
- Chapitre: left=850, sp_before=60  twips (3pt),  bold=False
"""

from docx import Document
from docx.shared import Pt, Cm
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

CHEMIN = '/home/user/tts-docs/LA_PAIX_ON_PEUT_L_EVITER_CORRIGE.docx'
doc = Document(CHEMIN)
paras = doc.paragraphs

KEYWORDS_PARTIE = ['PARTIE', 'ÉPILOGUE', 'EPILOGUE', 'PROLOGUE',
                   'INTRODUCTION', 'AVANT-PROPOS', 'CONCLUSION']

def set_ind_xml(p, left_twips, firstline_twips=0):
    """Force w:ind directement dans le XML (contourne les héritages de style)."""
    pPr = p._p.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr')
        p._p.insert(0, pPr)
    ind = pPr.find(qn('w:ind'))
    if ind is None:
        ind = OxmlElement('w:ind')
        pPr.append(ind)
    ind.set(qn('w:left'),      str(left_twips))
    ind.set(qn('w:firstLine'), str(firstline_twips))

def set_spacing_xml(p, before_twips, after_twips=0):
    pPr = p._p.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr')
        p._p.insert(0, pPr)
    sp = pPr.find(qn('w:spacing'))
    if sp is None:
        sp = OxmlElement('w:spacing')
        pPr.append(sp)
    sp.set(qn('w:before'), str(before_twips))
    if after_twips is not None:
        sp.set(qn('w:after'), str(after_twips))

def clean_leading_spaces(p):
    """Supprime les espaces/tabs en tête du premier run non vide."""
    for run in p.runs:
        if run.text:
            run.text = run.text.lstrip(' \t\xa0')
            break

n_partie = n_chap = 0

for i, p in enumerate(paras):
    if i < 47 or i > 155:
        continue
    txt = p.text.strip()
    if not txt:
        continue
    upper = txt.upper()

    is_partie   = any(kw in upper for kw in KEYWORDS_PARTIE)
    is_chapitre = 'Chapitre' in txt or 'CHAPITRE' in upper

    if is_partie:
        clean_leading_spaces(p)
        set_ind_xml(p, left_twips=0, firstline_twips=0)
        set_spacing_xml(p, before_twips=240, after_twips=80)  # 12pt / 4pt
        for run in p.runs:
            run.font.bold = True
        n_partie += 1

    elif is_chapitre:
        clean_leading_spaces(p)
        set_ind_xml(p, left_twips=850, firstline_twips=0)     # 850 twips = Cm(1.5)
        set_spacing_xml(p, before_twips=60, after_twips=0)    # 3pt
        for run in p.runs:
            run.font.bold = False
        n_chap += 1

doc.save(CHEMIN)
print(f"✓ {n_partie} PARTIE  : left=0,   sp_before=12pt, bold=True")
print(f"✓ {n_chap} chapitres : left=850t, sp_before=3pt,  bold=False")
print(f"✓ Espaces en tête nettoyés")
print(f"✓ Sauvegardé : {CHEMIN}")
