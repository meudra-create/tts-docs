#!/usr/bin/env python3
from docx import Document
from docx.oxml.ns import qn
from lxml import etree

doc = Document('/home/user/tts-docs/LA_PAIX_ON_PEUT_L_EVITER_CORRIGE.docx')
paras = doc.paragraphs

# Comparer Chapitre 12 (induit) vs 13b (non indenté selon image)
for i in [73, 75, 76, 77]:
    p = paras[i]
    print(f"\n{'='*60}")
    print(f"[{i}] {p.text.strip()[:60]}")
    print(f"{'='*60}")
    print(etree.tostring(p._p, encoding='unicode', pretty_print=True)[:1500])
