import docx, re, os
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ══════════════════════════════════════════
#  THÈME 03 — SAHEL ROUGE  ×  FORMAT KDP
#  Trim: 6 × 9 in  ·  Marges KDP  ·  ★ ★ ★
# ══════════════════════════════════════════

# Palette Sahel Rouge
ROUGE    = RGBColor(0x8B, 0x1A, 0x1A)
OR       = RGBColor(0xD4, 0xA0, 0x17)
BORDEAUX = RGBColor(0x5A, 0x10, 0x10)
NOIR     = RGBColor(0x0A, 0x0A, 0x0A)
IVOIRE   = RGBColor(0xF5, 0xF0, 0xE8)
GRISRG   = RGBColor(0x6A, 0x40, 0x40)
FONT     = 'FreeSans'

doc = docx.Document()

# ── KDP 6×9″ paperback margins ────────────────────────────
# For 151–300 pages: inside (gutter) ≥ 0.75″, outside ≥ 0.25″
# We use comfortable reading margins:
#   Inside (gutter): 0.80″  ·  Outside: 0.60″
#   Top: 0.75″  ·  Bottom: 0.70″
sec = doc.sections[0]
sec.page_width    = Inches(6)
sec.page_height   = Inches(9)
sec.left_margin   = Inches(0.80)   # gutter (inside)
sec.right_margin  = Inches(0.60)   # outside
sec.top_margin    = Inches(0.75)
sec.bottom_margin = Inches(0.70)
sec.gutter        = Inches(0)      # already accounted for in left_margin
sec.orientation   = WD_ORIENT.PORTRAIT

# ── Styles ─────────────────────────────────────────────────
n = doc.styles['Normal']
n.font.name = FONT; n.font.size = Pt(10.5); n.font.color.rgb = NOIR
n.paragraph_format.space_after   = Pt(6)
n.paragraph_format.space_before  = Pt(0)
n.paragraph_format.line_spacing  = 1.35
n.paragraph_format.alignment     = WD_ALIGN_PARAGRAPH.JUSTIFY
n.paragraph_format.widow_control = True

def force_font(style, fontname):
    rpr = style.element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts'); rpr.append(rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:cs'):
        rf.set(qn(a), fontname)

def set_heading(name, size, color, caps=False, space_before=12, space_after=6):
    s = doc.styles[name]
    s.font.name  = FONT
    s.font.size  = Pt(size)
    s.font.color.rgb = color
    s.font.bold  = True
    s.font.all_caps = caps
    s.paragraph_format.space_before  = Pt(space_before)
    s.paragraph_format.space_after   = Pt(space_after)
    s.paragraph_format.keep_with_next = True
    s.paragraph_format.widow_control  = True
    force_font(s, FONT)

set_heading('Heading 1', 18, ROUGE, space_before=18, space_after=8)
set_heading('Heading 2', 13, ROUGE, space_before=14, space_after=6)
set_heading('Heading 3', 11, BORDEAUX, space_before=10, space_after=4)
force_font(n, FONT)

def force_font_run(r):
    rpr = r._r.get_or_add_rPr()
    rf  = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts'); rpr.append(rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:cs'):
        rf.set(qn(a), FONT)

# ── Helpers ────────────────────────────────────────────────
def bottom_border(p, color="D4A017", sz="18"):
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr')
    b = OxmlElement('w:bottom')
    b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), sz)
    b.set(qn('w:space'), '4');    b.set(qn('w:color'), color)
    pbdr.append(b); pPr.append(pbdr)

def top_border(p, color="D4A017", sz="18"):
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr')
    b = OxmlElement('w:top')
    b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), sz)
    b.set(qn('w:space'), '4');    b.set(qn('w:color'), color)
    pbdr.append(b); pPr.append(pbdr)

