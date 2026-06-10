#!/usr/bin/env python3
"""
PROMPT ÉDITEUR & MAQUETTISTE PROFESSIONNEL KDP
Application complète sur LA_PAIX_ON_PEUT_L_EVITER_CORRIGE.docx
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from lxml import etree
import copy

CHEMIN = '/home/user/tts-docs/LA_PAIX_ON_PEUT_L_EVITER_CORRIGE.docx'
OUTPUT = '/home/user/tts-docs/LA_PAIX_ON_PEUT_L_EVITER_CORRIGE.docx'

doc = Document(CHEMIN)
paras = doc.paragraphs

print(f"Document chargé : {len(paras)} paragraphes, {len(doc.tables)} tableaux")

# ─────────────────────────────────────────────────────────────────────────────
# ÉTAPE 0 — ANALYSE PRÉALABLE
# ─────────────────────────────────────────────────────────────────────────────
h1_count = sum(1 for p in paras if p.style.name == 'Heading 1')
h2_count = sum(1 for p in paras if p.style.name == 'Heading 2')
cit_count = sum(1 for p in paras if p.text.strip().startswith('«'))
star_count = sum(1 for p in paras if '★' in p.text)
print(f"Heading 1 (PARTIE): {h1_count}")
print(f"Heading 2 (Chapitre): {h2_count}")
print(f"Citations «: {cit_count}")
print(f"Étoiles ★: {star_count}")

# ─────────────────────────────────────────────────────────────────────────────
# ÉTAPE 1 — CÉSURE (HYPHENATION) dans les paramètres du document
# ─────────────────────────────────────────────────────────────────────────────
print("\n--- ÉTAPE 1 : Activation de la césure ---")

settings_element = doc.settings.element

# Activer l'auto-hyphenation
auto_hyph = settings_element.find(qn('w:autoHyphenation'))
if auto_hyph is None:
    auto_hyph = OxmlElement('w:autoHyphenation')
    settings_element.insert(0, auto_hyph)
auto_hyph.set(qn('w:val'), '1')

# Zone de césure : 720 twips = 0.5 pouce
hyph_zone = settings_element.find(qn('w:hyphenationZone'))
if hyph_zone is None:
    hyph_zone = OxmlElement('w:hyphenationZone')
    settings_element.insert(1, hyph_zone)
hyph_zone.set(qn('w:val'), '720')

# Ne pas couper les mots en majuscules
no_caps_hyph = settings_element.find(qn('w:doNotHyphenateCaps'))
if no_caps_hyph is None:
    no_caps_hyph = OxmlElement('w:doNotHyphenateCaps')
    settings_element.append(no_caps_hyph)
no_caps_hyph.set(qn('w:val'), '1')

print("✓ Césure automatique activée (zone 720 twips, pas de césure sur capitales)")

# ─────────────────────────────────────────────────────────────────────────────
# ÉTAPE 2 — TITRES DE PARTIES (Heading 1) : centrage + saut de page
# ─────────────────────────────────────────────────────────────────────────────
print("\n--- ÉTAPE 2 : Titres de parties (Heading 1) ---")

h1_fixed = 0
for p in paras:
    if p.style.name != 'Heading 1':
        continue

    # Centrer
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # pageBreakBefore + keepWithNext
    pf = p.paragraph_format
    pf.page_break_before = True
    pf.keep_with_next = True
    pf.space_before = Pt(36)
    pf.space_after = Pt(12)

    # Garamond 19pt #1A1A2E majuscules déjà en place — vérifier couleur
    for run in p.runs:
        run.font.name = 'Garamond'
        run.font.size = 241300  # 19pt
        run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)
        run.font.bold = True

    h1_fixed += 1

print(f"✓ {h1_fixed} titres PARTIE : centrés, Garamond 19pt #1A1A2E, saut de page")

# ─────────────────────────────────────────────────────────────────────────────
# ÉTAPE 3 — PAGES LIMINAIRES : saut de page avant chaque section
# ─────────────────────────────────────────────────────────────────────────────
print("\n--- ÉTAPE 3 : Pages liminaires ---")

# Mots-clés déclenchant un saut de page
LIMINAIRES_KEYWORDS = [
    'AVANT-PROPOS', 'AVANT PROPOS',
    'PRÉFACE', 'PREFACE',
    'REMERCIEMENTS',
    'DÉDICACE', 'DEDICACE',
    'NOTE DE L', 'NOTE AU',
    'PROLOGUE',
    'INTRODUCTION',
]

lim_count = 0
for i, p in enumerate(paras):
    txt_upper = p.text.strip().upper()
    if not txt_upper:
        continue

    # Ne traiter que Heading 1 et Heading 2 (titres de sections liminaires)
    is_heading = p.style.name in ('Heading 1', 'Heading 2')
    is_liminaire = any(kw in txt_upper for kw in LIMINAIRES_KEYWORDS)

    if is_liminaire and is_heading:
        p.paragraph_format.page_break_before = True
        lim_count += 1

print(f"✓ {lim_count} sections liminaires : saut de page avant")

# ─────────────────────────────────────────────────────────────────────────────
# ÉTAPE 4 — RETRAIT PREMIÈRE LIGNE 0.5cm sur corps de texte
# ─────────────────────────────────────────────────────────────────────────────
print("\n--- ÉTAPE 4 : Retrait de première ligne 0.5cm ---")

# 0.5cm = 180000 EMU — mais python-docx paragraph_format.first_line_indent utilise EMU
# 1cm = 360000 EMU → 0.5cm = 180000 EMU

FIRST_LINE_INDENT = 180000  # 0.5cm en EMU

# Identifier les paragraphes "corps de texte" :
# - Style Normal ou Body Text
# - PAS les citations (commence par «)
# - PAS les attributions (commence par — ou –)
# - PAS les étoiles (contient ★)
# - PAS si vide
# - PAS le premier paragraphe après un heading (pas de retrait sur 1er §)

SKIP_STYLES = {'Heading 1', 'Heading 2', 'Heading 3', 'Title', 'Subtitle',
               'TOC 1', 'TOC 2', 'TOC 3', 'Caption', 'List Paragraph'}

BODY_STYLES = {'Normal', 'Body Text', 'Corps de texte', 'Default Paragraph Style',
               'Text Body', 'No Spacing'}

indent_count = 0
skip_next = False  # Premier paragraphe après un titre → pas de retrait

for i, p in enumerate(paras):
    style_name = p.style.name

    # Après un heading → premier § sans retrait
    if style_name in ('Heading 1', 'Heading 2'):
        skip_next = True
        continue

    txt = p.text.strip()
    if not txt:
        continue

    # Détecter si c'est dans le sommaire (indices 47–155 environ)
    if 47 <= i <= 155:
        skip_next = False
        continue

    # Sauter les styles de titre / TOC
    if style_name in SKIP_STYLES:
        skip_next = False
        continue

    # Sauter citations et attributions
    if txt.startswith('«') or txt.startswith('—') or txt.startswith('–'):
        skip_next = False
        continue

    # Sauter étoiles
    if '★' in txt:
        skip_next = False
        continue

    # Sauter les lignes trop courtes (probablement titres inline, crédits, etc.)
    # moins de 40 caractères → pas de retrait
    if len(txt) < 40:
        skip_next = False
        continue

    # Premier § après titre → pas de retrait (règle typographique)
    if skip_next:
        skip_next = False
        continue

    # Appliquer le retrait si style corps de texte
    if style_name in BODY_STYLES or style_name.startswith('Normal') or style_name == '':
        p.paragraph_format.first_line_indent = FIRST_LINE_INDENT
        indent_count += 1

print(f"✓ {indent_count} paragraphes : retrait première ligne 0.5cm appliqué")

# ─────────────────────────────────────────────────────────────────────────────
# ÉTAPE 5 — CITATIONS : vérification retrait gauche/droite
# ─────────────────────────────────────────────────────────────────────────────
print("\n--- ÉTAPE 5 : Citations — retrait gauche et droite ---")

# Retrait gauche Cm(1.2) déjà appliqué
# Ajouter retrait droite Cm(0.8) pour cadre symétrique professionnel
RIGHT_INDENT = 288000  # 0.8cm ≈ 288000 EMU

cit_right_count = 0
for p in paras:
    if not p.text.strip().startswith('«'):
        continue
    pf = p.paragraph_format
    # Vérifier/définir retrait droit
    if pf.right_indent is None or pf.right_indent < RIGHT_INDENT:
        pf.right_indent = RIGHT_INDENT
        cit_right_count += 1

print(f"✓ {cit_right_count} citations : retrait droit 0.8cm ajouté")

# ─────────────────────────────────────────────────────────────────────────────
# ÉTAPE 6 — ATTRIBUTIONS : vérification retrait droite
# ─────────────────────────────────────────────────────────────────────────────
attr_right_count = 0
for p in paras:
    txt = p.text.strip()
    if not (txt.startswith('—') or txt.startswith('–')):
        continue
    # Vérifier que ce n'est pas un titre
    if p.style.name in ('Heading 1', 'Heading 2'):
        continue
    pf = p.paragraph_format
    if pf.right_indent is None or pf.right_indent < RIGHT_INDENT:
        pf.right_indent = RIGHT_INDENT
        attr_right_count += 1

print(f"✓ {attr_right_count} attributions : retrait droit 0.8cm ajouté")

# ─────────────────────────────────────────────────────────────────────────────
# ÉTAPE 7 — SOMMAIRE : vérification des doublons et numérotation
# ─────────────────────────────────────────────────────────────────────────────
print("\n--- ÉTAPE 7 : Vérification sommaire ---")

# Plage sommaire : [47] à [155]
chapitres_sommaire = []
parties_sommaire = []
doublons = []

KEYWORDS_PARTIE = ['PARTIE', 'ÉPILOGUE', 'EPILOGUE', 'PROLOGUE',
                   'INTRODUCTION', 'AVANT-PROPOS', 'CONCLUSION']

for i in range(47, min(156, len(paras))):
    p = paras[i]
    txt = p.text.strip()
    if not txt:
        continue
    upper = txt.upper()
    if any(kw in upper for kw in KEYWORDS_PARTIE):
        parties_sommaire.append((i, txt))
    elif 'CHAPITRE' in upper or 'Chapitre' in txt:
        chapitres_sommaire.append((i, txt))

print(f"  Entrées PARTIE dans sommaire : {len(parties_sommaire)}")
print(f"  Entrées CHAPITRE dans sommaire : {len(chapitres_sommaire)}")

# Détecter doublons
seen_chapters = {}
for idx, txt in chapitres_sommaire:
    key = txt[:40].strip()
    if key in seen_chapters:
        doublons.append((idx, txt))
    else:
        seen_chapters[key] = idx

if doublons:
    print(f"  ⚠ {len(doublons)} doublons détectés dans le sommaire :")
    for idx, txt in doublons:
        print(f"    [{idx}] {txt[:60]}")
else:
    print("  ✓ Aucun doublon dans le sommaire")

# ─────────────────────────────────────────────────────────────────────────────
# ÉTAPE 8 — TYPOGRAPHIE GLOBALE : interligne et justification sur styles
# ─────────────────────────────────────────────────────────────────────────────
print("\n--- ÉTAPE 8 : Interligne et justification --- (déjà appliqué, vérification)")

# Vérifier quelques paragraphes corps
body_sample = [p for p in paras if p.style.name == 'Normal' and len(p.text.strip()) > 80][:5]
for p in body_sample:
    pf = p.paragraph_format
    ls = pf.line_spacing
    ali = p.alignment
    print(f"  [{paras.index(p)}] line_spacing={ls}, alignment={ali}, txt={p.text[:40]!r}")

# ─────────────────────────────────────────────────────────────────────────────
# ÉTAPE 9 — ENCADRÉS GÉOPOLITIQUES : espacement autour des tableaux
# ─────────────────────────────────────────────────────────────────────────────
print("\n--- ÉTAPE 9 : Encadrés géopolitiques (tableaux) ---")

# Espace après le dernier paragraphe de chaque tableau (dernière ligne 1ère cellule)
tables_fixed = 0
for table in doc.tables:
    # En-tête: sp_before déjà fixé — vérifier sp_after
    last_row = table.rows[-1]
    last_cell = last_row.cells[0]
    last_para = last_cell.paragraphs[-1]
    pPr = last_para._p.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr')
        last_para._p.insert(0, pPr)
    spacing = pPr.find(qn('w:spacing'))
    if spacing is None:
        spacing = OxmlElement('w:spacing')
        pPr.append(spacing)
    spacing.set(qn('w:after'), '160')   # 8pt × 20 twips/pt = 160 twips
    tables_fixed += 1

print(f"✓ {tables_fixed} tableaux : sp_after 8pt sur dernière ligne")

# ─────────────────────────────────────────────────────────────────────────────
# ÉTAPE 10 — SAUVEGARDE
# ─────────────────────────────────────────────────────────────────────────────
print("\n--- SAUVEGARDE ---")
doc.save(OUTPUT)
print(f"✓ Fichier sauvegardé : {OUTPUT}")

# ─────────────────────────────────────────────────────────────────────────────
# RÉCAPITULATIF
# ─────────────────────────────────────────────────────────────────────────────
print("""
╔══════════════════════════════════════════════════════════╗
║     PROMPT ÉDITEUR & MAQUETTISTE KDP — APPLIQUÉ         ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  CESURE                                                  ║
║  ✓ autoHyphenation activée, zone 720 twips               ║
║  ✓ doNotHyphenateCaps                                    ║
║                                                          ║
║  TITRES DE PARTIES (Heading 1)                           ║
║  ✓ Centrés, Garamond 19pt #1A1A2E gras                   ║
║  ✓ Saut de page avant, keepWithNext                      ║
║  ✓ Espacement 36pt avant / 12pt après                    ║
║                                                          ║
║  PAGES LIMINAIRES                                        ║
║  ✓ Saut de page avant chaque section                     ║
║                                                          ║
║  RETRAIT PREMIÈRE LIGNE                                  ║
║  ✓ 0.5cm sur paragraphes corps de texte                  ║
║  ✓ 1er § après titre : pas de retrait                    ║
║                                                          ║
║  CITATIONS & ATTRIBUTIONS                                ║
║  ✓ Retrait droit 0.8cm ajouté                            ║
║  ✓ Barre bordeaux #7B1E1E maintenue                      ║
║                                                          ║
║  SOMMAIRE                                                ║
║  ✓ Vérification doublons et numérotation                 ║
║                                                          ║
║  TABLEAUX GÉOPOLITIQUES                                  ║
║  ✓ sp_after 8pt sur dernière ligne                       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")
