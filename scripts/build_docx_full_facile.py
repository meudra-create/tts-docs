#!/usr/bin/env python3
"""Génère le DOCX complet depuis les sources markdown — identique au PDF :
gras/italique inline, pages de partie, filet or sur citations, en-tête/pied de page."""
import os, re, glob
from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION_START
from docx.enum.table import WD_ALIGN_VERTICAL, WD_ROW_HEIGHT_RULE

# ─── Couleurs ─────────────────────────────────────────────────────────────────
ARDOISE      = "2C3A4A"
ARDOISE_RGB  = RGBColor(0x2C, 0x3A, 0x4A)
GOLD_HEX     = "A07820"
GOLD_RGB     = RGBColor(0xA0, 0x78, 0x20)
DARK_RED_RGB = RGBColor(0x8B, 0x1A, 0x1A)
WHITE_RGB    = RGBColor(0xFF, 0xFF, 0xFF)
CREAM_HEX    = "F4EFE4"
GRIS_RGB     = RGBColor(0x3C, 0x3C, 0x3C)
FONT_NAME    = "FreeSerif"
BORDER_SZ    = "7"   # 0.90 pt

# Pages de partie (même dict que build_pdf.py)
PART_PAGES = {
    4:  ("PARTIE I",   "L'Afrique avant la domination"),
    8:  ("PARTIE II",  "Comment la dépendance a été organisée"),
    14: ("PARTIE III", "La guerre du Sahel"),
    19: ("PARTIE IV",  "La révolution de la souveraineté"),
    25: ("PARTIE V",   "Le réveil panafricain"),
    29: ("PARTIE VI",  "Les défis de demain"),
}

# ─── XML helpers ──────────────────────────────────────────────────────────────
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

def set_letter_spacing(run, points):
    """Espacement des lettres (w:spacing en 1/20e de point) — reproduit
    \\addfontfeature{LetterSpace=...} du PDF sur le label « PARTIE X »."""
    rPr = run._r.find(qn('w:rPr'))
    if rPr is None:
        rPr = OxmlElement('w:rPr'); run._r.insert(0, rPr)
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:val'), str(int(points * 20)))
    rPr.append(spacing)

def set_section_valign(section, val):
    """Centre verticalement le contenu d'une section sur la page (w:vAlign) —
    remplace les pavés de paragraphes vides utilisés pour simuler \\vfill, qui
    provoquaient des pages blanches en cas de débordement. val: 'top'|'center'|
    'bottom'|'both' (justifié)."""
    sectPr = section._sectPr
    va = OxmlElement('w:vAlign')
    va.set(qn('w:val'), val)
    ex = sectPr.find(qn('w:vAlign'))
    if ex is not None: sectPr.remove(ex)
    sectPr.append(va)

def suppress_header_footer_this_page(section):
    """Masque l'en-tête/pied de page sur la première (et unique) page de cette
    section — reproduit \\thispagestyle{empty} du PDF pour les pages de partie."""
    section.different_first_page_header_footer = True
    fh = section.first_page_header
    for p in fh.paragraphs:
        p.clear()
    ff = section.first_page_footer
    for p in ff.paragraphs:
        p.clear()

def add_page_break(doc):
    p = doc.add_paragraph()
    run = p.add_run()
    br = OxmlElement('w:br')
    br.set(qn('w:type'), 'page')
    run._r.append(br)

# ─── Inline formatting parser ─────────────────────────────────────────────────
def add_inline_runs(para, text, size=11, color=None, italic_base=False):
    """Parse **bold**, *italic*, `code` et crée des runs Word distincts."""
    # Nettoyage simple du texte brut
    text = text.strip()
    if not text:
        return
    # Tokenisation : **gras**, *italique*, `code`, reste
    pattern = r'(\*\*[^*]+?\*\*|\*[^*]+?\*|`[^`]+?`)'
    parts = re.split(pattern, text)
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**') and len(part) > 4:
            styled_run(para, part[2:-2], bold=True, italic=italic_base, size=size, color=color)
        elif part.startswith('*') and part.endswith('*') and len(part) > 2:
            styled_run(para, part[1:-1], italic=True, size=size, color=color)
        elif part.startswith('`') and part.endswith('`') and len(part) > 2:
            styled_run(para, part[1:-1], size=size - 0.5, color=GRIS_RGB)
        else:
            styled_run(para, part, italic=italic_base, size=size, color=color)

