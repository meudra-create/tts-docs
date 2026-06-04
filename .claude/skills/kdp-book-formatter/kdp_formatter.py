#!/usr/bin/env python3
"""
KDP Book Formatter — BEN-H2O / "PEACE, WE CAN PREVENT IT" (2026)
=================================================================
Usage:
    python3 kdp_formatter.py [input.docx [output.docx]]

Applies full KDP 6×9 print-book formatting:
  • Page size & mirror margins
  • Typography (Garamond body, headings)
  • Callout-table style (dark-navy header / cream body / gold border)
  • Duplicate-title cleanup
  • Running header + page-number footer
  • Widow/orphan control
"""

import sys
from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.text import WD_ALIGN_PARAGRAPH

# ══════════════════════════════════════════════════════════════════
#  BOOK PARAMETERS  — edit here to restyle the book
# ══════════════════════════════════════════════════════════════════

# ── Colour palette ────────────────────────────────────────────────
DARK_NAVY      = "1A1A2E"   # table header fill / body text colour
CREAM_TEXT     = "E8E0D0"   # table header text
CREAM_BODY     = "F5F5F0"   # table body cell fill
GOLD_BORDER    = "C8A000"   # outer table border
GOLD_INNER     = "C8A951"   # header row top/bottom rule
HEADER_GREY    = RGBColor(0x55, 0x55, 0x55)  # running header text

# ── Page layout ───────────────────────────────────────────────────
PAGE_W          = Inches(6.0)
PAGE_H          = Inches(9.0)
MARGIN_TOP      = Inches(0.75)
MARGIN_BOTTOM   = Inches(0.75)
MARGIN_INSIDE   = Inches(0.875)   # binding / gutter side
MARGIN_OUTSIDE  = Inches(0.625)

# ── Typography ────────────────────────────────────────────────────
BODY_FONT       = "Garamond"
BODY_SIZE       = Pt(11)
BODY_AFTER      = Pt(6)
BODY_BEFORE     = Pt(0)
LINE_SPACING    = 1.15             # multiple

HEADER_FONT     = BODY_FONT
HEADER_SIZE     = Pt(8)

FOOTER_FONT     = BODY_FONT
FOOTER_SIZE     = Pt(9)

FIRST_LINE_INDENT = Inches(0.25)  # first-line indent for body paragraphs

# ── Table geometry ────────────────────────────────────────────────
TBL_WIDTH_PCT   = "5000"          # 100% of text column (pct units)
TBL_GRID_COL    = "6120"          # single column width (dxa)
TBL_BORDER_SZ   = "8"             # outer border thickness (1/8 pt)
TBL_INNER_SZ    = "4"             # header-row rule thickness
TBL_HDR_MARGIN  = "160"           # header cell top/bottom margin (dxa)
TBL_HDR_SIDE    = "360"           # header cell left/right margin (dxa)
TBL_BODY_MARGIN = "80"            # body cell top/bottom margin (dxa)
TBL_BODY_SIDE   = "200"           # body cell left/right margin (dxa)
TBL_FONT_SZ     = "19"            # half-points → ~9.5 pt
TBL_PARA_BEFORE = "20"            # body para spacing before (dxa)
TBL_PARA_AFTER  = "60"            # body para spacing after (dxa)

# ── Book metadata ─────────────────────────────────────────────────
BOOK_TITLE      = "PEACE, WE CAN PREVENT IT"
BOOK_AUTHOR     = "BEN–H2O"

# ── Style names used in the document ─────────────────────────────
HEADING_STYLES  = {"Heading 1", "Heading 2", "Heading 3", "Heading 4"}
SUPPRESS_INDENT = {"PartNumber", "ForewordHead", "BackMatterHead",
                   "ChapterTag", "SubHeading", "FirstPara", "Separator",
                   "BookQuote", "Attribution", "Epigraph", "EpigraphAttrib"}
KEEP_NEXT_WITH  = HEADING_STYLES  # keep heading + first para together


# ══════════════════════════════════════════════════════════════════
#  CALLOUT TABLE BUILDER
# ══════════════════════════════════════════════════════════════════

def make_styled_table(rows_data: list[str]):
    """
    Build a styled callout table element.

    rows_data[0]  → dark-navy header row (bold, cream text)
    rows_data[1:] → cream body rows
                    All-caps rows shorter than 80 chars become sub-headers
                    (same dark-navy style, bold, cream text).

    Returns an lxml element ready for insertion with addnext() / addprevious().
    """
    tbl = OxmlElement("w:tbl")

    # Table properties
    tblPr = OxmlElement("w:tblPr")
    _append(tblPr, "w:tblStyle",  **{qn("w:val"): "a"})
    _append(tblPr, "w:tblW",      **{qn("w:w"): TBL_WIDTH_PCT, qn("w:type"): "pct"})
    _append(tblPr, "w:tblInd",    **{qn("w:w"): "0",           qn("w:type"): "dxa"})

    tblBorders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right"):
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"),  TBL_BORDER_SZ)
        b.set(qn("w:space"), "0")
        b.set(qn("w:color"), GOLD_BORDER)
        tblBorders.append(b)
    tblPr.append(tblBorders)
    _append(tblPr, "w:tblLook", **{qn("w:val"): "0000"})
    tbl.append(tblPr)

    tblGrid = OxmlElement("w:tblGrid")
    _append(tblGrid, "w:gridCol", **{qn("w:w"): TBL_GRID_COL})
    tbl.append(tblGrid)

    for i, text in enumerate(rows_data):
        is_header    = (i == 0)
        is_subheader = (not is_header) and text.isupper() and len(text) < 80
        dark         = is_header or is_subheader
        tbl.append(_make_row(text, dark))

    return tbl


