#!/usr/bin/env python3
from docx import Document
from docx.shared import Cm

doc = Document('/home/user/tts-docs/LA_PAIX_ON_PEUT_L_EVITER_CORRIGE.docx')
paras = doc.paragraphs

KEYWORDS_PARTIE = ['PARTIE', 'ÉPILOGUE', 'EPILOGUE', 'PROLOGUE',
                   'INTRODUCTION', 'AVANT-PROPOS', 'CONCLUSION']

print("=== SOMMAIRE [47–155] ===\n")
errors = []
for i, p in enumerate(paras):
    if i < 47 or i > 155:
        continue
    txt = p.text.strip()
    if not txt:
        continue
    pf = p.paragraph_format
    upper = txt.upper()
    is_partie   = any(kw in upper for kw in KEYWORDS_PARTIE)
    is_chapitre = 'Chapitre' in txt

    if is_partie:
        indent = pf.left_indent or 0
        sp_b   = pf.space_before.pt if pf.space_before else None
        bold   = any(run.font.bold for run in p.runs if run.text.strip())
        ok = indent == 0 and sp_b == 12.0 and bold
        status = '✓' if ok else '✗'
        if not ok:
            errors.append((i, txt[:50], f"indent={indent} sp_before={sp_b} bold={bold}"))
        print(f"[{i:3d}] {status} PARTIE   indent={indent} sp_before={sp_b}pt bold={bold} | {txt[:50]}")

    elif is_chapitre:
        indent = pf.left_indent or 0
        sp_b   = pf.space_before.pt if pf.space_before else None
        bold   = any(run.font.bold for run in p.runs if run.text.strip())
        ok = abs(indent - int(Cm(1.5))) < 1000 and sp_b == 3.0 and not bold
        status = '✓' if ok else '✗'
        if not ok:
            errors.append((i, txt[:50], f"indent={indent} sp_before={sp_b} bold={bold}"))
        print(f"[{i:3d}] {status} CHAPITRE indent={indent} sp_before={sp_b}pt bold={bold} | {txt[:50]}")

print(f"\n{'─'*60}")
if errors:
    print(f"⚠ {len(errors)} erreur(s) :")
    for idx, t, info in errors:
        print(f"  [{idx}] {info} | {t}")
else:
    print("✓ Sommaire 100% conforme")
