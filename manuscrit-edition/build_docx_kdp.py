import docx, re, os
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ══════════════════════════════════════════
#  THÈME — ARDOISE & OR  ×  FORMAT KDP
#  Identique au PDF · Trim 6 × 9 in · ★★★
# ══════════════════════════════════════════

# Palette Ardoise & Or (identique au PDF)
BLANC     = RGBColor(0xFF, 0xFF, 0xFF)
ARDOISE   = RGBColor(0x2C, 0x3A, 0x4A)
ARDOISE_L = RGBColor(0x3D, 0x50, 0x68)
OR        = RGBColor(0xA0, 0x78, 0x20)   # or satiné
OR_CLAIR  = RGBColor(0xC9, 0xA2, 0x4A)
CREME     = RGBColor(0xF4, 0xEF, 0xE4)
CREME_BD  = RGBColor(0xD8, 0xCE, 0xBC)
GRIS_TX   = RGBColor(0x2E, 0x2E, 0x2E)
BORDEAUX  = RGBColor(0x8B, 0x1A, 0x1A)   # citations en exergue
NOIR      = RGBColor(0x0A, 0x0A, 0x0A)
IVOIRE    = RGBColor(0xF5, 0xF0, 0xE8)
GRISRG    = RGBColor(0x6A, 0x5A, 0x44)   # gris chaud (auteur de citation)
# Fonds hexadécimaux (shading)
HEX_ARDOISE = '2C3A4A'
HEX_CREME   = 'F4EFE4'
HEX_OR      = 'A07820'
FONT        = 'FreeSerif'

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

# Le pied de page est ajouté plus bas, après la définition de force_font_run.

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

set_heading('Heading 1', 15, ARDOISE, space_before=18, space_after=10)
set_heading('Heading 2', 12, ARDOISE, space_before=14, space_after=6)
set_heading('Heading 3', 11, OR, space_before=10, space_after=4)
force_font(n, FONT)

def force_font_run(r):
    rpr = r._r.get_or_add_rPr()
    rf  = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts'); rpr.append(rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:cs'):
        rf.set(qn(a), FONT)

# ── Numérotation des pages (pied de page centré « — N — ») ─
def add_page_number_footer(section):
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p.add_run("— ")
    fld_begin = OxmlElement('w:fldChar'); fld_begin.set(qn('w:fldCharType'), 'begin')
    instr     = OxmlElement('w:instrText'); instr.set(qn('xml:space'), 'preserve'); instr.text = "PAGE"
    fld_end   = OxmlElement('w:fldChar'); fld_end.set(qn('w:fldCharType'), 'end')
    r_field = p.add_run()
    r_field._r.append(fld_begin); r_field._r.append(instr); r_field._r.append(fld_end)
    r2 = p.add_run(" —")
    for r in (r1, r_field, r2):
        r.font.size = Pt(9); r.font.name = FONT
        r.font.color.rgb = RGBColor(0xA8, 0xA8, 0xA0)
        force_font_run(r)

add_page_number_footer(sec)

# ── Helpers ────────────────────────────────────────────────
def bottom_border(p, color="A07820", sz="18"):
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr')
    b = OxmlElement('w:bottom')
    b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), sz)
    b.set(qn('w:space'), '4');    b.set(qn('w:color'), color)
    pbdr.append(b); pPr.append(pbdr)

def top_border(p, color="A07820", sz="18"):
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
    """★★★ — or, centré, sans espace entre les étoiles (charte habillage)"""
    p = center("★★★", size=11, color=OR, space_before=8, space_after=8)
    return p

def quote(text):
    is_attrib = text.lstrip().startswith("—")
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.italic = True
    if is_attrib:
        r.font.size = Pt(9); r.font.color.rgb = NOIR
    else:
        r.font.size = Pt(10); r.font.color.rgb = BORDEAUX
    p.paragraph_format.left_indent  = Cm(1.0)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(6)
    pPr  = p._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr')
    lft  = OxmlElement('w:left')
    # sz est en huitièmes de point : 0,5 pt = 4 huitièmes
    lft.set(qn('w:val'), 'single'); lft.set(qn('w:sz'), '4')
    lft.set(qn('w:space'), '8');    lft.set(qn('w:color'), 'A07820')
    pbdr.append(lft); pPr.append(pbdr)
    return p

def shade(cell, hexfill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd  = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:fill'), hexfill)
    tcPr.append(shd)

def para_shade(p, hexfill):
    """Fond de paragraphe (bandeau)."""
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:fill'), hexfill)
    pPr.append(shd)

def set_table_borders(tbl, color='2C3A4A', sz='8'):
    """Bordures uniformes (encadrés ardoise)."""
    tblPr = tbl._tbl.tblPr
    borders = OxmlElement('w:tblBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement(f'w:{edge}')
        e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), sz)
        e.set(qn('w:space'), '0');    e.set(qn('w:color'), color)
        borders.append(e)
    tblPr.append(borders)