# ─── Éléments de document ────────────────────────────────────────────────────
def _set_outline_level(para, level):
    """Marque un paragraphe comme titre de niveau `level` (0 = Heading 1) pour
    que le champ TOC natif de Word le détecte, sans changer son style visuel."""
    pPr = para._p.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr'); para._p.insert(0, pPr)
    ol = OxmlElement('w:outlineLvl')
    ol.set(qn('w:val'), str(level))
    ex = pPr.find(qn('w:outlineLvl'))
    if ex is not None: pPr.remove(ex)
    pPr.append(ol)

def add_heading1(doc, text):
    """Bandeau ardoise plein + titre blanc capitales.
    PDF : filet or 2.5pt au-dessus, bandeau ardoise, filet or 1pt en dessous.
    Marqué comme titre de niveau 1 pour alimenter le sommaire (TOC), exactement
    comme \\addcontentsline{toc}{section}{...} ne s'applique qu'aux H1 en PDF."""
    # Filet or au-dessus (2.5pt = sz 20 en 1/8pt)
    top_rule = doc.add_paragraph(style='Normal')
    top_rule.paragraph_format.space_before = Pt(10)
    top_rule.paragraph_format.space_after  = Pt(0)
    set_para_border(top_rule, 'bottom', GOLD_HEX, sz="20", space="0")
    # Bandeau ardoise + texte blanc centré
    para = doc.add_paragraph(style='Normal')
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(0)
    para.paragraph_format.space_after  = Pt(0)
    para.paragraph_format.space_before = Pt(10)
    para.paragraph_format.space_after  = Pt(10)
    set_para_shading(para, ARDOISE)
    set_para_border(para, 'bottom', GOLD_HEX, sz="8", space="0")
    clean = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    clean = re.sub(r'\*(.+?)\*', r'\1', clean)
    styled_run(para, clean, color=WHITE_RGB, bold=False, size=13.2, caps=True)
    _set_outline_level(para, 0)

def add_heading2(doc, text):
    """H2 ardoise gras + filet or — espacements PDF : 14pt avant / 6pt après."""
    para = doc.add_paragraph(style='Normal')
    para.paragraph_format.space_before = Pt(14)
    para.paragraph_format.space_after  = Pt(6)
    set_para_border(para, 'bottom', GOLD_HEX, sz=BORDER_SZ, space="3")
    clean = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    clean = re.sub(r'\*(.+?)\*', r'\1', clean)
    styled_run(para, clean, color=ARDOISE_RGB, bold=True, size=11)

def add_heading3(doc, text):
    """H3 ardoise gras \small — espacements PDF : 10pt avant / 4pt après."""
    para = doc.add_paragraph(style='Normal')
    para.paragraph_format.space_before = Pt(10)
    para.paragraph_format.space_after  = Pt(4)
    clean = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    clean = re.sub(r'\*(.+?)\*', r'\1', clean)
    styled_run(para, clean, color=ARDOISE_RGB, bold=True, size=10)

def add_section_rule(doc):
    """Filet or horizontal (PDF \sectionrule) — reproduit le --- markdown."""
    para = doc.add_paragraph()
    para.paragraph_format.space_before = Pt(6)
    para.paragraph_format.space_after  = Pt(6)
    set_para_border(para, 'bottom', GOLD_HEX, sz="3", space="2")

def add_separator(doc):
    """Séparateur typographique — PDF : \\separator rend « *  *  * » (astérisques,
    pas des étoiles), en \\large (≈14.4pt) doré centré."""
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(10)
    para.paragraph_format.space_after  = Pt(8)
    styled_run(para, '*  *  *', color=GOLD_RGB, size=14.4)

