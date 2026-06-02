# kindle-format

Calibre un livre `.docx` aux spécifications exactes de **Kindle Direct Publishing (KDP)** — ebook Kindle ou impression papier (paperback/hardcover).

## Usage

```
/kindle-format <fichier.docx> [mode]
```

**Modes disponibles :**

| Mode | Format | Usage |
|---|---|---|
| `ebook` | Kindle reflowable (.docx → KDP ebook) | Liseuse Kindle, tablette, appli Kindle |
| `print-6x9` | 6×9 pouces paperback **(recommandé)** | Impression KDP standard — non-fiction, essai |
| `print-5x8` | 5×8 pouces paperback | Format poche |
| `print-55x85` | 5.5×8.5 pouces paperback | Format intermédiaire |

**Exemples :**
```
/kindle-format mon-livre.docx ebook
/kindle-format mon-livre.docx print-6x9
/kindle-format mon-livre.docx print-5x8
```

Si aucun mode n'est précisé, demander à l'utilisateur ou utiliser `print-6x9` (le plus courant pour non-fiction/géopolitique).

---

## Instructions complètes

### Étape 0 — Vérifier les dépendances

```bash
python3 -c "import docx; print('ok')" 2>/dev/null || pip3 install python-docx -q
```

### Étape 1 — Analyser le document source

Avant toute modification, inspecter la structure du document :

```python
from docx import Document
from docx.shared import Pt

doc = Document("<FICHIER_SOURCE>")

print(f"Paragraphes : {len(doc.paragraphs)}")
print(f"Tableaux    : {len(doc.tables)}")
print(f"Sections    : {len(doc.sections)}")

section = doc.sections[0]
print(f"\nPage actuelle :")
print(f"  Largeur  : {section.page_width.cm:.2f} cm")
print(f"  Hauteur  : {section.page_height.cm:.2f} cm")
print(f"  Marge haut    : {section.top_margin.cm:.2f} cm")
print(f"  Marge bas     : {section.bottom_margin.cm:.2f} cm")
print(f"  Marge gauche  : {section.left_margin.cm:.2f} cm")
print(f"  Marge droite  : {section.right_margin.cm:.2f} cm")

# Détecter les chapitres (texte gras + grande taille)
print("\nChapitres détectés :")
chapter_count = 0
for p in doc.paragraphs:
    if p.runs:
        r = p.runs[0]
        try:
            size = r.font.size
            if r.bold and size and size.pt >= 14:
                print(f"  [{chapter_count}] {p.text[:70]!r}")
                chapter_count += 1
        except:
            pass
print(f"Total chapitres : {chapter_count}")

# Tailles de police utilisées
sizes = {}
for p in doc.paragraphs:
    for run in p.runs:
        try:
            s = run.font.size
            if s:
                key = f"{s.pt:.0f}pt"
                sizes[key] = sizes.get(key, 0) + 1
        except:
            pass
print("\nTailles de police :")
for sz, n in sorted(sizes.items(), key=lambda x: -x[1])[:10]:
    print(f"  {sz}: {n} runs")
```

### Étape 2 — Appliquer le format Kindle

Choisir la configuration selon le mode demandé, puis exécuter :

