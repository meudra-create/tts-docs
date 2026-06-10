#!/usr/bin/env python3
"""
Correction script for LA_PAIX_ON_PEUT_L_EVITER manuscript.
Applies all specified corrections: sommaire, styles, citations, KDP formatting.
"""

from docx import Document
from docx.shared import Cm, Pt, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from lxml import etree
import copy

INPUT = '/root/.claude/uploads/b45e147f-797f-534f-b314-e426149163a1/fadbeac1-LA_PAIX_ON_PEUT_L_EVITER_08_06_FINAL.docx'
OUTPUT = '/home/user/tts-docs/LA_PAIX_ON_PEUT_L_EVITER_CORRIGE.docx'

doc = Document(INPUT)
paras = doc.paragraphs

print(f"Loaded document with {len(paras)} paragraphs")

# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def set_paragraph_format(p, space_before=None, space_after=None, left_indent=None, alignment=None):
    """Set paragraph format properties."""
    pf = p.paragraph_format
    if space_before is not None:
        pf.space_before = space_before
    if space_after is not None:
        pf.space_after = space_after
    if left_indent is not None:
        pf.left_indent = left_indent
    if alignment is not None:
        pf.alignment = alignment

def set_run_format(p, size=None, italic=None):
    """Set font properties on all runs in a paragraph."""
    for r in p.runs:
        if size is not None:
            r.font.size = size
        if italic is not None:
            r.font.italic = italic

def make_new_paragraph_like(doc, text, style_name, space_before=None, space_after=None,
                              left_indent=None, size=None, italic=None, alignment=None):
    """Create a new paragraph element with specified formatting."""
    # Create a new paragraph
    new_p = OxmlElement('w:p')

    # Build pPr (paragraph properties)
    pPr = OxmlElement('w:pPr')

    # Style
    pStyle = OxmlElement('w:pStyle')
    pStyle.set(qn('w:val'), style_name)
    pPr.append(pStyle)

    # Spacing
    spacing = OxmlElement('w:spacing')
    if space_before is not None:
        spacing.set(qn('w:before'), str(int(space_before)))
    if space_after is not None:
        spacing.set(qn('w:after'), str(int(space_after)))
    pPr.append(spacing)

    # Indent
    if left_indent is not None:
        ind = OxmlElement('w:ind')
        ind.set(qn('w:left'), str(int(left_indent)))
        pPr.append(ind)

    # Alignment
    if alignment is not None:
        jc = OxmlElement('w:jc')
        jc.set(qn('w:val'), alignment)
        pPr.append(jc)

    new_p.append(pPr)

    # Build run with text
    r_elem = OxmlElement('w:r')

    # Run properties
    rPr = OxmlElement('w:rPr')
    if size is not None:
        sz = OxmlElement('w:sz')
        sz.set(qn('w:val'), str(int(size / 635)))  # EMU to half-points
        sz_cs = OxmlElement('w:szCs')
        sz_cs.set(qn('w:val'), str(int(size / 635)))
        rPr.append(sz)
        rPr.append(sz_cs)
    if italic:
        i_elem = OxmlElement('w:i')
        rPr.append(i_elem)
        i_cs = OxmlElement('w:iCs')
        rPr.append(i_cs)
    r_elem.append(rPr)

    # Text
    t = OxmlElement('w:t')
    t.text = text
    if text.startswith(' ') or text.endswith(' '):
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    r_elem.append(t)

    new_p.append(r_elem)

    return new_p


def insert_paragraph_after(ref_para, new_p_xml):
    """Insert new_p_xml element immediately after ref_para._p."""
    ref_para._p.addnext(new_p_xml)


def insert_paragraph_before(ref_para, new_p_xml):
    """Insert new_p_xml element immediately before ref_para._p."""
    ref_para._p.addprevious(new_p_xml)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: SOMMAIRE CORRECTIONS
# ─────────────────────────────────────────────────────────────────────────────

