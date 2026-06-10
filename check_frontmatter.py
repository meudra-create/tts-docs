#!/usr/bin/env python3
from docx import Document

CHEMIN = '/home/user/tts-docs/LA_PAIX_ON_PEUT_L_EVITER_CORRIGE.docx'
doc = Document(CHEMIN)
paras = doc.paragraphs

# Chercher PROLOGUE, INTRODUCTION, EPILOGUE (tous styles)
print("=== SECTIONS LIMINAIRES/FINALES (tous styles) ===")
KEYWORDS = ['PROLOGUE', 'INTRODUCTION', 'ÉPILOGUE', 'EPILOGUE', 'REMERCIEMENTS',
            'DÉDICACE', 'CONCLUSION', 'AVANT-PROPOS', 'SOMMAIRE']
for i, p in enumerate(paras):
    txt = p.text.strip()
    upper = txt.upper()
    for kw in KEYWORDS:
        if kw in upper and len(txt) < 80:
            pf = p.paragraph_format
            print(f"[{i:4d}] style={p.style.name!r:20s} pbr={pf.page_break_before} | {txt[:70]!r}")
            break