def _make_row(text: str, dark: bool):
    tr = OxmlElement("w:tr")
    tc = OxmlElement("w:tc")

    # Cell properties
    tcPr = OxmlElement("w:tcPr")
    _append(tcPr, "w:tcW", **{qn("w:w"): "0", qn("w:type"): "auto"})

    tcBorders = OxmlElement("w:tcBorders")
    if dark:
        for side in ("top", "bottom"):
            b = OxmlElement(f"w:{side}")
            b.set(qn("w:val"), "single")
            b.set(qn("w:sz"),  TBL_INNER_SZ)
            b.set(qn("w:space"), "0")
            b.set(qn("w:color"), GOLD_INNER)
            tcBorders.append(b)
        for side in ("left", "right"):
            _append(tcBorders, f"w:{side}", **{qn("w:val"): "nil"})
    else:
        for side in ("top", "left", "bottom", "right"):
            _append(tcBorders, f"w:{side}", **{qn("w:val"): "nil"})
    tcPr.append(tcBorders)

    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"),   "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"),  DARK_NAVY if dark else CREAM_BODY)
    tcPr.append(shd)

    tcMar = OxmlElement("w:tcMar")
    vm = TBL_HDR_MARGIN if dark else TBL_BODY_MARGIN
    hm = TBL_HDR_SIDE   if dark else TBL_BODY_SIDE
    for side, val in (("top", vm), ("left", hm), ("bottom", vm), ("right", hm)):
        _append(tcMar, f"w:{side}", **{qn("w:w"): val, qn("w:type"): "dxa"})
    tcPr.append(tcMar)
    tc.append(tcPr)

    # Paragraph
    p = OxmlElement("w:p")
    if not dark:
        pPr = OxmlElement("w:pPr")
        spacing = OxmlElement("w:spacing")
        spacing.set(qn("w:before"), TBL_PARA_BEFORE)
        spacing.set(qn("w:after"),  TBL_PARA_AFTER)
        pPr.append(spacing)
        p.append(pPr)

    r = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    fonts = OxmlElement("w:rFonts")
    fonts.set(qn("w:ascii"),  BODY_FONT)
    fonts.set(qn("w:hAnsi"), BODY_FONT)
    rPr.append(fonts)
    if dark:
        rPr.append(OxmlElement("w:b"))
    color = OxmlElement("w:color")
    color.set(qn("w:val"), CREAM_TEXT if dark else DARK_NAVY)
    rPr.append(color)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), TBL_FONT_SZ)
    rPr.append(sz)
    r.append(rPr)

    t = OxmlElement("w:t")
    t.text = text
    if text.startswith(" ") or text.endswith(" "):
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    r.append(t)
    p.append(r)
    tc.append(p)
    tr.append(tc)
    return tr


# ══════════════════════════════════════════════════════════════════
#  FORMATTING PASSES
# ══════════════════════════════════════════════════════════════════

def apply_page_layout(doc):
    for section in doc.sections:
        section.page_width    = PAGE_W
        section.page_height   = PAGE_H
        section.top_margin    = MARGIN_TOP
        section.bottom_margin = MARGIN_BOTTOM
        section.left_margin   = MARGIN_INSIDE
        section.right_margin  = MARGIN_OUTSIDE


def apply_mirror_margins(doc):
    settings = doc.settings.element
    if settings.find(qn("w:mirrorMargins")) is None:
        settings.insert(1, OxmlElement("w:mirrorMargins"))


def apply_normal_style(doc):
    style = doc.styles["Normal"]
    style.font.name = BODY_FONT
    style.font.size = BODY_SIZE
    pf = style.paragraph_format
    pf.space_after  = BODY_AFTER
    pf.space_before = BODY_BEFORE
    pf.line_spacing = LINE_SPACING
    pf.widow_control = True


def apply_para_fixes(doc):
    """Widow/orphan + keep-with-next on every paragraph."""
    for para in doc.paragraphs:
        pPr = _ensure(para._p, "w:pPr")
        _set_flag(pPr, "w:widowControl", "1")
        if para.style.name in KEEP_NEXT_WITH:
            _set_flag(pPr, "w:keepNext")