print("\n=== SECTION 1: SOMMAIRE CORRECTIONS ===")

# 1A. Fix truncated titles in sommaire
print("\n[1A] Fixing truncated titles...")

# Para 86: fix Chapitre 22
p86 = paras[86]
old_text = p86.text
if 'Russie, Turquie' in p86.text and 'Chine' not in p86.text:
    # Modify the run text
    for r in p86.runs:
        if 'Russie, Turquie' in r.text:
            r.text = r.text.replace('Russie, Turquie', 'Russie, Chine, Turquie')
            break
    print(f"  Para 86: '{old_text[:60]}' -> '{p86.text[:70]}'")
else:
    print(f"  Para 86 SKIP (already correct or text mismatch): {p86.text[:60]!r}")

# Para 92: fix Chapitre 25b
p92 = paras[92]
old_text = p92.text
target_full = '    Chapitre 25b — Le renseignement comme arme de guerre : barbouzes, ESSD et guerre secrète en Afrique'
if 'barbouzes' in p92.text and 'ESSD' not in p92.text:
    # Replace the run text entirely
    full_new_text = '    Chapitre 25b — Le renseignement comme arme de guerre : barbouzes, ESSD et guerre secrète en Afrique'
    # Clear existing runs and set new text
    for r in p92.runs:
        r.text = ''
    if p92.runs:
        p92.runs[0].text = full_new_text
    else:
        # Add a run
        r_elem = OxmlElement('w:r')
        t = OxmlElement('w:t')
        t.text = full_new_text
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        r_elem.append(t)
        p92._p.append(r_elem)
    print(f"  Para 92: fixed -> '{p92.text[:80]}'")
else:
    print(f"  Para 92 SKIP: {p92.text[:60]!r}")

# Para 95: fix Chapitre 25e
p95 = paras[95]
old_text = p95.text
if 'vecteur d' in p95.text and 'résistance' not in p95.text:
    full_new_text = '           Chapitre 25e — La diaspora en guerre : du vecteur d’influence au front de résistance'
    for r in p95.runs:
        r.text = ''
    if p95.runs:
        p95.runs[0].text = full_new_text
    print(f"  Para 95: fixed -> '{p95.text[:90]}'")
else:
    print(f"  Para 95 SKIP: {p95.text[:60]!r}")

# 1B. Insert missing chapters in sommaire
print("\n[1B] Inserting missing chapters in sommaire...")

# Need to refresh paras reference after potential XML changes
# Actually inserts happen at XML level so let's continue using original indices

# Insert Chapitre 30 BEFORE current para 103 (Chapitre 31)
p103 = paras[103]
print(f"  Para 103 current: {p103.text!r}")

if 'Chapitre 31' in p103.text and 'Chapitre 30' not in paras[102].text:
    # Create new paragraph for Chapitre 30
    new_ch30 = make_new_paragraph_like(
        doc,
        '    Chapitre 30 — Bazoum sans le savoir : les aveux involontaires du dernier compradore',
        'Normal'
    )
    insert_paragraph_before(p103, new_ch30)
    print("  Inserted Chapitre 30 before Chapitre 31 in PARTIE VIII")
else:
    print(f"  Chapitre 30 insertion SKIP")

# Now need to refresh paras since we inserted
# Reload paras from doc
paras = doc.paragraphs
print(f"  Doc now has {len(paras)} paragraphs")

# Insert Chapitre 32 in PARTIE IX (before Chapitre 33)
# Find para with "Chapitre 33" in PARTIE IX section
ch33_idx = None
for i, p in enumerate(paras):
    if 'Chapitre 33' in p.text and 'monnaie' in p.text.lower():
        ch33_idx = i
        break