def add_quote(doc, text):
    """Citation : filet or gauche 2pt + rouge italique interligne 1.5 — PDF skipabove/below 14pt."""
    clean = re.sub(r'^> ?', '', text, flags=re.MULTILINE).strip()
    if not clean:
        return
    para = doc.add_paragraph(style='Normal')
    # innerleftmargin 18pt + leftmargin 0pt → indent Word équivalent
    para.paragraph_format.left_indent  = Cm(0.64)   # ≈ 18pt
    para.paragraph_format.right_indent = Cm(0.21)   # ≈ 6pt
    para.paragraph_format.space_before = Pt(14)     # skipabove PDF
    para.paragraph_format.space_after  = Pt(14)     # skipbelow PDF
    # Interligne 1.5 sur la citation (PDF : \setstretch{1.5} dans citblock)
    from docx.oxml import OxmlElement as _OE
    pPr = para._p.find(qn('w:pPr'))
    if pPr is None:
        pPr = _OE('w:pPr'); para._p.insert(0, pPr)
    lsEl = pPr.find(qn('w:jc'))  # just to ensure pPr exists
    spacing = _OE('w:spacing')
    spacing.set(qn('w:line'), '360')      # 360/240 = 1.5x
    spacing.set(qn('w:lineRule'), 'auto')
    ex = pPr.find(qn('w:spacing'))
    if ex is not None: pPr.remove(ex)
    pPr.append(spacing)
    # Filet or gauche 2 pt (sz=16 = 2pt en 1/8pt)
    set_para_border(para, 'left', GOLD_HEX, sz="16", space="18")
    add_inline_runs(para, clean, size=11, color=DARK_RED_RGB, italic_base=True)

def add_normal(doc, text, no_indent=False):
    """Paragraphe courant — retrait 1 cm sauf après un titre (\noindent PDF)."""
    para = doc.add_paragraph(style='Normal')
    if not no_indent:
        para.paragraph_format.first_line_indent = Cm(1.0)
    para.paragraph_format.space_after = Pt(3)
    add_inline_runs(para, text, size=11)
    return para

def add_bullet(doc, text):
    """Puce — texte noir, taille \small = 10pt comme en PDF dans itemize."""
    para = doc.add_paragraph(style='List Bullet')
    add_inline_runs(para, text, size=10.5)  # noir pur
    return para

def _set_cell_border(cell, sides=None, sz="4", color=ARDOISE, val="single"):
    """Applique des bordures individuelles sur une cellule."""
    tc = cell._tc
    tcPr = tc.find(qn('w:tcPr'))
    if tcPr is None:
        tcPr = OxmlElement('w:tcPr'); tc.insert(0, tcPr)
    tcBorders = tcPr.find(qn('w:tcBorders'))
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders'); tcPr.append(tcBorders)
    for side in (sides or []):
        el = OxmlElement(f'w:{side}')
        el.set(qn('w:val'), val)
        el.set(qn('w:sz'), sz)
        el.set(qn('w:space'), '0')
        el.set(qn('w:color'), color)
        ex = tcBorders.find(qn(f'w:{side}'))
        if ex is not None: tcBorders.remove(ex)
        tcBorders.append(el)
    # Supprimer tous les autres côtés (none)
    all_sides = {'top','left','bottom','right','insideH','insideV'}
    for side in all_sides - set(sides or []):
        el = OxmlElement(f'w:{side}')
        el.set(qn('w:val'), 'none')
        el.set(qn('w:sz'), '0')
        el.set(qn('w:space'), '0')
        el.set(qn('w:color'), 'auto')
        ex = tcBorders.find(qn(f'w:{side}'))
        if ex is not None: tcBorders.remove(ex)
        tcBorders.append(el)

def _inline_clean(text):
    t = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    return re.sub(r'\*(.+?)\*', r'\1', t).strip()

