#!/usr/bin/env python3
"""
Harmonisation complète des polices, tailles et couleurs.
Palette officielle :
  #1A1A2E  — Navy    → titres
  #7B1E1E  — Bordeaux → citations, étoiles
  #C8A951  — Gold    → bordures (pas dans les runs)
  Auto/None — corps de texte (noir naturel Word)
"""

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

CHEMIN = '/home/user/tts-docs/LA_PAIX_ON_PEUT_L_EVITER_CORRIGE.docx'

NAVY     = RGBColor(0x1A, 0x1A, 0x2E)
BORDEAUX = RGBColor(0x7B, 0x1E, 0x1E)

# Couleurs à normaliser → couleur cible
# None = supprimer la couleur explicite (auto = noir Word)
COLOR_MAP = {
    '8B0000': BORDEAUX,   # faux bordeaux → bordeaux spec
    '943634': BORDEAUX,   # autre faux bordeaux
    'D99594': None,       # rose anormal → auto
    '4A4A4A': None,       # gris foncé → auto
    '555555': None,       # gris attributions → auto
    '1A1A1A': None,       # quasi-noir corps → auto
}

# Polices anormales → Garamond
BAD_FONTS = {'Segoe UI Symbol', 'Calibri', 'Arial', 'Times New Roman',
             'Times', 'Helvetica', 'Cambria'}

# Tailles non conformes à corriger (en EMU) → taille cible
# 12pt paragraphes Normal → 11pt
SIZE_FIX = {
    355600: 139700,    # 28pt étoile → 11pt (la couleur/centrage déjà OK)
    152400: 139700,    # 12pt sous-titres → 11pt
}

doc = Document(CHEMIN)
paras = doc.paragraphs

stats = {
    'color_fixed':  0,
    'color_auto':   0,
    'font_fixed':   0,
    'size_fixed':   0,
    'star_fixed':   0,
}

# ─── Correction dans les paragraphes ─────────────────────────
for p in paras:
    txt = p.text.strip()
    if not txt:
        continue

    is_copyright = any(m in txt for m in [
        '©', 'ISBN', 'Dépôt légal', 'Tous droits réservés',
        'Kindle Direct Publishing', 'autorisation écrite',
        'Première édition', 'Format : 15,24',
    ])

    for run in p.runs:
        if not run.text.strip():
            continue

        # ── 1. Police ──────────────────────────────────────
        if run.font.name in BAD_FONTS:
            run.font.name = 'Garamond'
            stats['font_fixed'] += 1
            if '★' in run.text:
                stats['star_fixed'] += 1

        # ── 2. Taille ──────────────────────────────────────
        if run.font.size in SIZE_FIX:
            # Ne pas toucher aux étoiles (leur taille est gérée séparément)
            if '★' not in run.text:
                run.font.size = SIZE_FIX[run.font.size]
                stats['size_fixed'] += 1
            else:
                # Étoile à 28pt → normaliser à 12pt (taille lisible centrée)
                run.font.size = 152400   # 12pt
                stats['star_fixed'] += 1

        # ── 3. Couleur ─────────────────────────────────────
        if is_copyright:
            continue   # garder le gris #404040 intentionnel sur la page copyright

        try:
            clr = str(run.font.color.rgb) if run.font.color and run.font.color.type else None
        except Exception:
            clr = None

        if clr and clr.upper() in COLOR_MAP:
            target = COLOR_MAP[clr.upper()]
            if target is not None:
                run.font.color.rgb = target
                stats['color_fixed'] += 1
            else:
                # Supprimer la couleur explicite → héritage automatique (noir)
                rPr = run._r.find(qn('w:rPr'))
                if rPr is not None:
                    clr_el = rPr.find(qn('w:color'))
                    if clr_el is not None:
                        rPr.remove(clr_el)
                stats['color_auto'] += 1

# ─── Correction dans les cellules de tableaux ────────────────
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for cp in cell.paragraphs:
                for run in cp.runs:
                    if not run.text.strip():
                        continue
                    if run.font.name in BAD_FONTS:
                        run.font.name = 'Garamond'
                        stats['font_fixed'] += 1
                    try:
                        clr = str(run.font.color.rgb) if run.font.color and run.font.color.type else None
                    except Exception:
                        clr = None
                    if clr and clr.upper() in COLOR_MAP:
                        target = COLOR_MAP[clr.upper()]
                        if target is not None:
                            run.font.color.rgb = target
                            stats['color_fixed'] += 1
                        else:
                            rPr = run._r.find(qn('w:rPr'))
                            if rPr is not None:
                                clr_el = rPr.find(qn('w:color'))
                                if clr_el is not None:
                                    rPr.remove(clr_el)
                            stats['color_auto'] += 1

# ─── Vérification post-correction ────────────────────────────
from collections import Counter
fonts_after  = Counter()
colors_after = Counter()
for p in paras:
    for run in p.runs:
        if not run.text.strip(): continue
        if run.font.name: fonts_after[run.font.name]  += 1
        try:
            clr = str(run.font.color.rgb) if run.font.color and run.font.color.type else 'auto'
        except:
            clr = 'auto'
        colors_after[clr] += 1

doc.save(CHEMIN)

print("╔══════════════════════════════════════════════════════╗")
print("║      HARMONISATION DES POLICES — RAPPORT            ║")
print("╠══════════════════════════════════════════════════════╣")
print(f"║  Couleurs corrigées  (→ palette)   : {stats['color_fixed']:4d}          ║")
print(f"║  Couleurs normalisées (→ auto noir) : {stats['color_auto']:4d}          ║")
print(f"║  Polices corrigées   (→ Garamond)  : {stats['font_fixed']:4d}          ║")
print(f"║  Tailles corrigées   (→ 11pt)      : {stats['size_fixed']:4d}          ║")
print(f"║  Étoiles corrigées                 : {stats['star_fixed']:4d}          ║")
print("╠══════════════════════════════════════════════════════╣")
print("║  POLICES RESTANTES                                   ║")
for f, n in fonts_after.most_common():
    print(f"║    {n:4d}×  {f:<46s}║")
print("╠══════════════════════════════════════════════════════╣")
print("║  COULEURS RESTANTES                                  ║")
for c, n in colors_after.most_common():
    print(f"║    {n:4d}×  #{c:<45s}║")
print("╚══════════════════════════════════════════════════════╝")
print(f"\n✓ Sauvegardé : {CHEMIN}")