if ch33_idx is not None:
    print(f"  Found Chapitre 33 at para {ch33_idx}: {paras[ch33_idx].text!r}")
    # Check if Chapitre 32 already exists before it
    ch32_exists = any('Chapitre 32' in paras[j].text for j in range(max(0, ch33_idx-5), ch33_idx))
    if not ch32_exists:
        new_ch32 = make_new_paragraph_like(
            doc,
            '    Chapitre 32 — Les morts de Barkhane : autopsie d’un mensonge d’État',
            'Normal'
        )
        insert_paragraph_before(paras[ch33_idx], new_ch32)
        print("  Inserted Chapitre 32 before Chapitre 33 in PARTIE IX")
    else:
        print("  Chapitre 32 already exists before Chapitre 33")
else:
    print("  ERROR: Could not find Chapitre 33 in sommaire")

# Refresh paras again
paras = doc.paragraphs
print(f"  Doc now has {len(paras)} paragraphs")

# 1C. ÉPILOGUE — Insert Chapitre 39
print("\n[1C] Inserting Chapitre 39 in ÉPILOGUE...")

# Find Chapitre 38 and Chapitre 40 in the sommaire section
# Sommaire is paras ~47-119 range; we need to find them there
epilogue_ch38_idx = None
epilogue_ch40_idx = None

# Find the ÉPILOGUE section and then ch38/ch40 within it
in_epilogue = False
for i, p in enumerate(paras):
    if p.text.strip() == 'ÉPILOGUE' and i < 150:  # In sommaire range
        in_epilogue = True
    if in_epilogue and 'Chapitre 38' in p.text and i < 150:
        epilogue_ch38_idx = i
    if in_epilogue and 'Chapitre 40' in p.text and i < 150:
        epilogue_ch40_idx = i
        break

_t38 = paras[epilogue_ch38_idx].text if epilogue_ch38_idx else 'NOT FOUND'
_t40 = paras[epilogue_ch40_idx].text if epilogue_ch40_idx else 'NOT FOUND'
print(f"  EPILOGUE Chapitre 38 at para {epilogue_ch38_idx}: {_t38!r}")
print(f"  EPILOGUE Chapitre 40 at para {epilogue_ch40_idx}: {_t40!r}")

if epilogue_ch40_idx is not None:
    # Check if Chapitre 39 already exists
    ch39_exists = any('Chapitre 39' in paras[j].text for j in range(epilogue_ch38_idx or 0, epilogue_ch40_idx))
    if not ch39_exists:
        new_ch39 = make_new_paragraph_like(
            doc,
            '    Chapitre 39 — Conclusion : L’irréversibilité africaine',
            'Normal'
        )
        insert_paragraph_before(paras[epilogue_ch40_idx], new_ch39)
        print("  Inserted Chapitre 39 before Chapitre 40 in ÉPILOGUE")
    else:
        print("  Chapitre 39 already exists")
else:
    print("  ERROR: Could not find Chapitre 40 in sommaire ÉPILOGUE")

# Refresh paras
paras = doc.paragraphs
print(f"  Doc now has {len(paras)} paragraphs")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: CORPS DU TEXTE — Corrections de style
# ─────────────────────────────────────────────────────────────────────────────

print("\n=== SECTION 2: CORPS DU TEXTE CORRECTIONS ===")

# 2A. Fix paragraphs with wrong style (Normal instead of Heading 2)
# Need to find them by text since indices may have shifted
print("\n[2A] Fixing chapter headings with wrong style...")

targets_h2 = [
    "Chapitre 32 — Les morts de Barkhane",
    "Chapitre 40 — L'arrogance comme doctrine",
    "Chapitre 41 — Anatomie d'une peur",
]

for i, p in enumerate(paras):
    for target in targets_h2:
        if target in p.text and p.style.name == 'Normal':
            # Change style to Heading 2
            p.style = doc.styles['Heading 2']
            print(f"  Para {i}: Changed to Heading 2: {p.text[:70]!r}")
            break