def add_pipe_table(doc, header, rows):
    """Timeline verticale — identique au PDF (Option C).
    2 colonnes : table 2-col avec règle ardoise verticale.
    3+ colonnes : paragraphes empilés avec bullets or et connecteurs ardoise.
    """
    n = max(1, len(header))

    # ── Espace avant ─────────────────────────────────────────────────────────
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(6)
    sp.paragraph_format.space_after  = Pt(0)

    if n == 2:
        # ── 2 colonnes : table timeline ──────────────────────────────────────
        # Largeurs ~ 28 % / 62 % de la zone texte (15.5 cm = 21-2.5-2.5 cm)
        LEFT_W  = Cm(4.0)
        RIGHT_W = Cm(9.5)

        # Ligne d'en-tête (labels italiques ardoise)
        hdr_tbl = doc.add_table(rows=1, cols=2)
        hdr_tbl.allow_autofit = False
        hdr_tbl.columns[0].width = LEFT_W
        hdr_tbl.columns[1].width = RIGHT_W
        hl = hdr_tbl.rows[0].cells[0]
        hr = hdr_tbl.rows[0].cells[1]
        _set_cell_border(hl, sides=[])
        _set_cell_border(hr, sides=[])
        hl.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        styled_run(hl.paragraphs[0], _inline_clean(header[0]), color=ARDOISE_RGB, italic=True, size=9)
        styled_run(hr.paragraphs[0], _inline_clean(header[1]), color=ARDOISE_RGB, italic=True, size=9)

        # Filet or sous les en-têtes
        sep = doc.add_paragraph()
        sep.paragraph_format.space_before = Pt(1)
        sep.paragraph_format.space_after  = Pt(1)
        set_para_border(sep, 'bottom', GOLD_HEX, sz="4", space="2")

        # Lignes de données
        data_tbl = doc.add_table(rows=len(rows), cols=2)
        data_tbl.allow_autofit = False
        data_tbl.columns[0].width = LEFT_W
        data_tbl.columns[1].width = RIGHT_W
        for r, row in enumerate(rows):
            cl = data_tbl.rows[r].cells[0]
            cr = data_tbl.rows[r].cells[1]
            # Bordures : seule la ligne verticale entre les deux cols (ardoise 0.5pt)
            _set_cell_border(cl, sides=['right'], sz="4", color=ARDOISE)
            _set_cell_border(cr, sides=['left'],  sz="4", color=ARDOISE)
            # Cellule gauche : right-aligned, bullet or + label ardoise
            cl.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            cl.paragraphs[0].paragraph_format.right_indent = Cm(0.2)
            styled_run(cl.paragraphs[0], '● ', color=GOLD_RGB, size=8)
            styled_run(cl.paragraphs[0], _inline_clean(row[0]) if row else '',
                       color=ARDOISE_RGB, size=9)
            # Cellule droite : contenu gris
            cr.paragraphs[0].paragraph_format.left_indent = Cm(0.2)
            c1 = _inline_clean(row[1]) if len(row) > 1 else ''
            add_inline_runs(cr.paragraphs[0], c1, size=9, color=GRIS_RGB)
    else:
        # ── 3+ colonnes : empilés verticaux ──────────────────────────────────
        # En-tête : labels italiques ardoise séparés par " | "
        h_para = doc.add_paragraph()
        h_para.paragraph_format.space_after = Pt(1)
        for idx, h in enumerate(header):
            if idx > 0:
                styled_run(h_para, '  |  ', color=ARDOISE_RGB, size=9)
            styled_run(h_para, _inline_clean(h), color=ARDOISE_RGB, italic=True, size=9)

        # Filet or
        sep = doc.add_paragraph()
        sep.paragraph_format.space_before = Pt(1)
        sep.paragraph_format.space_after  = Pt(2)
        set_para_border(sep, 'bottom', GOLD_HEX, sz="4", space="2")

        for idx, row in enumerate(rows):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after  = Pt(0)
            p.paragraph_format.left_indent  = Cm(0.3)
            styled_run(p, '● ', color=GOLD_RGB, size=9)
            styled_run(p, _inline_clean(row[0]) if row else '',
                       color=ARDOISE_RGB, size=9)
            for c in row[1:n]:
                styled_run(p, '  —  ', color=ARDOISE_RGB, size=9)
                add_inline_runs(p, _inline_clean(c), size=9, color=GRIS_RGB)
            # Connecteur vertical ardoise entre les items
            if idx < len(rows) - 1:
                cp = doc.add_paragraph()
                cp.paragraph_format.space_before = Pt(0)
                cp.paragraph_format.space_after  = Pt(0)
                cp.paragraph_format.left_indent  = Cm(0.3)
                styled_run(cp, '│', color=ARDOISE_RGB, size=8)

    # ── Espace après ─────────────────────────────────────────────────────────
    ep = doc.add_paragraph()
    ep.paragraph_format.space_before = Pt(0)
    ep.paragraph_format.space_after  = Pt(6)

