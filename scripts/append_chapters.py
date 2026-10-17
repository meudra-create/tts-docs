#!/usr/bin/env python3
import os, re, glob
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ─── Colors ─────────────────────────────────────────────────────────────────
ARDOISE      = "2C3A4A"
ARDOISE_RGB  = RGBColor(0x2C, 0x3A, 0x4A)
GOLD_HEX     = "A07820"
GOLD_RGB     = RGBColor(0xA0, 0x78, 0x20)
DARK_RED_RGB = RGBColor(0x8B, 0x1A, 0x1A)
WHITE_RGB    = RGBColor(0xFF, 0xFF, 0xFF)
CREAM_HEX    = "F4EFE4"
GRIS_RGB     = RGBColor(0x3C, 0x3C, 0x3C)
FONT_NAME    = "FreeSerif"
BORDER_SZ    = "7"   # 0.90 pt = 7 × 1/8 pt

# ─── XML helpers ─────────────────────────────────────────────────────────────
def set_cell_fill(cell, fill_hex):
    tc = cell._tc
    tcPr = tc.find(qn('w:tcPr'))
    if tcPr is None:
        tcPr = OxmlElement('w:tcPr'); tc.insert(0, tcPr)
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    ex = tcPr.find(qn('w:shd'))
    if ex is not None: tcPr.remove(ex)
    tcPr.append(shd)

def set_para_shading(para, fill_hex):
    """Full-width background color on a paragraph."""
    pPr = para._p.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr'); para._p.insert(0, pPr)
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    ex = pPr.find(qn('w:shd'))
    if ex is not None: pPr.remove(ex)
    pPr.append(shd)

def set_para_border(para, side, color_hex, sz=BORDER_SZ, space="4"):
    """Add a border to one side of a paragraph (e.g. bottom = filet or)."""
    pPr = para._p.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr'); para._p.insert(0, pPr)
    pBdr = pPr.find(qn('w:pBdr'))
    if pBdr is None:
        pBdr = OxmlElement('w:pBdr'); pPr.append(pBdr)
    el = OxmlElement(f'w:{side}')
    el.set(qn('w:val'), 'single')
    el.set(qn('w:sz'), sz)
    el.set(qn('w:space'), space)
    el.set(qn('w:color'), color_hex)
    ex = pBdr.find(qn(f'w:{side}'))
    if ex is not None: pBdr.remove(ex)
    pBdr.append(el)