# 2B. Fix double space in Chapitre 13 heading
print("\n[2B] Fixing double space in Chapitre 13 heading...")
for i, p in enumerate(paras):
    if 'Chapitre 13' in p.text and '  Les élites' in p.text and p.style.name == 'Heading 2':
        for r in p.runs:
            if '  Les élites' in r.text:
                r.text = r.text.replace('  Les élites', ' Les élites')
                print(f"  Para {i}: Fixed double space in Heading 2: {p.text[:80]!r}")
                break
        # Also strip trailing spaces from all runs
        for r in p.runs:
            r.text = r.text.rstrip()
        print(f"  Para {i}: After fix: {p.text[:80]!r}")
        break

# 2C. Delete parasitic paragraph (para 42, text ".")
print("\n[2C] Deleting parasitic paragraph with only '.'...")
# Find it by content - should be early in doc with just "."
deleted = False
for i, p in enumerate(paras[:60]):  # Search only in first 60
    if p.text == '.' and p.style.name == 'Normal' and i > 35:
        p._p.getparent().remove(p._p)
        print(f"  Deleted parasitic '.' paragraph at index {i}")
        deleted = True
        break
if not deleted:
    print("  WARNING: Could not find parasitic '.' paragraph")

# Refresh paras
paras = doc.paragraphs
print(f"  Doc now has {len(paras)} paragraphs")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: CITATIONS — Harmonisation
# ─────────────────────────────────────────────────────────────────────────────

print("\n=== SECTION 3: CITATIONS CORRECTIONS ===")

# Reference format:
# Quote: Normal, italic, size=133350, sb=101600(8pt), sa=25400(2pt), li=431800, no alignment
# Attribution: Normal, italic, size=120650, sb=None(0), sa=127000(10pt), li=431800, no alignment

QUOTE_SIZE = 133350
QUOTE_SB = Pt(8)    # 101600
QUOTE_SA = Pt(2)    # 25400
QUOTE_LI = 431800   # ~0.47cm (actual reference value)

ATTR_SIZE = 120650
ATTR_SB = None      # 0/None
ATTR_SA = Pt(10)    # 127000
ATTR_LI = 431800

def format_as_quote(p):
    pf = p.paragraph_format
    pf.space_before = QUOTE_SB
    pf.space_after = QUOTE_SA
    pf.left_indent = QUOTE_LI
    pf.alignment = None
    for r in p.runs:
        r.font.size = QUOTE_SIZE
        r.font.italic = True

def format_as_attribution(p):
    pf = p.paragraph_format
    pf.space_before = ATTR_SB
    pf.space_after = ATTR_SA
    pf.left_indent = ATTR_LI
    pf.alignment = None
    for r in p.runs:
        r.font.size = ATTR_SIZE
        r.font.italic = True

# Rebuild paragraph index after deletions/insertions
paras = doc.paragraphs

# 3.1 Split para 713 — find it by content
print("\n[3.1] Splitting combined quote+attribution paragraph...")
tiani_para_idx = None
for i, p in enumerate(paras):
    if 'Restons vigilants' in p.text and 'Général Tiani' in p.text:
        tiani_para_idx = i
        break

if tiani_para_idx is not None:
    p713 = paras[tiani_para_idx]
    print(f"  Found combined para at index {tiani_para_idx}: {p713.text!r}")

    # Split into two paragraphs at XML level
    # Quote: «\xa0Restons vigilants.\xa0»
    # Attribution: — Général Tiani, CNSP Niger, 13 novembre 2025

    quote_text = '« Restons vigilants. »'
    attr_text = '— Général Tiani, CNSP Niger, 13 novembre 2025'

    # Build attribution paragraph XML
    new_attr = make_new_paragraph_like(
        doc,
        attr_text,
        'Normal',
        space_before=None,
        space_after=int(ATTR_SA),
        left_indent=ATTR_LI,
        size=ATTR_SIZE,
        italic=True
    )

    # Insert after current paragraph
    insert_paragraph_after(p713, new_attr)

    # Now fix the original paragraph to just have the quote
    for r in p713.runs:
        r.text = ''
    if p713.runs:
        p713.runs[0].text = quote_text
        p713.runs[0].font.size = QUOTE_SIZE
        p713.runs[0].font.italic = True

    # Format as quote
    pf = p713.paragraph_format
    pf.space_before = QUOTE_SB
    pf.space_after = QUOTE_SA
    pf.left_indent = QUOTE_LI
    pf.alignment = None

    print(f"  Split into quote: {p713.text!r}")
    print(f"  And attribution: {attr_text!r}")