def add_styled_table(doc, title, rows):
    """Encadré 1 colonne : header ardoise blanc 10pt caps, lignes crème gris 10pt (= PDF \small)."""
    table = doc.add_table(rows=1 + len(rows), cols=1)
    set_table_borders(table, BORDER_SZ, ARDOISE)
    hc = table.rows[0].cells[0]
    set_cell_fill(hc, ARDOISE)
    hc.paragraphs[0].paragraph_format.left_indent = Cm(0.2)
    styled_run(hc.paragraphs[0], title, color=WHITE_RGB, bold=True, size=10, caps=True)
    for i, row_text in enumerate(rows):
        cell = table.rows[i + 1].cells[0]
        set_cell_fill(cell, CREAM_HEX)
        cell.paragraphs[0].paragraph_format.left_indent = Cm(0.2)
        add_inline_runs(cell.paragraphs[0], row_text, size=10, color=GRIS_RGB)   # \small = 10pt
    doc.add_paragraph()

# ─── Page de partie ───────────────────────────────────────────────────────────
def add_part_page(doc, roman, subtitle):
    """Contenu de la page de partie : fond BLANC, label + titre en ardoise
    centrés, filet or court (8cm) centré sous le titre. Reproduit \\partpage
    du PDF (PARTIE X / TITRE / filet or) — PAS de fond ardoise ni de texte
    blanc, contrairement au bandeau H1. Ne gère PAS les sauts de page : la
    page dédiée et le centrage vertical (w:vAlign) sont gérés par la boucle
    d'assemblage via un saut de section, pour éviter tout risque de page
    blanche liée à un remplissage de paragraphes vides."""
    # « PARTIE X » — petit, ardoise, lettres espacées, MAJUSCULES
    p1 = doc.add_paragraph(style='Normal')
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_after = Pt(24)
    r1 = styled_run(p1, roman, color=ARDOISE_RGB, bold=False, size=12, caps=True)
    set_letter_spacing(r1, 2.5)

    # Titre de partie — grand, ardoise, MAJUSCULES, centré (peut passer sur 2 lignes)
    p2 = doc.add_paragraph(style='Normal')
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_after = Pt(30)
    styled_run(p2, subtitle.upper(), color=ARDOISE_RGB, bold=False, size=26)

    # Filet or court (8cm, ~1.5pt), centré — table 1x1 sans bordures sauf bottom
    rule_tbl = doc.add_table(rows=1, cols=1)
    rule_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    rule_tbl.autofit = False
    rule_tbl.columns[0].width = Cm(8.0)
    rc = rule_tbl.rows[0].cells[0]
    rc.width = Cm(8.0)
    _set_cell_border(rc, sides=['bottom'], sz="12", color=GOLD_HEX)
    rc.paragraphs[0].paragraph_format.space_after = Pt(0)