```python
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

SRC = "<FICHIER_SOURCE>"
DST = "<FICHIER_DESTINATION>"

# ══════════════════════════════════════════════════════
# CONFIGURATIONS KDP
# ══════════════════════════════════════════════════════

CONFIGS = {

    # ── Kindle Ebook (reflowable) ──────────────────
    "ebook": {
        "page_width":      None,       # pas de taille fixe
        "page_height":     None,
        "margin_top":      Cm(2.54),
        "margin_bottom":   Cm(2.54),
        "margin_left":     Cm(2.54),
        "margin_right":    Cm(2.54),
        "font_body":       "Georgia",
        "size_body":       Pt(11),
        "size_h1":         Pt(22),     # Titre partie / chapitre principal
        "size_h2":         Pt(16),     # Sous-chapitre
        "size_h3":         Pt(13),     # Section
        "size_h4":         Pt(11.5),   # Sous-section
        "size_quote":      Pt(10.5),
        "size_caption":    Pt(9),
        "line_spacing":    1.3,
        "space_before_h1": Pt(24),
        "space_after_h1":  Pt(12),
        "space_before_h2": Pt(18),
        "space_after_h2":  Pt(8),
        "space_after_para": Pt(6),
        "first_line_indent": Cm(0.7), # indentation première ligne corps
        "chapter_break":   True,       # saut de page avant H1
        "mirror_margins":  False,
        "header_footer":   False,      # pas de header/footer pour ebook
        "toc":             True,
    },

    # ── KDP Print 6×9 (standard non-fiction) ──────
    "print-6x9": {
        "page_width":      Inches(6),
        "page_height":     Inches(9),
        "margin_top":      Inches(1.0),
        "margin_bottom":   Inches(1.0),
        "margin_left":     Inches(1.0),   # intérieur / gouttière
        "margin_right":    Inches(0.75),  # extérieur
        "font_body":       "Garamond",
        "size_body":       Pt(11),
        "size_h1":         Pt(24),
        "size_h2":         Pt(16),
        "size_h3":         Pt(13),
        "size_h4":         Pt(11.5),
        "size_quote":      Pt(10),
        "size_caption":    Pt(9),
        "line_spacing":    1.3,
        "space_before_h1": Pt(36),
        "space_after_h1":  Pt(18),
        "space_before_h2": Pt(24),
        "space_after_h2":  Pt(10),
        "space_after_para": Pt(0),
        "first_line_indent": Cm(0.7),
        "chapter_break":   True,
        "mirror_margins":  True,           # marges miroir pour reliure
        "header_footer":   True,
        "toc":             True,
    },

    # ── KDP Print 5×8 (format poche) ──────────────
    "print-5x8": {
        "page_width":      Inches(5),
        "page_height":     Inches(8),
        "margin_top":      Inches(0.875),
        "margin_bottom":   Inches(0.875),
        "margin_left":     Inches(0.875),
        "margin_right":    Inches(0.75),
        "font_body":       "Garamond",
        "size_body":       Pt(10.5),
        "size_h1":         Pt(20),
        "size_h2":         Pt(14),
        "size_h3":         Pt(12),
        "size_h4":         Pt(11),
        "size_quote":      Pt(9.5),
        "size_caption":    Pt(8.5),
        "line_spacing":    1.25,
        "space_before_h1": Pt(30),
        "space_after_h1":  Pt(14),
        "space_before_h2": Pt(18),
        "space_after_h2":  Pt(8),
        "space_after_para": Pt(0),
        "first_line_indent": Cm(0.6),
        "chapter_break":   True,
        "mirror_margins":  True,
        "header_footer":   True,
        "toc":             True,
    },

    # ── KDP Print 5.5×8.5 (intermédiaire) ─────────
    "print-55x85": {
        "page_width":      Inches(5.5),
        "page_height":     Inches(8.5),
        "margin_top":      Inches(1.0),
        "margin_bottom":   Inches(1.0),
        "margin_left":     Inches(1.0),
        "margin_right":    Inches(0.75),
        "font_body":       "Garamond",
        "size_body":       Pt(11),
        "size_h1":         Pt(22),
        "size_h2":         Pt(15),
        "size_h3":         Pt(12.5),
        "size_h4":         Pt(11),
        "size_quote":      Pt(10),
        "size_caption":    Pt(9),
        "line_spacing":    1.3,
        "space_before_h1": Pt(32),
        "space_after_h1":  Pt(16),
        "space_before_h2": Pt(20),
        "space_after_h2":  Pt(8),
        "space_after_para": Pt(0),
        "first_line_indent": Cm(0.65),
        "chapter_break":   True,
        "mirror_margins":  True,
        "header_footer":   True,
        "toc":             True,
    },
}

MODE   = "<MODE_CHOISI>"    # "ebook", "print-6x9", "print-5x8", "print-55x85"
TITLE  = "<TITRE_LIVRE>"    # ex: "PEACE, WE CAN AVOID IT"
AUTHOR = "<AUTEUR>"         # ex: "BEN-H2O"

cfg = CONFIGS[MODE]

# ── Utilitaires ────────────────────────────────────────────
def get_rgb(run):
    try:
        rgb = run.font.color.rgb
        return (rgb[0], rgb[1], rgb[2]) if rgb else None
    except:
        return None

def is_heading(para):
    """Détecte si un paragraphe est un titre (gras + grande taille)."""
    if not para.runs:
        return False, 0
    run = para.runs[0]
    try:
        size = run.font.size
        bold = run.bold
        if bold and size:
            pt = size.pt
            if pt >= 20:  return True, 1
            if pt >= 14:  return True, 2
            if pt >= 12:  return True, 3
            if pt >= 11:  return True, 4
        elif bold and not size:
            # taille héritée — traiter comme H2
            return True, 2
    except:
        pass
    return False, 0

def set_line_spacing(para, spacing_factor):
    pf = para.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = spacing_factor

def add_page_break_before(para):
    """Ajoute un saut de page avant le paragraphe via XML."""
    pPr = para._p.get_or_add_pPr()
    pb = OxmlElement('w:pageBreakBefore')
    pb.set(qn('w:val'), '1')
    pPr.append(pb)

def remove_page_break_before(para):
    pPr = para._p.get_or_add_pPr()
    for pb in pPr.findall(qn('w:pageBreakBefore')):
        pPr.remove(pb)

def add_header_footer(doc, title, author):
    """Ajoute numéros de page en en-tête (pages paires = titre, impaires = auteur)."""
    from docx.oxml.ns import nsmap
    section = doc.sections[0]
    section.different_first_page_header_footer = True
    section.header_distance = Inches(0.5)
    section.footer_distance = Inches(0.5)

    # Header page gauche (paire) — titre du livre
    header_even = section.even_page_header
    p_even = header_even.paragraphs[0] if header_even.paragraphs else header_even.add_paragraph()
    p_even.clear()
    p_even.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p_even.add_run(title.upper())
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

    # Header page droite (impaire) — auteur
    header_odd = section.header
    p_odd = header_odd.paragraphs[0] if header_odd.paragraphs else header_odd.add_paragraph()
    p_odd.clear()
    p_odd.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p_odd.add_run(author)
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

# ── Ouvrir et calibrer ─────────────────────────────────────
doc = Document(SRC)

# 1. Page et marges
for section in doc.sections:
    if cfg["page_width"]:
        section.page_width  = cfg["page_width"]
        section.page_height = cfg["page_height"]
    section.top_margin    = cfg["margin_top"]
    section.bottom_margin = cfg["margin_bottom"]
    section.left_margin   = cfg["margin_left"]
    section.right_margin  = cfg["margin_right"]
    if cfg["mirror_margins"]:
        # Activer marges miroir via XML
        sectPr = section._sectPr
        pgMar = sectPr.find(qn('w:pgMar'))
        if pgMar is not None:
            pgMar.set(qn('w:mirrorMargins'), '1')

# 2. Typographie paragraphe par paragraphe
for para in doc.paragraphs:
    is_hdg, level = is_heading(para)
    pf = para.paragraph_format

    if is_hdg:
        # Titres
        size_map = {1: cfg["size_h1"], 2: cfg["size_h2"],
                    3: cfg["size_h3"], 4: cfg["size_h4"]}
        target_size = size_map.get(level, cfg["size_h2"])

        for run in para.runs:
            run.font.size = target_size
            if not run.font.name or run.font.name in ("", "Calibri", "Arial", "Times New Roman"):
                pass  # conserver la police des titres si elle est stylistique

        # Espacement
        if level == 1:
            pf.space_before = cfg["space_before_h1"]
            pf.space_after  = cfg["space_after_h1"]
            pf.first_line_indent = Pt(0)
            if cfg["chapter_break"] and para.text.strip():
                add_page_break_before(para)
        elif level == 2:
            pf.space_before = cfg["space_before_h2"]
            pf.space_after  = cfg["space_after_h2"]
            pf.first_line_indent = Pt(0)
            remove_page_break_before(para)
        else:
            pf.space_before = Pt(10)
            pf.space_after  = Pt(6)
            pf.first_line_indent = Pt(0)

        set_line_spacing(para, 1.15)

    else:
        # Corps de texte
        if not para.text.strip():
            # Paragraphe vide → réduire l'espace (Kindle aplatit les vides)
            pf.space_before = Pt(0)
            pf.space_after  = Pt(0)
            continue

        for run in para.runs:
            if run.font.size and run.font.size.pt > 0:
                # Conserver les tailles stylistiques (citations, notes)
                if run.font.size.pt > cfg["size_body"].pt + 2:
                    pass  # titre non détecté, laisser tel quel
                elif run.font.size.pt < cfg["size_body"].pt - 2:
                    run.font.size = cfg["size_quote"]  # petite taille = caption/note
                else:
                    run.font.size = cfg["size_body"]
            else:
                run.font.size = cfg["size_body"]

            # Police corps
            if not run.font.name or run.font.name in ("Calibri", "Arial"):
                run.font.name = cfg["font_body"]

        pf.space_before = Pt(0)
        pf.space_after  = cfg["space_after_para"]
        # Indentation première ligne sauf après titre
        pf.first_line_indent = cfg["first_line_indent"]
        set_line_spacing(para, cfg["line_spacing"])

# 3. Tableaux — taille de police et espacement
for table in doc.tables:
    for row_idx, row in enumerate(table.rows):
        for cell in row.cells:
            for para in cell.paragraphs:
                for run in para.runs:
                    if not run.font.size or run.font.size.pt > cfg["size_body"].pt:
                        if row_idx == 0:
                            run.font.size = Pt(cfg["size_body"].pt - 0.5)
                        else:
                            run.font.size = cfg["size_body"]

# 4. En-tête / pied de page (mode print uniquement)
if cfg["header_footer"]:
    add_header_footer(doc, TITLE, AUTHOR)

doc.save(DST)
print(f"Format '{MODE}' appliqué → {DST}")
```