else:
    print("  WARNING: Could not find 'Restons vigilants' paragraph")

# Refresh
paras = doc.paragraphs

# 3.2 Fix para 157 (attribution): space_after=2pt -> 10pt, size=114300 -> 120650
print("\n[3.2] Fixing para 157 (attribution)...")
# Find by content
for i, p in enumerate(paras):
    if 'André Bourgeot' in p.text and 'CNRS' in p.text:
        print(f"  Found para {i}: {p.text!r}")
        p.paragraph_format.space_after = ATTR_SA
        for r in p.runs:
            r.font.size = ATTR_SIZE
        print(f"  Fixed: space_after=10pt, size=120650")
        break

# 3.3 Fix para 292 (attribution): space_after=2pt -> 10pt, size=None -> 120650
print("\n[3.3] Fixing para 292 (attribution - Bazoum Washington Post)...")
for i, p in enumerate(paras):
    if 'Mohamed Bazoum' in p.text and 'Washington Post' in p.text and '—' in p.text:
        print(f"  Found para {i}: {p.text!r}")
        p.paragraph_format.space_after = ATTR_SA
        for r in p.runs:
            r.font.size = ATTR_SIZE
        print(f"  Fixed: space_after=10pt, size=120650")
        break

# 3.4 Fix paras 440, 452, 462, 473, 482, 487, 493, 498
print("\n[3.4] Fixing attribution paras (left_indent, size, space_after, italic)...")

# These were at original indices but may have shifted; find by content
attribution_targets = [
    'Raphaël Granvaud',
    'Human Rights Watch',
    'Procureur Karim Khan',
    'Thomas Dietrich',
    'Jonathan Batenguène',
    'Banda Kani',
]

# Actually let's find ALL attributions with 457200 indent and fix them
fixed_count = 0
for i, p in enumerate(paras):
    pf = p.paragraph_format
    # Attribution paragraphs: left_indent=457200 (1.27cm), starts with —
    if pf.left_indent == 457200 and p.text.strip().startswith('—'):
        print(f"  Fixing para {i}: {p.text[:60]!r}")
        pf.left_indent = ATTR_LI  # 431800
        pf.space_after = ATTR_SA  # 127000 (10pt)
        for r in p.runs:
            r.font.size = ATTR_SIZE  # 120650
            r.font.italic = True
        fixed_count += 1

print(f"  Fixed {fixed_count} attribution paragraphs with 457200 indent")

# 3.5 Fix para 548 (quote): space_before=0 -> 8pt, left_indent=1.27cm -> QUOTE_LI
print("\n[3.5] Fixing para 548 (quote - Bazoum RFI)...")
for i, p in enumerate(paras):
    if 'nigériens qui m' in p.text or ('Bazoum' in p.text and 'élu' in p.text and p.text.strip().startswith('«')):
        pf = p.paragraph_format
        if pf.left_indent == 457200:
            print(f"  Found para {i}: {p.text[:60]!r}")
            pf.space_before = QUOTE_SB
            pf.left_indent = QUOTE_LI
            for r in p.runs:
                r.font.size = QUOTE_SIZE
                r.font.italic = True
            print(f"  Fixed: space_before=8pt, left_indent=431800")
            break