def center(text, size=None, bold=False, italic=False, color=None, space_before=0, space_after=0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if space_before: p.paragraph_format.space_before = Pt(space_before)
    if space_after:  p.paragraph_format.space_after  = Pt(space_after)
    r = p.add_run(text)
    if size:  r.font.size = Pt(size)
    r.bold = bold; r.italic = italic
    if color: r.font.color.rgb = color
    force_font_run(r)
    return p

def ornament():
    """★ ★ ★ — or de résistance, centré, espacement contrôlé"""
    p = center("★  ★  ★", size=11, color=OR, space_before=8, space_after=8)
    return p

def quote(text):
    is_attrib = text.lstrip().startswith("—")
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.italic = True
    if is_attrib:
        r.font.size = Pt(9); r.font.color.rgb = GRISRG
    else:
        r.font.size = Pt(10); r.font.color.rgb = ROUGE
    p.paragraph_format.left_indent  = Cm(1.0)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(6)
    pPr  = p._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr')
    lft  = OxmlElement('w:left')
    lft.set(qn('w:val'), 'single'); lft.set(qn('w:sz'), '18')
    lft.set(qn('w:space'), '8');    lft.set(qn('w:color'), 'D4A017')
    pbdr.append(lft); pPr.append(pbdr)
    return p

def shade(cell, hexfill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd  = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:fill'), hexfill)
    tcPr.append(shd)

def inline(p, s):
    for seg in re.split(r'(\*\*.+?\*\*|\*.+?\*)', s):
        if not seg: continue
        if seg.startswith("**") and seg.endswith("**"):
            r = p.add_run(seg[2:-2]); r.bold = True
        elif seg.startswith("*") and seg.endswith("*"):
            r = p.add_run(seg[1:-1]); r.italic = True
        else:
            p.add_run(seg)

# ── Parse Markdown ─────────────────────────────────────────
lines = open("LIVRE-FINAL.md").read().split("\n")
first_h1_seen = False
i = 0

while i < len(lines):
    s = lines[i].strip()

    # ── Marqueurs structurels (ne pas imprimer) ────────────
    if re.match(r'^---(ENCADRE|FIN)---$', s) or re.fullmatch(r'-{3,}', s):
        i += 1; continue

    # ── Encadrés ───────────────────────────────────────────
    m_box = re.match(r'^\*\*(.+)\*\*$', s)
    if m_box and i+1 < len(lines):
        j = i + 1
        while j < len(lines) and not lines[j].strip(): j += 1
        bullets = []; k = j
        while k < len(lines) and (re.match(r'^\s*[-*] ', lines[k]) or re.match(r'^\s*\d+\.\s', lines[k])):
            cleaned = re.sub(r'^\s*[-*] ', '', lines[k].strip())
            cleaned = re.sub(r'^\s*\d+\.\s*', '', cleaned)
            bullets.append(cleaned); k += 1
        if len(bullets) >= 1:
            tbl = doc.add_table(rows=1+len(bullets), cols=1)
            tbl.style = 'Table Grid'
            hd = tbl.rows[0].cells[0]; shade(hd, '8B1A1A')
            ph = hd.paragraphs[0]
            rh = ph.add_run(m_box.group(1).upper())
            rh.bold = True; rh.font.size = Pt(9)
            rh.font.color.rgb = IVOIRE; rh.font.name = FONT
            for bi, btxt in enumerate(bullets):
                c  = tbl.rows[1+bi].cells[0]; shade(c, 'FFF0EE')
                pc = c.paragraphs[0]
                rc = pc.add_run(re.sub(r'\*\*(.+?)\*\*', r'\1', btxt))
                rc.font.size = Pt(9); rc.font.color.rgb = NOIR; rc.font.name = FONT
            doc.add_paragraph()
            i = k; continue

    # ── Ornements ★ ★ ★ ──────────────────────────────────
    if s.replace(" ", "") == "★★★":
        ornament(); i += 1; continue

    if not s: i += 1; continue

    # ── Titres ─────────────────────────────────────────────
    if s.startswith("# "):
        title = s[2:].strip()
        if first_h1_seen:
            doc.add_page_break()
        first_h1_seen = True

        if title.startswith("PARTIE"):
            # Page de partie : 2 filets or, titre rouge capitales, centré
            for _ in range(5): doc.add_paragraph()
            sep1 = doc.add_paragraph()
            bottom_border(sep1, color="D4A017", sz="24")
            p = center(title, size=18, bold=True, color=ROUGE,
                       space_before=16, space_after=16)
            sep2 = doc.add_paragraph()
            top_border(sep2, color="D4A017", sz="24")
        elif title == "Sommaire":
            h = doc.add_heading(title, level=1)
            bottom_border(h, color="D4A017", sz="14")
        else:
            h = doc.add_heading(title, level=1)
            bottom_border(h, color="D4A017", sz="18")
        i += 1; continue

    if s.startswith("## "):
        doc.add_heading(s[3:].strip(), level=2)
        i += 1; continue

    if s.startswith("### "):
        doc.add_heading(s[4:].strip(), level=3)
        i += 1; continue

    # ── Citations ──────────────────────────────────────────
    if s.startswith(">"):
        quote(s.lstrip("> ").strip()); i += 1; continue

    # ── Listes ─────────────────────────────────────────────
    if s.startswith("- ") or s.startswith("* "):
        p = doc.add_paragraph(style='List Bullet')
        inline(p, re.sub(r'\*\*(.+?)\*\*', r'\1', s[2:].strip()))
        i += 1; continue

    if re.match(r'^\d+\.\s', s):
        doc.add_paragraph(
            re.sub(r'\*\*(.+?)\*\*', r'\1', re.sub(r'^\d+\.\s', '', s)),
            style='List Number')
        i += 1; continue

    # ── Tableaux Markdown ──────────────────────────────────
    if s.startswith("|"):
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not all(set(c) <= set("-: ") for c in cells):
            doc.add_paragraph("  •  ".join(c for c in cells if c))
        i += 1; continue

    # ── Citations italiques seules ─────────────────────────
    m = re.match(r'^\*(.+)\*$', s)
    if m and ("—" in s or "«" in s):
        quote(m.group(1)); i += 1; continue

    # ── Page de titre (avant premier H1) ───────────────────
    if not first_h1_seen:
        if s.startswith("LA PAIX"):
            for _ in range(4): doc.add_paragraph()
            center(s, size=28, bold=True, color=ROUGE, space_after=4)
        elif s.startswith("Enquête"):
            center(s, size=12, italic=True, color=OR, space_before=8, space_after=8)
        elif s.startswith("BEN"):
            center(s, size=11, bold=True, color=NOIR, space_before=20)
        elif s.startswith("— 2026"):
            center(s, size=10, color=GRISRG, space_before=4, space_after=16)
        elif s == "★ ★ ★":
            ornament()
        elif s.startswith("©"):
            center(s, size=8, color=GRISRG, space_before=30, space_after=6)
        elif s.startswith("«"):
            center(s, size=9, italic=True, color=GRISRG, space_before=4, space_after=2)
        elif s.startswith("—") and not s.startswith("— 2026"):
            center(s, size=8.5, italic=True, color=GRISRG, space_before=0, space_after=8)
        else:
            center(s, color=NOIR)
        i += 1; continue

    # ── Corps de texte ─────────────────────────────────────
    p = doc.add_paragraph()
    inline(p, s)
    i += 1

doc.save("LIVRE-FINAL.docx")
sz = os.path.getsize("LIVRE-FINAL.docx")
print(f"DOCX Sahel Rouge KDP: {round(sz/1024)} Ko, {len(doc.tables)} encadrés")
print(f"Format: 6×9 in, marges inside 0.80\", outside 0.60\", top 0.75\", bottom 0.70\"")