### Étape 3 — Vérifier la conformité KDP

```python
from docx import Document
from docx.shared import Inches, Pt

doc = Document("<FICHIER_DESTINATION>")
section = doc.sections[0]

print("=== CONFORMITÉ KDP ===")

# Page
w = section.page_width.inches
h = section.page_height.inches
print(f"\nPage : {w:.2f}\" x {h:.2f}\"")
if abs(w - 6) < 0.1 and abs(h - 9) < 0.1:
    print("  ✓ 6×9 conforme KDP")
elif abs(w - 5) < 0.1 and abs(h - 8) < 0.1:
    print("  ✓ 5×8 conforme KDP")
else:
    print("  ⚠ Vérifier les dimensions")

# Marges
print(f"\nMarges :")
print(f"  Haut    : {section.top_margin.cm:.2f} cm")
print(f"  Bas     : {section.bottom_margin.cm:.2f} cm")
print(f"  Gauche  : {section.left_margin.cm:.2f} cm (intérieur)")
print(f"  Droite  : {section.right_margin.cm:.2f} cm (extérieur)")
if section.top_margin.cm >= 2.0:
    print("  ✓ Marges conformes")
else:
    print("  ⚠ Marges trop petites (KDP min: 0.5\")")

# Chapitres avec sauts de page
chapter_breaks = 0
for p in doc.paragraphs:
    pPr = p._p.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr')
    if pPr is not None:
        pb = pPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pageBreakBefore')
        if pb is not None:
            chapter_breaks += 1

print(f"\nSauts de page : {chapter_breaks} chapitres")
if chapter_breaks > 0:
    print("  ✓ Sauts de page présents")
else:
    print("  ⚠ Aucun saut de page — vérifier la détection des titres")

# Tailles de police
sizes = {}
for p in doc.paragraphs:
    for run in p.runs:
        try:
            s = run.font.size
            if s:
                key = f"{s.pt:.0f}pt"
                sizes[key] = sizes.get(key, 0) + 1
        except:
            pass
print(f"\nTailles de police :")
for sz, n in sorted(sizes.items(), key=lambda x: -x[1])[:6]:
    print(f"  {sz}: {n} runs")

print(f"\nTableaux : {len(doc.tables)}")
print(f"Paragraphes : {len(doc.paragraphs)}")
print("\n✓ Document prêt pour upload KDP")
```

