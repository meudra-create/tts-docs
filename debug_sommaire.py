#!/usr/bin/env python3
from docx import Document
from docx.oxml.ns import qn
from docx.shared import Cm
from lxml import etree

doc = Document('/home/user/tts-docs/LA_PAIX_ON_PEUT_L_EVITER_CORRIGE.docx')
paras = doc.paragraphs

print("=== XML des entrées chapitre dans le sommaire [73-78] ===\n")
for i in range(73, 79):
    p = paras[i]
    txt = p.text.strip()
    pf  = p.paragraph_format
    ind = pf.left_indent
    pPr = p._p.find(qn('w:pPr'))
    w_ind = None
    if pPr is not None:
        ind_el = pPr.find(qn('w:ind'))
        if ind_el is not None:
            w_ind = ind_el.get(qn('w:left'))
    print(f"[{i}] indent={ind} w:ind/left={w_ind} | {txt[:60]}")
    if pPr is not None:
        print(f"     XML pPr: {etree.tostring(pPr, encoding='unicode')[:200]}")
    print()