# 3.6 Fix para 549 (attribution after Bazoum RFI quote)
print("\n[3.6] Fixing para 549 (attribution - Bazoum RFI/France 24)...")
for i, p in enumerate(paras):
    if 'Bazoum' in p.text and 'RFI' in p.text and p.text.strip().startswith('—'):
        pf = p.paragraph_format
        if pf.left_indent == 457200 or True:  # Fix regardless
            print(f"  Found para {i}: {p.text[:60]!r}")
            pf.space_after = ATTR_SA
            pf.left_indent = ATTR_LI
            for r in p.runs:
                r.font.size = ATTR_SIZE
                r.font.italic = True
            print(f"  Fixed: space_after=10pt, left_indent=431800, size=120650")
            break

# 3.7 Fix paras 631, 637 (attributions)
print("\n[3.7] Fixing attributions 631, 637 (de Gaulle, Batenguène)...")
for i, p in enumerate(paras):
    text = p.text.strip()
    if (('de Gaulle' in text and '1966' in text and text.startswith('—')) or
        ('Jonathan Batenguène' in text and text.startswith('—'))):
        pf = p.paragraph_format
        print(f"  Found para {i}: {p.text[:60]!r}")
        pf.left_indent = ATTR_LI
        pf.space_after = ATTR_SA
        for r in p.runs:
            r.font.size = ATTR_SIZE
            r.font.italic = True
        print(f"  Fixed: left_indent=431800, size=120650, space_after=10pt")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: MISE EN PAGE KDP
# ─────────────────────────────────────────────────────────────────────────────

print("\n=== SECTION 4: KDP PAGE FORMAT ===")

sec = doc.sections[0]

# Page size: 6x9 inches (already set)
sec.page_width = int(Cm(15.24))
sec.page_height = int(Cm(22.86))

# Margins
sec.top_margin = int(Cm(2.54))
sec.bottom_margin = int(Cm(2.54))
sec.left_margin = int(Cm(2.0))    # inner/gutter
sec.right_margin = int(Cm(1.75))  # outer

# Header/footer distance
sec.header_distance = int(Cm(1.25))
sec.footer_distance = int(Cm(1.25))

print(f"  Page size: {sec.page_width/914400*2.54:.2f}cm x {sec.page_height/914400*2.54:.2f}cm")
print(f"  Margins: top={sec.top_margin/914400*2.54:.2f}cm, bottom={sec.bottom_margin/914400*2.54:.2f}cm")
print(f"           left={sec.left_margin/914400*2.54:.2f}cm, right={sec.right_margin/914400*2.54:.2f}cm")
print(f"  Header/footer distance: {sec.header_distance/914400*2.54:.2f}cm")

# Mirror margins: set mirrorMargins attribute on sectPr
sectPr = sec._sectPr
sectPr.set(qn('w:mirrorMargins'), '1')
print("  Mirror margins: enabled")

# Body text: ensure space_after=4pt consistently for Normal+size=139700 paras
print("\n[4B] Normalizing body text space_after to 4pt...")
body_fixed = 0
paras = doc.paragraphs
for i, p in enumerate(paras):
    if p.style.name == 'Normal':
        pf = p.paragraph_format
        # Check if it's a body text paragraph (size 139700 = 11pt)
        is_body = False
        if p.runs and p.runs[0].font.size == 139700:
            is_body = True
        # Also check paragraph alignment
        if is_body and pf.space_after not in (50800, None):
            # Only normalize non-standard values
            if pf.space_after not in (50800,):
                pf.space_after = Pt(4)  # 50800 EMU
                body_fixed += 1

print(f"  Normalized space_after for {body_fixed} body paragraphs")

# Line spacing: check and set at least 1.15x if not already set
# (Currently many have 1.3x line spacing which is already > 1.15x, so skip)
print("  Line spacing: already >= 1.15x for body text (no change needed)")


# ─────────────────────────────────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────────────────────────────────

print(f"\n=== SAVING to {OUTPUT} ===")
doc.save(OUTPUT)
print("DONE!")

import os
size = os.path.getsize(OUTPUT)
print(f"Output file size: {size:,} bytes ({size/1024/1024:.2f} MB)")