# ─── En-tête et pied de page ─────────────────────────────────────────────────
def setup_header_footer(doc):
    """Ajoute en-tête gauche/droite et pied de page centré (numéro de page)."""
    section = doc.sections[0]
    section.different_first_page_header_footer = True

    header = section.header
    header.is_linked_to_previous = False
    # Vider l'en-tête par défaut
    for p in header.paragraphs:
        p.clear()
    hp = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    hp.paragraph_format.space_after = Pt(2)
    set_para_border(hp, 'bottom', GOLD_HEX, sz=BORDER_SZ, space="2")
    # Gauche : BEN-H2O (or)
    styled_run(hp, "BEN–H2O", color=GOLD_RGB, size=8, italic=True)
    # Tabulation centrée → droite
    run_tab = hp.add_run("\t")
    run_tab.font.name = FONT_NAME
    # Droite : titre (ardoise)
    styled_run(hp, "LA PAIX, ON PEUT L'ÉVITER — FACILE", color=ARDOISE_RGB, size=8)

    footer = section.footer
    footer.is_linked_to_previous = False
    for p in footer.paragraphs:
        p.clear()
    fp = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    # Numéro de page via champ Word
    fld_begin = OxmlElement('w:fldChar')
    fld_begin.set(qn('w:fldCharType'), 'begin')
    inst = OxmlElement('w:instrText')
    inst.text = ' PAGE '
    fld_end = OxmlElement('w:fldChar')
    fld_end.set(qn('w:fldCharType'), 'end')
    run = fp.add_run()
    run.font.name = FONT_NAME
    run.font.size = Pt(9)
    run.font.color.rgb = ARDOISE_RGB
    run._r.append(fld_begin)
    run._r.append(inst)
    run._r.append(fld_end)

# ─── Parseur markdown ────────────────────────────────────────────────────────
def _split_pipe_row(line):
    s = line.strip()
    if s.startswith('|'): s = s[1:]
    if s.endswith('|'):   s = s[:-1]
    return [c.strip() for c in s.split('|')]

def parse_and_append(doc, md_text):
    lines = md_text.split('\n')
    i = 0
    quote_buf = []
    after_heading = False   # \noindent PDF : pas de retrait après un titre

    def flush_quote():
        nonlocal after_heading
        if quote_buf:
            add_quote(doc, '\n'.join(quote_buf).strip())
            quote_buf.clear()
            after_heading = False

    while i < len(lines):
        line = lines[i]

        # Ligne vide ou \newpage
        if not line.strip() or line.strip() == r'\newpage':
            flush_quote(); i += 1; continue

        # Titres
        if line.startswith('# '):
            flush_quote(); add_heading1(doc, line[2:].strip()); after_heading = True; i += 1; continue
        if line.startswith('## '):
            flush_quote(); add_heading2(doc, line[3:].strip()); after_heading = True; i += 1; continue
        if line.startswith('### '):
            flush_quote(); add_heading3(doc, line[4:].strip()); after_heading = True; i += 1; continue

        # Séparateurs --- et ★★★
        if re.match(r'^---+$', line.strip()):
            flush_quote(); add_section_rule(doc); after_heading = False; i += 1; continue
        if line.strip() in ('★★★', '*   *   *', '* * *'):
            flush_quote(); add_separator(doc); after_heading = False; i += 1; continue

        # Citations
        if line.startswith('>'):
            quote_buf.append(re.sub(r'^> ?', '', line)); i += 1; continue

        # Tableau pipe markdown
        if (re.match(r'^\s*\|.*\|\s*$', line)
                and i + 1 < len(lines)
                and re.match(r'^\s*\|[\s:|\-]+\|\s*$', lines[i+1])
                and '-' in lines[i+1]):
            flush_quote()
            header = _split_pipe_row(line)
            j = i + 2; body = []
            while j < len(lines) and re.match(r'^\s*\|.*\|\s*$', lines[j]):
                body.append(_split_pipe_row(lines[j])); j += 1
            add_pipe_table(doc, header, body)
            after_heading = False; i = j; continue

        # Listes
        if re.match(r'^[-*] ', line):
            flush_quote()
            add_bullet(doc, line[2:].strip()); after_heading = False; i += 1; continue
        if re.match(r'^\d+\. ', line):
            flush_quote()
            add_bullet(doc, re.sub(r'^\d+\. ', '', line)); after_heading = False; i += 1; continue

        # Ligne bold seule → possible encadré
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
                    rows.append(content); j += 1
                else:
                    break
            if rows:
                add_styled_table(doc, title, rows); after_heading = False; i = j
            else:
                p = doc.add_paragraph(style='Normal')
                styled_run(p, title, color=ARDOISE_RGB, bold=True, size=11)
                after_heading = False; i += 1
            continue

        # Paragraphe courant
        flush_quote()
        text = line.strip()
        if text:
            add_normal(doc, text, no_indent=after_heading)
            after_heading = False
        i += 1

    flush_quote()

