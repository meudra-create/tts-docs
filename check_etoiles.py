#!/usr/bin/env python3
from docx import Document
from docx.oxml.ns import qn

doc = Document('/home/user/tts-docs/LA_PAIX_ON_PEUT_L_EVITER_CORRIGE.docx')
paras = doc.paragraphs

print("=== ÉTAT DE TOUTES LES ÉTOILES ===\n")
for i, p in enumerate(paras):
    if '★' not in p.text:
        continue
    ali = p.alignment
    runs_info = []
    for run in p.runs:
        clr = None
        try:
            clr = run.font.color.rgb
        except:
            pass
        runs_info.append(f"txt={run.text!r} color={clr} bold={run.font.bold} italic={run.font.italic}")
    print(f"[{i:4d}] align={ali} | txt={p.text!r}")
    for r in runs_info:
        print(f"       run: {r}")
    print()
print(f"Total : {sum(1 for p in paras if '★' in p.text)} étoiles")