### Étape 4 — Checklist avant upload KDP

```bash
# Vérifier que le fichier est valide
python3 -c "
from docx import Document
doc = Document('<FICHIER_DESTINATION>')
print('OK — fichier valide')
print(f'  {len(doc.paragraphs)} paragraphes, {len(doc.tables)} tableaux')
"

echo "CHECKLIST KDP PRINT :"
echo "  [ ] Couverture séparée (format PDF, 300dpi, RGB)"
echo "  [ ] ISBN saisi dans KDP si disponible"
echo "  [ ] Catégorie BISAC choisie"
echo "  [ ] Prix fixé"
echo "  [ ] Prévisualiser dans KDP Previewer avant publication"
echo ""
echo "CHECKLIST KDP EBOOK :"
echo "  [ ] Table des matières avec liens hypertexte"
echo "  [ ] Pas de fond de couleur sur le texte"
echo "  [ ] Images en JPEG < 5MB chacune"
echo "  [ ] Tester sur Kindle Previewer 3"
```

---

## Spécifications de référence KDP

### Format recommandé selon le type de livre

| Type | Format recommandé | Raison |
|---|---|---|
| Essai géopolitique | `print-6x9` | Standard non-fiction US/international |
| Roman / récit | `print-5x8` | Format poche classique |
| Manuel académique | `print-55x85` | Format académique standard |
| Diffusion numérique | `ebook` | Liseuses, tablettes, mobile |

