#!/usr/bin/env python3
"""Analyse complète des polices, tailles et couleurs — détection des anomalies."""

from docx import Document
from docx.oxml.ns import qn
from collections import Counter

doc = Document('/home/user/tts-docs/LA_PAIX_ON_PEUT_L_EVITER_CORRIGE.docx')
paras = doc.paragraphs

fonts   = Counter()
sizes   = Counter()
colors  = Counter()
anomalies = []

EXPECTED = {
    'Heading 1' : {'font': 'Garamond', 'size': 241300, 'color': '1A1A2E'},
    'Heading 2' : {'font': 'Garamond', 'size': 177800, 'color': '1A1A2E'},
    'Normal'    : {'font': None,       'size': 139700, 'color': None},
}

for i, p in enumerate(paras):
    style = p.style.name
    txt   = p.text.strip()
    if not txt:
        continue
    for run in p.runs:
        if not run.text.strip():
            continue
        fn  = run.font.name
        fsz = run.font.size
        try:
            clr = str(run.font.color.rgb) if run.font.color and run.font.color.type else None
        except:
            clr = None

        if fn:  fonts[fn]  += 1
        if fsz: sizes[int(fsz)] += 1
        if clr: colors[clr] += 1

        # Détecter les anomalies par rapport aux attendus
        if style in EXPECTED:
            exp = EXPECTED[style]
            if exp['font'] and fn and fn != exp['font']:
                anomalies.append((i, style, f"font={fn!r} attendu={exp['font']!r}", txt[:40]))
            if exp['color'] and clr and clr != exp['color']:
                anomalies.append((i, style, f"color={clr!r} attendu={exp['color']!r}", txt[:40]))

print("=== POLICES UTILISÉES ===")
for f, n in fonts.most_common():
    print(f"  {n:4d}×  {f!r}")

print("\n=== TAILLES (EMU) ===")
for s, n in sorted(sizes.items(), reverse=True):
    pt = round(s / 12700, 1)
    print(f"  {n:4d}×  {s} ({pt}pt)")

print("\n=== COULEURS ===")
for c, n in colors.most_common():
    print(f"  {n:4d}×  #{c}")

print(f"\n=== ANOMALIES ({len(anomalies)}) ===")
seen = set()
for idx, style, msg, txt in anomalies[:30]:
    key = (style, msg)
    if key not in seen:
        seen.add(key)
        print(f"  [{idx:4d}] {style:12s} {msg} | {txt!r}")