def chapter_band(title):
    """Bandeau de chapitre : fond ardoise, texte blanc capitales, filet or au-dessus."""
    p = doc.add_paragraph()
    p.style = doc.styles['Heading 1']          # conserve la structure / le plan
    pf = p.paragraph_format
    pf.alignment    = WD_ALIGN_PARAGRAPH.LEFT
    pf.space_before = Pt(6)
    pf.space_after  = Pt(16)
    pf.line_spacing = 1.25
    para_shade(p, HEX_ARDOISE)
    top_border(p, color=HEX_OR, sz="34")       # filet or épais (~4,5 pt)
    r = p.add_run(title.upper())
    r.bold = True; r.font.size = Pt(14)
    r.font.color.rgb = BLANC; r.font.name = FONT
    force_font_run(r)
    return p

def inline(p, s):
    for seg in re.split(r'(\*\*.+?\*\*|\*.+?\*)', s):
        if not seg: continue
        if seg.startswith("**") and seg.endswith("**"):
            r = p.add_run(seg[2:-2]); r.bold = True
        elif seg.startswith("*") and seg.endswith("*"):
            r = p.add_run(seg[1:-1]); r.italic = True
        else:
            p.add_run(seg)

# ── Sommaire complet (réplique du PDF) ─────────────────────
def toc_entry(text, *, size=10.5, bold=False, italic=False, color=NOIR,
              left_indent=0.0, space_before=0, space_after=2):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment     = WD_ALIGN_PARAGRAPH.LEFT
    pf.left_indent   = Inches(left_indent)
    pf.space_before  = Pt(space_before)
    pf.space_after   = Pt(space_after)
    pf.line_spacing  = 1.2
    r = p.add_run(text)
    r.font.size = Pt(size); r.bold = bold; r.italic = italic
    r.font.color.rgb = color
    force_font_run(r)
    return p

def build_toc_docx(all_lines):
    """Génère un sommaire complet depuis tous les titres H1 (hors 'Sommaire')."""
    for ln in all_lines:
        m = re.match(r'^# (.+)$', ln.strip())
        if not m:
            continue
        title = m.group(1).strip()
        if title.lower() == "sommaire":
            continue
        pm = re.match(r'^(PARTIE\s+[IVX]+)\s+[—–-]\s+(.+)$', title)
        cm = re.match(r'^(Chapitre\s+\d+)\s+[—–-]\s+(.+)$', title)
        if pm:
            toc_entry(f"{pm.group(1)} — {pm.group(2)}", size=10.5, bold=True,
                      color=OR, space_before=12, space_after=3)
        elif cm:
            toc_entry(f"{cm.group(1)} — {cm.group(2)}", size=10,
                      color=GRIS_TX, left_indent=0.30, space_after=1)
        else:
            toc_entry(title, size=10.5, bold=True, italic=True, color=ARDOISE,
                      space_before=5, space_after=2)

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
            set_table_borders(tbl, color=HEX_ARDOISE, sz='8')
            # Entête : fond ardoise, texte blanc capitales
            hd = tbl.rows[0].cells[0]; shade(hd, HEX_ARDOISE)
            ph = hd.paragraphs[0]
            rh = ph.add_run(m_box.group(1).upper())
            rh.bold = True; rh.font.size = Pt(9.5)
            rh.font.color.rgb = BLANC; rh.font.name = FONT
            force_font_run(rh)
            # Corps : fond crème, texte gris
            for bi, btxt in enumerate(bullets):
                c  = tbl.rows[1+bi].cells[0]; shade(c, HEX_CREME)
                pc = c.paragraphs[0]
                rc = pc.add_run(re.sub(r'\*\*(.+?)\*\*', r'\1', btxt))
                rc.font.size = Pt(9.5); rc.font.color.rgb = GRIS_TX; rc.font.name = FONT
                force_font_run(rc)
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
            # Page de partie : 2 filets or, titre ardoise capitales, centré
            for _ in range(5): doc.add_paragraph()
            sep1 = doc.add_paragraph()
            bottom_border(sep1, color="A07820", sz="24")
            p = center(title, size=18, bold=True, color=ARDOISE,
                       space_before=16, space_after=16)
            sep2 = doc.add_paragraph()
            top_border(sep2, color="A07820", sz="24")
        elif title == "Sommaire":
            h = center(title.upper(), size=18, bold=True, color=ARDOISE,
                       space_before=6, space_after=10)
            bottom_border(h, color="A07820", sz="16")
            build_toc_docx(lines)
            # Sauter les puces placeholder du Markdown jusqu'au prochain titre / ornement
            j = i + 1
            while j < len(lines):
                ss = lines[j].strip()
                if ss.startswith("# ") or ss.replace(" ", "") == "★★★":
                    break
                j += 1
            i = j; continue
        else:
            chapter_band(title)
        i += 1; continue

    if s.startswith("## "):
        h2 = doc.add_heading(s[3:].strip(), level=2)
        bottom_border(h2, color="A07820", sz="8")
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
            center(s, size=28, bold=True, color=ARDOISE, space_after=4)
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
print(f"DOCX Ardoise & Or KDP: {round(sz/1024)} Ko, {len(doc.tables)} encadrés")
print(f"Format: 6×9 in, marges inside 0.80\", outside 0.60\", top 0.75\", bottom 0.70\"")