### Règles KDP critiques

**Ebook :**
- Pas de fond de couleur sur le texte (`background-color` bloque l'affichage sur Paperwhite)
- Pas de tailles de police inférieures à 9pt
- Pas d'en-têtes/pieds de page fixes (le lecteur Kindle les ignore)
- Tableaux : éviter les cellules fusionnées complexes

**Print :**
- Marge intérieure (gouttière) ≥ 1" pour un livre de 300+ pages
- Ne pas dépasser 828 pages (limite KDP print)
- Zone de sécurité : laisser 0.25" sans texte aux bords pour l'impression
- Police minimum recommandée : 9pt pour les notes, 11pt pour le corps

### Tailles de page KDP disponibles

```
4.25 x 6.87"  |  5.06 x 7.81"  |  5 x 8"
5.5 x 8.5"    |  6 x 9" ★      |  6.14 x 9.21"
6.69 x 9.61"  |  7 x 10"       |  7.44 x 9.69"
8 x 10"       |  8.5 x 11"
```
★ = 6×9 recommandé pour non-fiction/géopolitique

---

## Notes

- La détection des titres (fonction `is_heading`) est basée sur **gras + taille de police**. Si votre document utilise uniquement des styles Word (Heading 1, 2...) sans formatage inline, adapter la détection via `para.style.name`.
- Le mode `ebook` ne définit pas de taille de page fixe — Kindle gère le recadrage automatiquement.
- Pour les livres très longs (300+ pages), augmenter la marge intérieure à **1.25"** en `print-6x9`.
- La police `Garamond` est la plus professionnelle pour l'impression KDP. Si elle n'est pas disponible sur la machine, utiliser `Georgia` (toujours disponible, optimisée pour l'écran et l'impression).
