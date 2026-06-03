#!/usr/bin/env python3
"""
KDP Print Formatter — PEACE, WE CAN PREVENT IT
Trim: 6" × 9"  |  Mirror margins  |  Garamond typography
Produces a KDP-ready DOCX for print-on-demand publication.
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

# ─── Paths ────────────────────────────────────────────────────────────────────
SRC = '/home/user/tts-docs/PEACE_WE_CAN_PREVENT_IT_EN_4.docx'
OUT = '/home/user/tts-docs/PEACE_KDP_6x9.docx'

# ─── Colours ──────────────────────────────────────────────────────────────────
NAVY  = RGBColor(0x1a, 0x1a, 0x2e)
DARK  = RGBColor(0x2c, 0x2c, 0x2c)
GREY  = RGBColor(0x66, 0x66, 0x66)
LGREY = RGBColor(0x99, 0x99, 0x99)

# ─── Fonts ────────────────────────────────────────────────────────────────────
F = 'Garamond'

# ─── Source analysis helpers ──────────────────────────────────────────────────
def txt(p):
    return p.text.strip()

def is_bold(p):
    return any(r.bold for r in p.runs)

def is_italic(p):
    return any(r.italic for r in p.runs)

def is_separator(p):
    return txt(p) == '★ ★ ★'

def is_quote(p):
    t = txt(p)
    return is_italic(p) and (t.startswith('“') or t.startswith('"'))

def is_attribution(p):
    t = txt(p)
    return t.startswith('—') or t.startswith('—')

def is_subheading(p):
    return is_italic(p) and not is_quote(p) and not is_attribution(p) and txt(p)

def is_part_bold(p):
    return is_bold(p) and txt(p).startswith('PART')

def classify_back(p):
    t = txt(p)
    bm_heads = {
        'METHODOLOGICAL NOTES & CORPUS',
        'PRIMARY OFFICIAL AES SOURCES',
        'FRENCH ADVERSARIAL SOURCES',
        'PAN-AFRICANIST AND AFRICAN SOURCES',
        'INSTITUTIONAL AND ACADEMIC SOURCES',
        'TRANSLATION GLOSSARY',
    }
    return t in bm_heads

# ─── XML helpers ──────────────────────────────────────────────────────────────
def add_field(run, field_code):
    """Insert a Word field (PAGE, NUMPAGES…) into a run."""
    r = run._r
    fc1 = OxmlElement('w:fldChar'); fc1.set(qn('w:fldCharType'), 'begin')
    ins = OxmlElement('w:instrText'); ins.text = f' {field_code} '
    fc2 = OxmlElement('w:fldChar'); fc2.set(qn('w:fldCharType'), 'end')
    r.append(fc1); r.append(ins); r.append(fc2)

def thin_bottom_border(para):
    """Add a thin bottom rule under a paragraph (for headers)."""
    pPr = para._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '4')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '999999')
    pBdr.append(bottom)
    pPr.append(pBdr)

def set_no_spacing(para):
    """Remove space before/after a paragraph."""
    pf = para.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after  = Pt(0)

# ─── Document & page setup ────────────────────────────────────────────────────
doc = Document()

# Remove default empty paragraph
for p in list(doc.paragraphs):
    p._element.getparent().remove(p._element)

section = doc.sections[0]
section.page_width       = Inches(6)
section.page_height      = Inches(9)
section.top_margin       = Inches(0.75)
section.bottom_margin    = Inches(0.75)
section.left_margin      = Inches(0.875)   # inside / gutter
section.right_margin     = Inches(0.625)   # outside

# Mirror margins
settings_el = doc.settings.element
mm = OxmlElement('w:mirrorMargins')
settings_el.append(mm)

# Different header on first page + odd/even headers
section.different_first_page_header_footer = True
section.odd_and_even_pages_header_footer   = True

# ─── Style helpers ────────────────────────────────────────────────────────────
def sty(name):
    return doc.styles[name]

def add_sty(name):
    if name in [s.name for s in doc.styles]:
        return doc.styles[name]
    return doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)

def conf_font(style, size, bold=False, italic=False, color=None, caps=False, sc=False):
    style.font.name  = F
    style.font.size  = size
    style.font.bold  = bold
    style.font.italic = italic
    if color: style.font.color.rgb = color
    if caps:  style.font.all_caps = True
    if sc:    style.font.small_caps = True

def conf_para(style, align=WD_ALIGN_PARAGRAPH.LEFT,
              sb=Pt(0), sa=Pt(0), fi=Inches(0.25),
              li=None, ri=None, ls=1.15, pbr=False):
    pf = style.paragraph_format
    pf.alignment        = align
    pf.space_before     = sb
    pf.space_after      = sa
    pf.first_line_indent = fi
    if li is not None: pf.left_indent  = li
    if ri is not None: pf.right_indent = ri
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing      = ls
    if pbr: pf.page_break_before = True

# Normal body
conf_font(sty('Normal'), Pt(11), color=DARK)
conf_para(sty('Normal'))

# Heading 1 → Part title (centred, large caps, page break before)
conf_font(sty('Heading 1'), Pt(26), bold=True, color=NAVY, caps=True)
conf_para(sty('Heading 1'), align=WD_ALIGN_PARAGRAPH.CENTER,
          sb=Pt(0), sa=Pt(14), fi=Pt(0), ls=1.0, pbr=True)

# Heading 2 → Chapter title
conf_font(sty('Heading 2'), Pt(19), bold=True, color=NAVY)
conf_para(sty('Heading 2'), align=WD_ALIGN_PARAGRAPH.CENTER,
          sb=Pt(72), sa=Pt(24), fi=Pt(0), ls=1.0, pbr=True)

# Heading 3 → Part subtitle / tag line
conf_font(sty('Heading 3'), Pt(11), italic=True, color=GREY)
conf_para(sty('Heading 3'), align=WD_ALIGN_PARAGRAPH.CENTER,
          sb=Pt(4), sa=Pt(48), fi=Pt(0), ls=1.0)

# Custom styles
BQ  = add_sty('BookQuote')
ATT = add_sty('Attribution')
SEP = add_sty('Separator')
SUB = add_sty('SubHeading')
PNM = add_sty('PartNumber')
EPI = add_sty('Epigraph')
EAT = add_sty('EpigraphAttrib')
FP  = add_sty('FirstPara')
BMH = add_sty('BackMatterHead')
BMS = add_sty('BackMatterSub')
FWH = add_sty('ForewordHead')
CHP = add_sty('ChapterTag')

conf_font(BQ,  Pt(10.5), italic=True, color=DARK)
conf_para(BQ,  li=Inches(0.4), ri=Inches(0.4), fi=Pt(0), sb=Pt(8), sa=Pt(4), ls=1.1)

conf_font(ATT, Pt(9), color=GREY)
conf_para(ATT, align=WD_ALIGN_PARAGRAPH.CENTER, fi=Pt(0), sb=Pt(2), sa=Pt(12))

conf_font(SEP, Pt(11), color=LGREY)
conf_para(SEP, align=WD_ALIGN_PARAGRAPH.CENTER, fi=Pt(0), sb=Pt(16), sa=Pt(16))

conf_font(SUB, Pt(11), italic=True, color=NAVY)
conf_para(SUB, align=WD_ALIGN_PARAGRAPH.CENTER, fi=Pt(0), sb=Pt(16), sa=Pt(8))

conf_font(PNM, Pt(12), color=LGREY, caps=True, sc=False)
conf_para(PNM, align=WD_ALIGN_PARAGRAPH.CENTER, fi=Pt(0), sb=Pt(108), sa=Pt(8), ls=1.0)

conf_font(EPI, Pt(11), italic=True, color=DARK)
conf_para(EPI, li=Inches(0.6), ri=Inches(0.2), fi=Pt(0), sb=Pt(18), sa=Pt(4), ls=1.2)

conf_font(EAT, Pt(9.5), color=GREY)
conf_para(EAT, li=Inches(0.6), fi=Pt(0), sb=Pt(2), sa=Pt(18))

conf_font(FP,  Pt(11), color=DARK)
conf_para(FP,  fi=Pt(0), sb=Pt(0), sa=Pt(0))

conf_font(BMH, Pt(13), bold=True, color=NAVY, caps=True)
conf_para(BMH, align=WD_ALIGN_PARAGRAPH.CENTER, fi=Pt(0), sb=Pt(28), sa=Pt(12), ls=1.0)

conf_font(BMS, Pt(10.5), bold=True, color=NAVY)
conf_para(BMS, fi=Pt(0), sb=Pt(12), sa=Pt(4))

conf_font(FWH, Pt(16), bold=True, color=NAVY)
conf_para(FWH, align=WD_ALIGN_PARAGRAPH.CENTER, fi=Pt(0),
          sb=Pt(48), sa=Pt(24), ls=1.0, pbr=True)

conf_font(CHP, Pt(10), italic=True, color=GREY)
conf_para(CHP, align=WD_ALIGN_PARAGRAPH.CENTER, fi=Pt(0), sb=Pt(0), sa=Pt(0))

# ─── Headers & Footers ────────────────────────────────────────────────────────
def hdr_para(container, text, align=WD_ALIGN_PARAGRAPH.CENTER, rule=False):
    p = container.paragraphs[0] if container.paragraphs else container.add_paragraph()
    p.clear()
    p.paragraph_format.alignment = align
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(4)
    r = p.add_run(text)
    r.font.name  = F
    r.font.size  = Pt(8)
    r.font.color.rgb = LGREY
    r.font.all_caps  = True
    if rule:
        thin_bottom_border(p)
    return p

def ftr_page_num(container):
    p = container.paragraphs[0] if container.paragraphs else container.add_paragraph()
    p.clear()
    p.paragraph_format.alignment    = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(0)
    r = p.add_run()
    r.font.name  = F
    r.font.size  = Pt(9)
    r.font.color.rgb = GREY
    add_field(r, 'PAGE')

# Even (verso): book title
hdr_para(section.even_page_header,
         'Peace, We Can Prevent It', rule=True)
# Odd (recto): subtitle
hdr_para(section.header,
         'Geopolitics of African Resistance', rule=True)
# Footers
ftr_page_num(section.footer)
ftr_page_num(section.even_page_footer)
# First page: no header/footer (title page)
section.first_page_header.is_linked_to_previous = False
section.first_page_footer.is_linked_to_previous = False

# ─── Low-level paragraph writers ──────────────────────────────────────────────
def p_raw(style_name, text='', bold=False, italic=False,
          align=None, color=None, size=None):
    """Add a paragraph, return it."""
    p = doc.add_paragraph(style=style_name)
    if text:
        r = p.add_run(text)
        if bold:   r.bold  = bold
        if italic: r.italic = italic
        if color:  r.font.color.rgb = color
        if size:   r.font.size = size
    if align:
        p.paragraph_format.alignment = align
    return p

def page_break():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(0)
    r = p.add_run()
    r.add_break(WD_BREAK.PAGE)

# ─── TITLE PAGE ───────────────────────────────────────────────────────────────
def build_title_page():
    # Series label
    p = doc.add_paragraph()
    p.paragraph_format.alignment    = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(60)
    p.paragraph_format.space_after  = Pt(0)
    r = p.add_run('Alliance of Sahel States')
    r.font.name = F; r.font.size = Pt(10); r.font.color.rgb = LGREY
    r.font.all_caps = True

    # Thin rule
    p_r = doc.add_paragraph()
    p_r.paragraph_format.alignment    = WD_ALIGN_PARAGRAPH.CENTER
    p_r.paragraph_format.space_before = Pt(10)
    p_r.paragraph_format.space_after  = Pt(10)
    rr = p_r.add_run('⸻⸻⸻')
    rr.font.name = F; rr.font.size = Pt(12); rr.font.color.rgb = NAVY

    # Main title line 1
    p1 = doc.add_paragraph()
    p1.paragraph_format.alignment    = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(20)
    p1.paragraph_format.space_after  = Pt(4)
    r1 = p1.add_run('PEACE,')
    r1.font.name = F; r1.font.size = Pt(38); r1.font.bold = True
    r1.font.color.rgb = NAVY

    # Main title line 2
    p2 = doc.add_paragraph()
    p2.paragraph_format.alignment    = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after  = Pt(16)
    r2 = p2.add_run('WE CAN PREVENT IT')
    r2.font.name = F; r2.font.size = Pt(38); r2.font.bold = True
    r2.font.color.rgb = NAVY

    # Subtitle
    p_s = doc.add_paragraph()
    p_s.paragraph_format.alignment    = WD_ALIGN_PARAGRAPH.CENTER
    p_s.paragraph_format.space_before = Pt(0)
    p_s.paragraph_format.space_after  = Pt(40)
    rs = p_s.add_run('Geopolitics of African Resistance')
    rs.font.name = F; rs.font.size = Pt(16); rs.font.italic = True
    rs.font.color.rgb = GREY

    # Rule
    p_r2 = doc.add_paragraph()
    p_r2.paragraph_format.alignment    = WD_ALIGN_PARAGRAPH.CENTER
    p_r2.paragraph_format.space_before = Pt(0)
    p_r2.paragraph_format.space_after  = Pt(40)
    rr2 = p_r2.add_run('⸻⸻⸻')
    rr2.font.name = F; rr2.font.size = Pt(12); rr2.font.color.rgb = NAVY

    # Author
    p_a = doc.add_paragraph()
    p_a.paragraph_format.alignment    = WD_ALIGN_PARAGRAPH.CENTER
    p_a.paragraph_format.space_before = Pt(0)
    p_a.paragraph_format.space_after  = Pt(6)
    ra = p_a.add_run('BEN–H2O')
    ra.font.name = F; ra.font.size = Pt(14); ra.font.color.rgb = DARK

    p_y = doc.add_paragraph()
    p_y.paragraph_format.alignment    = WD_ALIGN_PARAGRAPH.CENTER
    p_y.paragraph_format.space_before = Pt(0)
    p_y.paragraph_format.space_after  = Pt(0)
    ry = p_y.add_run('2026')
    ry.font.name = F; ry.font.size = Pt(11); ry.font.color.rgb = LGREY

build_title_page()

# ─── COPYRIGHT PAGE ───────────────────────────────────────────────────────────
page_break()

def build_copyright_page():
    # Verso page — copyright notice
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(300)  # push to bottom of page
    p.paragraph_format.space_after  = Pt(0)
    p.paragraph_format.alignment    = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run('© 2026 BEN–H2O. All rights reserved.')
    r.font.name = F; r.font.size = Pt(9); r.font.color.rgb = GREY

    p2 = doc.add_paragraph()
    p2.paragraph_format.space_before = Pt(6); p2.paragraph_format.space_after = Pt(0)
    r2 = p2.add_run(
        'No part of this publication may be reproduced, stored in a retrieval system, '
        'or transmitted in any form or by any means, electronic, mechanical, photocopying, '
        'recording, or otherwise, without the prior written permission of the author.'
    )
    r2.font.name = F; r2.font.size = Pt(9); r2.font.color.rgb = GREY

    p3 = doc.add_paragraph()
    p3.paragraph_format.space_before = Pt(12); p3.paragraph_format.space_after = Pt(0)
    r3 = p3.add_run('First edition — 2026')
    r3.font.name = F; r3.font.size = Pt(9); r3.font.color.rgb = GREY

    p4 = doc.add_paragraph()
    p4.paragraph_format.space_before = Pt(6); p4.paragraph_format.space_after = Pt(0)
    r4 = p4.add_run('Printed and distributed via Kindle Direct Publishing (KDP)')
    r4.font.name = F; r4.font.size = Pt(9); r4.font.color.rgb = GREY

build_copyright_page()

# ─── EPIGRAPH PAGE ────────────────────────────────────────────────────────────
page_break()

src_doc = Document(SRC)
paras   = src_doc.paragraphs

# Epigraphs are at indices 7-18 in source
def build_epigraph_page():
    # Top spacer
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(60)
    p_sp.paragraph_format.space_after  = Pt(0)
    r_sp = p_sp.add_run('')
    r_sp.font.size = Pt(11)

    for i in range(7, 19):
        p = paras[i]
        t = txt(p)
        if not t:
            continue
        # Attribution lines start with —
        if is_attribution(p):
            pp = doc.add_paragraph(style='EpigraphAttrib')
            pp.runs[0].text if pp.runs else pp.add_run(t)
            if not pp.runs:
                pp.add_run(t)
            else:
                pp.runs[0].text = t
        else:
            pp = doc.add_paragraph(style='Epigraph')
            if not pp.runs:
                pp.add_run(t)
            else:
                pp.runs[0].text = t

build_epigraph_page()

# ─── FOREWORD ─────────────────────────────────────────────────────────────────
page_break()

def build_foreword():
    # Title
    p_fw = doc.add_paragraph(style='ForewordHead')
    r_fw = p_fw.add_run('FOREWORD')
    r_fw.font.name = F; r_fw.font.size = Pt(16); r_fw.font.bold = True
    r_fw.font.color.rgb = NAVY

    p_fwsub = doc.add_paragraph(style='ChapterTag')
    r_fwsub = p_fwsub.add_run('Method and Analytical Rigour')
    r_fwsub.font.name = F; r_fwsub.font.size = Pt(10); r_fwsub.font.italic = True
    r_fwsub.font.color.rgb = GREY

    # Foreword body: paragraphs 21-26 in source
    first = True
    for i in range(21, 28):
        p = paras[i]
        t = txt(p)
        if not t or t == '.':
            continue
        if is_separator(p):
            pp = doc.add_paragraph(style='Separator'); pp.add_run(t)
            first = True
            continue
        if is_attribution(p):
            pp = doc.add_paragraph(style='Attribution'); pp.add_run(t)
            continue
        if is_quote(p):
            pp = doc.add_paragraph(style='BookQuote'); pp.add_run(t)
            continue
        style = 'FirstPara' if first else 'Normal'
        pp = doc.add_paragraph(style=style); pp.add_run(t)
        first = False

build_foreword()

# ─── MAIN CONTENT PROCESSOR ───────────────────────────────────────────────────
# Sequence of source paragraph ranges to process:
#   [159–175]  Prologue + Introduction
#   [177–389]  Part I through Ch 25 (end of body before Ch 25b)
#   [73–135]   Chapter 25b (inserted in TOC area in source)
#   [390–509]  Ch 26 through Epilogue
#   [510–560]  Back matter

SEQUENCES = [
    range(159, 176),
    range(177, 390),
    range(73,  136),
    range(390, 510),
    range(510, 561),
]

def classify_and_add(p, first_after_heading):
    """
    Classify a source paragraph and add it to the target doc.
    Returns new value of first_after_heading.
    """
    t = txt(p)
    style = p.style.name

    if not t:
        return first_after_heading

    # ── Structural headings ──────────────────────────────────────────────────
    if style == 'Heading 1':
        # Part title — always has a companion PartNumber above it
        pp = doc.add_paragraph(style='Heading 1')
        pp.add_run(t)
        return True

    if style == 'Heading 2':
        # Chapter title
        pp = doc.add_paragraph(style='Heading 2')
        pp.add_run(t)
        return True

    if style == 'Heading 3':
        pp = doc.add_paragraph(style='Heading 3')
        pp.add_run(t)
        return first_after_heading

    # ── Part number label (Normal bold, starts with PART) ────────────────────
    if is_part_bold(p):
        pp = doc.add_paragraph(style='PartNumber')
        pp.add_run(t)
        return first_after_heading

    # ── Epilogue / back-matter section heads (Normal bold) ───────────────────
    if is_bold(p) and t in ('EPILOGUE',):
        pp = doc.add_paragraph(style='Heading 1')
        pp.add_run(t)
        return True

    if is_bold(p) and t.startswith('Chapter'):
        pp = doc.add_paragraph(style='Heading 2')
        pp.add_run(t)
        return True

    if classify_back(p):
        pp = doc.add_paragraph(style='BackMatterHead')
        pp.add_run(t)
        return True

    if is_bold(p) and t not in ('',):
        # bold sub-sections in back matter
        pp = doc.add_paragraph(style='BackMatterSub')
        pp.add_run(t)
        return False

    # ── Separator ─────────────────────────────────────────────────────────────
    if is_separator(p):
        pp = doc.add_paragraph(style='Separator')
        pp.add_run(t)
        return False

    # ── Block quote ───────────────────────────────────────────────────────────
    if is_quote(p):
        pp = doc.add_paragraph(style='BookQuote')
        pp.add_run(t)
        return False

    # ── Attribution line ──────────────────────────────────────────────────────
    if is_attribution(p):
        pp = doc.add_paragraph(style='Attribution')
        pp.add_run(t)
        return False

    # ── Sub-heading (italic, not quote) ──────────────────────────────────────
    if is_subheading(p):
        pp = doc.add_paragraph(style='SubHeading')
        pp.add_run(t)
        return False

    # ── Body text ─────────────────────────────────────────────────────────────
    style_name = 'FirstPara' if first_after_heading else 'Normal'
    pp = doc.add_paragraph(style=style_name)
    pp.add_run(t)
    return False

# ─── Chapter 25b heading is at index 73 in source ───────────────────────────
# Prologue / Introduction special headings
PROLOGUE_IDX = 159
INTRO_IDX    = 168

def add_section_head(title, subtitle=None):
    """Add a non-chapter section head (Prologue, Introduction, Epilogue)."""
    pp = doc.add_paragraph(style='Heading 2')
    pp.add_run(title)
    if subtitle:
        ps = doc.add_paragraph(style='ChapterTag')
        ps.add_run(subtitle)

# ─── Process all content ──────────────────────────────────────────────────────
first_after_heading = True

for seq in SEQUENCES:
    for i in seq:
        p = paras[i]
        t = txt(p)
        s = p.style.name

        # Skip TOC listing lines (indented chapter listings, not actual content)
        # These are in range 29-72 and 136-157 which we skip entirely.
        # The SEQUENCES above already skip those ranges.

        # Special handling for Prologue / Introduction text headings
        if i == PROLOGUE_IDX and t == 'PROLOGUE — The Villa in Niamey':
            add_section_head('PROLOGUE', 'The Villa in Niamey')
            first_after_heading = True
            continue

        if i == INTRO_IDX and t == 'INTRODUCTION — Why the AES Changes Everything':
            add_section_head('INTRODUCTION', 'Why the AES Changes Everything')
            first_after_heading = True
            continue

        first_after_heading = classify_and_add(p, first_after_heading)

# ─── Save ─────────────────────────────────────────────────────────────────────
doc.save(OUT)
print(f'✓ Saved → {OUT}')
print(f'  Paragraphs in output: {len(doc.paragraphs)}')