def apply_first_line_indent(doc):
    """
    KDP indent rule:
      • No first-line indent on the paragraph immediately after a heading
        or on any paragraph in SUPPRESS_INDENT styles.
      • 0.25" first-line indent on all other Normal paragraphs.
    """
    suppress_next = False
    for para in doc.paragraphs:
        sname = para.style.name
        if sname in HEADING_STYLES or sname in SUPPRESS_INDENT:
            suppress_next = True
            continue
        if sname == "Normal" and para.text.strip():
            para.paragraph_format.first_line_indent = (
                Pt(0) if suppress_next else FIRST_LINE_INDENT
            )
            suppress_next = False
        else:
            suppress_next = False


def add_running_header(section):
    header = section.header
    header.is_linked_to_previous = False
    for p in list(header.paragraphs):
        p._element.getparent().remove(p._element)

    para = header.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run(BOOK_TITLE)
    run.font.name  = HEADER_FONT
    run.font.size  = HEADER_SIZE
    run.font.color.rgb = HEADER_GREY

    pPr = _ensure(para._p, "w:pPr")
    pBdr = OxmlElement("w:pBdr")
    bot = OxmlElement("w:bottom")
    bot.set(qn("w:val"),   "single")
    bot.set(qn("w:sz"),    "4")
    bot.set(qn("w:space"), "1")
    bot.set(qn("w:color"), "AAAAAA")
    pBdr.append(bot)
    pPr.append(pBdr)


def add_page_number(section):
    footer = section.footer
    footer.is_linked_to_previous = False
    for p in list(footer.paragraphs):
        p._element.getparent().remove(p._element)

    para = footer.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run()
    run.font.name = FOOTER_FONT
    run.font.size = FOOTER_SIZE

    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    instr.text = " PAGE "
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run._r.extend([fld_begin, instr, fld_end])


def apply_headers_footers(doc):
    for section in doc.sections:
        add_running_header(section)
        add_page_number(section)


def remove_duplicate_subheadings(doc):
    """
    Drop any SubHeading paragraph whose text exactly matches the
    first-row header of an existing table (normalised apostrophes).
    """
    def norm(s):
        return s.replace("’", "'").replace("‘", "'").strip()

    table_headers = {norm(t.rows[0].cells[0].text) for t in doc.tables if t.rows}
    removed = 0
    for para in list(doc.paragraphs):
        if para.style.name == "SubHeading" and norm(para.text) in table_headers:
            para._element.getparent().remove(para._element)
            removed += 1
    return removed


# ══════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════

def format_book(src: str, dst: str):
    print(f"Loading  {src}")
    doc = Document(src)

    print("  → Normal style")
    apply_normal_style(doc)

    print("  → Paragraph fixes (widow/orphan, keep-with-next)")
    apply_para_fixes(doc)

    print("  → First-line indent rule")
    apply_first_line_indent(doc)

    print("  → Page layout (6×9, KDP margins)")
    apply_page_layout(doc)

    print("  → Mirror margins")
    apply_mirror_margins(doc)

    print("  → Running headers + page numbers")
    apply_headers_footers(doc)

    n = remove_duplicate_subheadings(doc)
    print(f"  → Removed {n} duplicate SubHeading(s)")

    doc.save(dst)

    # ── Smoke-test ────────────────────────────────────────────────
    chk = Document(dst)
    s   = chk.sections[0]
    print(f"\n{'─'*52}")
    print(f"  Page:     {s.page_width/914400:.2f}\" × {s.page_height/914400:.2f}\"")
    print(f"  Margins:  inside {s.left_margin/914400:.3f}\"  outside {s.right_margin/914400:.3f}\"")
    print(f"            top    {s.top_margin/914400:.3f}\"  bottom  {s.bottom_margin/914400:.3f}\"")
    print(f"  Paras:    {len(chk.paragraphs)}   Tables: {len(chk.tables)}")
    print(f"  Saved  →  {dst}")
    print(f"{'─'*52}")


# ── Helpers ───────────────────────────────────────────────────────

def _append(parent, tag, **attribs):
    el = OxmlElement(tag)
    for k, v in attribs.items():
        el.set(k, v)
    parent.append(el)
    return el


def _ensure(parent, tag):
    el = parent.find(qn(tag))
    if el is None:
        el = OxmlElement(tag)
        parent.insert(0, el)
    return el


def _set_flag(pPr, tag, val=None):
    el = pPr.find(qn(tag))
    if el is None:
        el = OxmlElement(tag)
        pPr.append(el)
    if val is not None:
        el.set(qn("w:val"), val)


if __name__ == "__main__":
    args = sys.argv[1:]
    src  = args[0] if len(args) > 0 else "/tmp/PEACE_KDP_FINAL.docx"
    dst  = args[1] if len(args) > 1 else "/tmp/PEACE_KDP_PRINT.docx"
    format_book(src, dst)