# ─── Construction du document ─────────────────────────────────────────────────
doc = Document()

# Format A4 + marges identiques au PDF
for section in doc.sections:
    section.page_width    = Cm(21.0)
    section.page_height   = Cm(29.7)
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin   = Cm(2.5)
    section.right_margin  = Cm(2.0)

# Interligne 1.3 et police de base FreeSerif 11pt sur le style Normal
from docx.oxml import OxmlElement as _OE
normal_style = doc.styles['Normal']
normal_style.font.name = FONT_NAME
normal_style.font.size = Pt(11)
# Interligne 1.3 via XML sur le style (cascade sur tous les paragraphes)
pPr_style = normal_style.element.find(qn('w:pPr'))
if pPr_style is None:
    pPr_style = _OE('w:pPr')
    normal_style.element.append(pPr_style)
sp_el = _OE('w:spacing')
sp_el.set(qn('w:line'), '360')       # 360/240 = 1.5x — identique PDF \setstretch{1.5}
sp_el.set(qn('w:lineRule'), 'auto')
ex = pPr_style.find(qn('w:spacing'))
if ex is not None: pPr_style.remove(ex)
pPr_style.append(sp_el)

setup_header_footer(doc)

# ── Page de titre ──────────────────────────────────────────────────────────────
# Fond ardoise plein garanti par une table 1x1 de hauteur ≥ page utile (pas de
# pavés de paragraphes vides à compter — source des pages blanches corrigées
# ici), contenu centré verticalement dans la cellule (w:vAlign="center").
section0 = doc.sections[0]
section0.different_first_page_header_footer = True

usable_h = Cm(29.7 - 2.5 - 2.5)   # hauteur de page utile (marges haut/bas)
usable_w = Cm(21.0 - 2.5 - 2.0)   # largeur de page utile (marges gauche/droite)

title_tbl = doc.add_table(rows=1, cols=1)
title_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
title_tbl.autofit = False
title_tbl.columns[0].width = usable_w
title_tbl.rows[0].height = usable_h
title_tbl.rows[0].height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
tcell = title_tbl.rows[0].cells[0]
tcell.width = usable_w
set_cell_fill(tcell, ARDOISE)
tcell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
_set_cell_border(tcell, sides=[])   # pas de bordure visible autour de la cellule

tp = tcell.paragraphs[0]
tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
tp.paragraph_format.space_after = Pt(24)
styled_run(tp, "LA PAIX, ON PEUT L'ÉVITER", color=WHITE_RGB, bold=True, size=24.9, caps=True)

tp1b = tcell.add_paragraph()
tp1b.alignment = WD_ALIGN_PARAGRAPH.CENTER
tp1b.paragraph_format.space_after = Pt(10)
styled_run(tp1b, "Version en français facile", color=GOLD_RGB, bold=True, size=15)

tp2 = tcell.add_paragraph()
tp2.alignment = WD_ALIGN_PARAGRAPH.CENTER
tp2.paragraph_format.space_after = Pt(40)
styled_run(tp2,
    "Enquête sur la naissance de l'Alliance des États du Sahel",
    color=GOLD_RGB, italic=True, size=13.2)

tp3 = tcell.add_paragraph()
tp3.alignment = WD_ALIGN_PARAGRAPH.CENTER
tp3.paragraph_format.space_after = Pt(10)
styled_run(tp3, "BEN–H2O", color=WHITE_RGB, bold=True, size=17.3)

tp4 = tcell.add_paragraph()
tp4.alignment = WD_ALIGN_PARAGRAPH.CENTER
tp4.paragraph_format.space_after = Pt(60)
styled_run(tp4, "— 2026 —", color=GOLD_RGB, size=11)

tp5 = tcell.add_paragraph()
tp5.alignment = WD_ALIGN_PARAGRAPH.CENTER
styled_run(tp5, "© 2026 BEN–H2O — Tous droits réservés.", color=GOLD_RGB, size=9.2)