def set_table_borders(table, sz=BORDER_SZ, color=ARDOISE):
    tbl = table._tbl
    tblPr = tbl.find(qn('w:tblPr'))
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr'); tbl.insert(0, tblPr)
    tblBorders = OxmlElement('w:tblBorders')
    for side in ('top','left','bottom','right','insideH','insideV'):
        b = OxmlElement(f'w:{side}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), sz)
        b.set(qn('w:space'), '0')
        b.set(qn('w:color'), color)
        tblBorders.append(b)
    ex = tblPr.find(qn('w:tblBorders'))
    if ex is not None: tblPr.remove(ex)
    tblPr.append(tblBorders)

def styled_run(para, text, color=None, bold=False, italic=False, size=None, caps=False):
    run = para.add_run(text)
    run.font.name = FONT_NAME
    if color: run.font.color.rgb = color
    if bold:  run.bold = True
    if italic: run.italic = True
    if size:  run.font.size = Pt(size)
    if caps:  run.font.all_caps = True
    return run

# ─── Document elements ───────────────────────────────────────────────────────
def add_page_break(doc):
    p = doc.add_paragraph()
    run = p.add_run()
    br = OxmlElement('w:br')
    br.set(qn('w:type'), 'page')
    run._r.append(br)

def add_heading1(doc, text):
    """Bandeau plein ardoise + titre blanc capitales + filet or en bas."""
    para = doc.add_paragraph(style='Normal')
    para.paragraph_format.space_before = Pt(6)
    para.paragraph_format.space_after  = Pt(2)
    # Full ardoise background
    set_para_shading(para, ARDOISE)
    # Gold bottom border (filet or)
    set_para_border(para, 'bottom', GOLD_HEX, sz="12", space="4")  # 1.5 pt gold filet
    # Padding via indent
    para.paragraph_format.left_indent  = Cm(0.3)
    para.paragraph_format.right_indent = Cm(0.3)
    styled_run(para, text, color=WHITE_RGB, bold=True, size=13, caps=True)
    return para

def add_heading2(doc, text):
    """Texte ardoise + filet or en bas."""
    para = doc.add_paragraph(style='Normal')
    para.paragraph_format.space_before = Pt(10)
    para.paragraph_format.space_after  = Pt(3)
    # Gold bottom border
    set_para_border(para, 'bottom', GOLD_HEX, sz=BORDER_SZ, space="3")
    styled_run(para, text, color=ARDOISE_RGB, bold=True, size=11.5)
    return para

def add_heading3(doc, text):
    para = doc.add_paragraph(style='Normal')
    para.paragraph_format.space_before = Pt(6)
    styled_run(para, text, color=ARDOISE_RGB, bold=True, size=11)
    return para

def add_separator(doc):
    para = doc.add_paragraph()
    para.alignment = 1
    para.paragraph_format.space_before = Pt(6)
    para.paragraph_format.space_after  = Pt(6)
    styled_run(para, '★★★', color=GOLD_RGB, size=14)

def add_quote(doc, text):
    clean = re.sub(r'^> ?', '', text, flags=re.MULTILINE).strip()
    if not clean: return
    para = doc.add_paragraph(style='Normal')
    para.paragraph_format.left_indent  = Cm(1.2)
    para.paragraph_format.right_indent = Cm(1.2)
    para.paragraph_format.space_before = Pt(4)
    para.paragraph_format.space_after  = Pt(4)
    styled_run(para, clean, color=DARK_RED_RGB, italic=True, size=10.5)

def add_normal(doc, text):
    para = doc.add_paragraph(style='Normal')
    para.paragraph_format.space_after = Pt(4)
    styled_run(para, text, size=11)
    return para

def add_bullet(doc, text):
    para = doc.add_paragraph(style='List Bullet')
    styled_run(para, text, size=10.5)
    return para

def add_styled_table(doc, title, rows):
    """Encadré : en-tête ardoise blanc + corps crème gris + bordures 0,90 pt."""
    table = doc.add_table(rows=1 + len(rows), cols=1)
    set_table_borders(table, BORDER_SZ, ARDOISE)
    # Header
    hc = table.rows[0].cells[0]
    set_cell_fill(hc, ARDOISE)
    hc.paragraphs[0].paragraph_format.left_indent = Cm(0.2)
    styled_run(hc.paragraphs[0], title, color=WHITE_RGB, bold=True, size=10, caps=True)
    # Body
    for i, row_text in enumerate(rows):
        cell = table.rows[i + 1].cells[0]
        set_cell_fill(cell, CREAM_HEX)
        cell.paragraphs[0].paragraph_format.left_indent = Cm(0.2)
        styled_run(cell.paragraphs[0], row_text, color=GRIS_RGB, size=9.5)
    doc.add_paragraph()

# ─── Markdown parser ──────────────────────────────────────────────────────────
def parse_and_append(doc, md_text):
    lines = md_text.split('\n')
    i = 0
    quote_buf = []

    def flush_quote():
        if quote_buf:
            add_quote(doc, '\n'.join(quote_buf).strip())
            quote_buf.clear()

    while i < len(lines):
        line = lines[i]

        if not line.strip() or line.strip() == r'\newpage':
            flush_quote(); i += 1; continue

        if line.startswith('# '):
            flush_quote(); add_heading1(doc, line[2:].strip()); i += 1; continue
        if line.startswith('## '):
            flush_quote(); add_heading2(doc, line[3:].strip()); i += 1; continue
        if line.startswith('### '):
            flush_quote(); add_heading3(doc, line[4:].strip()); i += 1; continue

        if re.match(r'^---+$', line.strip()):
            flush_quote(); i += 1; continue
        if line.strip() == '★★★':
            flush_quote(); add_separator(doc); i += 1; continue

        if line.startswith('>'):
            quote_buf.append(re.sub(r'^> ?', '', line)); i += 1; continue

        if re.match(r'^[-*] ', line):
            flush_quote(); add_bullet(doc, line[2:].strip()); i += 1; continue
        if re.match(r'^\d+\. ', line):
            flush_quote(); add_bullet(doc, re.sub(r'^\d+\. ', '', line)); i += 1; continue

        # Bold-only line → possible encadré title
        bm = re.match(r'^\*\*(.+?)\*\*\s*$', line.strip())
        if bm:
            flush_quote()
            title = bm.group(1)
            rows = []; j = i + 1
            while j < len(lines) and j < i + 30:
                nl = lines[j].strip()
                if not nl: j += 1; break
                if re.match(r'^[-*\d]', nl):
                    content = re.sub(r'^[-*]\s+|^\d+\.\s+', '', nl)
                    content = re.sub(r'\*\*(.+?)\*\*', r'\1', content)
                    content = re.sub(r'\*(.+?)\*', r'\1', content)
                    rows.append(content); j += 1
                else: break
            if rows:
                add_styled_table(doc, title, rows); i = j
            else:
                p = doc.add_paragraph(style='Normal')
                styled_run(p, title, color=ARDOISE_RGB, bold=True, size=11)
                i += 1
            continue

        flush_quote()
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', line.strip())
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        text = re.sub(r'`(.+?)`', r'\1', text)
        if text: add_normal(doc, text)
        i += 1

    flush_quote()

# ─── Main ─────────────────────────────────────────────────────────────────────
print("Opening LIVREFINAL_13.docx...")
doc = Document('/root/.claude/uploads/e3ecab87-9343-5812-ac40-80d3b0b7d656/193fadd5-LIVREFINAL_13.docx')

chapter_dir = '/home/user/tts-docs/content/3.livre/'
supp_files = sorted(
    [f for f in glob.glob(os.path.join(chapter_dir, '[0-9]*.md'))
     if int(os.path.basename(f).split('.')[0]) >= 40],
    key=lambda x: int(os.path.basename(x).split('.')[0])
)

print(f"Appending {len(supp_files)} chapters — FreeSerif, H1 ardoise/blanc/filet-or, H2 ardoise/filet-or, bordures 0,90 pt...")
for filepath in supp_files:
    num = int(os.path.basename(filepath).split('.')[0])
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3: content = parts[2].strip()
    add_page_break(doc)
    parse_and_append(doc, content)
    print(f"  ✓ {num}: {os.path.basename(filepath)[:55]}")

out = '/home/user/tts-docs/la-paix-on-peut-leviter.docx'
doc.save(out)
print(f"\nSaved: {out}  ({os.path.getsize(out)/1024:.1f} KB)")