# Saut de page unique vers le sommaire (la table fait déjà une page pleine).
add_page_break(doc)

# ── Sommaire (table des matières) ────────────────────────────────────────────
# Reproduit \tableofcontents du PDF : une page dédiée, juste après le titre,
# listant uniquement les titres de chapitre (H1) — via un champ TOC natif Word
# qui s'appuie sur les paragraphes marqués outlineLvl=0 par add_heading1().
toc_title = doc.add_paragraph(style='Normal')
toc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
toc_title.paragraph_format.space_after = Pt(18)
styled_run(toc_title, "Sommaire", color=ARDOISE_RGB, bold=True, size=18, caps=True)

toc_hint = doc.add_paragraph(style='Normal')
toc_hint.alignment = WD_ALIGN_PARAGRAPH.CENTER
toc_hint.paragraph_format.space_after = Pt(12)
styled_run(toc_hint,
    "(Sélectionner tout — Ctrl+A — puis F9 pour générer la pagination.)",
    color=GRIS_RGB, italic=True, size=9)

toc_para = doc.add_paragraph(style='Normal')
fld_begin = OxmlElement('w:fldChar'); fld_begin.set(qn('w:fldCharType'), 'begin')
fld_begin.set(qn('w:dirty'), 'true')
instr = OxmlElement('w:instrText'); instr.set(qn('xml:space'), 'preserve')
instr.text = r'TOC \o "1-1" \h \z \u'
fld_sep = OxmlElement('w:fldChar'); fld_sep.set(qn('w:fldCharType'), 'separate')
fld_end = OxmlElement('w:fldChar'); fld_end.set(qn('w:fldCharType'), 'end')
r1 = toc_para.add_run(); r1._r.append(fld_begin)
r2 = toc_para.add_run(); r2._r.append(instr)
r3 = toc_para.add_run(); r3._r.append(fld_sep)
r4 = toc_para.add_run("Le sommaire s'affichera ici après mise à jour des champs.")
r4.font.name = FONT_NAME; r4.font.color.rgb = ARDOISE_RGB; r4.font.size = Pt(10)
r5 = toc_para.add_run(); r5._r.append(fld_end)

# Force Word/LibreOffice à recalculer les champs (TOC + numéros de page) à
# l'ouverture du document, pour que le sommaire soit correct sans action manuelle.
settings_el = doc.settings.element
update_fields = OxmlElement('w:updateFields')
update_fields.set(qn('w:val'), 'true')
settings_el.append(update_fields)

# ── Chapitres ─────────────────────────────────────────────────────────────────
chapter_dir = "/home/user/tts-docs/content/5.livre-facile/"
files = sorted(
    glob.glob(os.path.join(chapter_dir, "[0-9]*.md")),
    key=lambda x: int(os.path.basename(x).split(".")[0]))

print(f"Assemblage de {len(files)} chapitres...")
for filepath in files:
    num = int(os.path.basename(filepath).split(".")[0])

    # Page de partie avant ce numéro ? Chaque page de partie vit dans sa
    # propre section (saut de page automatique en entrée ET en sortie —
    # donc PAS de add_page_break() supplémentaire autour, ce qui causait
    # auparavant une page blanche par partie). Centrage vertical du contenu
    # et masquage de l'en-tête/pied de page (\thispagestyle{empty} du PDF).
    if num in PART_PAGES:
        roman, subtitle = PART_PAGES[num]
        doc.add_section(WD_SECTION_START.NEW_PAGE)
        suppress_header_footer_this_page(doc.sections[-1])
        add_part_page(doc, roman, subtitle)
        doc.add_section(WD_SECTION_START.NEW_PAGE)
        set_section_valign(doc.sections[-2], 'center')
    else:
        add_page_break(doc)

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    # Supprimer le frontmatter YAML
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2].strip()

    parse_and_append(doc, content)
    print(f"  ✓ {num}: {os.path.basename(filepath)[:55]}")

out = "/home/user/tts-docs/la-paix-on-peut-leviter-facile.docx"
doc.save(out)
print(f"\nSaved: {out}  ({os.path.getsize(out)/1024:.1f} KB)")
