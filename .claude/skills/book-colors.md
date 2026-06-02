# book-colors

Applique une palette de couleurs professionnelle à un livre `.docx` sur la base des standards visuels des grandes publications géopolitiques mondiales.

## Usage

```
/book-colors <fichier.docx> [style]
```

**Styles disponibles :**

| Style | Inspiration | Couleur dominante |
|---|---|---|
| `cfr` | Council on Foreign Relations / Foreign Affairs | Bleu navy + or + bordeaux |
| `rand` | RAND Corporation / Brookings Institution | Navy profond + rouge vif |
| `diplomat` | The Diplomat / Foreign Policy Magazine | Indigo + ambre |
| `le-monde` | Le Monde Diplomatique / IRIS / IFRI | Noir-navy + rouge sang |
| `military` | IISS / Jane's / Military Review | Or militaire + olive foncé |
| `icj` | ONU / CIJ / Rapports internationaux | Bleu ONU |

**Exemples :**
```
/book-colors mon-livre.docx cfr
/book-colors mon-livre.docx rand
/book-colors mon-livre.docx le-monde
```

Si aucun style n'est précisé, utiliser `cfr` par défaut (le plus courant en géopolitique anglophone) ou demander à l'utilisateur.

---

## Instructions complètes

### Étape 0 — Vérifier les dépendances

```bash
python3 -c "import docx; print('ok')" 2>/dev/null || pip3 install python-docx -q
```

### Étape 1 — Analyser les couleurs existantes du document

Avant d'appliquer, toujours inspecter les couleurs actuelles pour construire le mapping :

```python
from docx import Document

doc = Document("<FICHIER_SOURCE>")

colors_found = {}
for p in doc.paragraphs:
    for run in p.runs:
        try:
            if run.font.color.type is not None:
                c = str(run.font.color.rgb)
                if c not in colors_found:
                    colors_found[c] = {"count": 0, "bold": run.bold, "sample": run.text[:40]}
                colors_found[c]["count"] += 1
        except:
            pass

for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for run in p.runs:
                    try:
                        if run.font.color.type is not None:
                            c = str(run.font.color.rgb)
                            if c not in colors_found:
                                colors_found[c] = {"count": 0, "bold": run.bold, "sample": run.text[:40]}
                            colors_found[c]["count"] += 1
                    except:
                        pass

print("Couleurs détectées :")
for col, info in sorted(colors_found.items(), key=lambda x: -x[1]["count"]):
    print(f"  #{col} ({info['count']} uses, bold={info['bold']}) — ex: {info['sample']!r}")
```

### Étape 2 — Appliquer la palette

Choisir la palette selon le style demandé, puis exécuter :

```python
from docx import Document
from docx.shared import RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = "<FICHIER_SOURCE>"
DST = "<FICHIER_DESTINATION>"

# ══════════════════════════════════════════════════
# PALETTES GÉOPOLITIQUES DE RÉFÉRENCE
# ══════════════════════════════════════════════════

PALETTES = {

    # ── CFR / Foreign Affairs ──────────────────────
    # Council on Foreign Relations, Foreign Affairs Magazine
    # Standard dominant en géopolitique anglophone
    "cfr": {
        "heading":     RGBColor(0x1B, 0x3A, 0x6B),  # bleu navy profond
        "body":        None,                          # corps de texte : héritage
        "quote":       RGBColor(0x8B, 0x1A, 0x1A),  # bordeaux sombre
        "secondary":   RGBColor(0x5A, 0x6A, 0x7A),  # gris acier
        "accent":      RGBColor(0xC8, 0xA0, 0x00),  # or ambre
        "table_hdr_bg": "1B3A6B",                    # fond navy
        "table_hdr_txt": RGBColor(0xFF, 0xFF, 0xFF), # texte blanc
    },

    # ── RAND / Brookings ──────────────────────────
    # RAND Corporation, Brookings Institution
    # Think tanks américains, rapports stratégiques
    "rand": {
        "heading":     RGBColor(0x00, 0x33, 0x66),  # navy intense
        "body":        None,
        "quote":       RGBColor(0xCC, 0x33, 0x00),  # rouge-orange vif
        "secondary":   RGBColor(0x66, 0x66, 0x66),  # gris neutre
        "accent":      RGBColor(0x33, 0x66, 0x99),  # bleu moyen
        "table_hdr_bg": "003366",
        "table_hdr_txt": RGBColor(0xFF, 0xFF, 0xFF),
    },

    # ── The Diplomat / Foreign Policy ─────────────
    # The Diplomat, Foreign Policy Magazine
    # Presse géopolitique internationale
    "diplomat": {
        "heading":     RGBColor(0x2C, 0x3E, 0x6B),  # indigo navy
        "body":        None,
        "quote":       RGBColor(0x7A, 0x3A, 0x00),  # brun-ambre sombre
        "secondary":   RGBColor(0x6B, 0x6B, 0x6B),  # gris moyen
        "accent":      RGBColor(0xC8, 0x78, 0x00),  # ambre profond
        "table_hdr_bg": "2C3E6B",
        "table_hdr_txt": RGBColor(0xF5, 0xE6, 0xC8), # crème chaud
    },

    # ── Le Monde Diplomatique / IFRI / IRIS ───────
    # Le Monde Diplomatique, Institut Français des
    # Relations Internationales, géopolitique française
    "le-monde": {
        "heading":     RGBColor(0x1A, 0x1A, 0x2E),  # noir-navy très foncé
        "body":        None,
        "quote":       RGBColor(0x8B, 0x00, 0x00),  # rouge sang
        "secondary":   RGBColor(0x55, 0x55, 0x55),  # gris foncé
        "accent":      RGBColor(0xA0, 0x52, 0x2D),  # brun sienna
        "table_hdr_bg": "1A1A2E",
        "table_hdr_txt": RGBColor(0xE8, 0xE0, 0xD0), # blanc cassé chaud
    },

    # ── Military / Strategic Studies ──────────────
    # IISS, Jane's Intelligence, Military Review
    # Revues stratégiques et militaires
    "military": {
        "heading":     RGBColor(0xC8, 0x96, 0x0A),  # or militaire
        "body":        None,
        "quote":       RGBColor(0x9A, 0x78, 0x20),  # or profond
        "secondary":   RGBColor(0x7A, 0x65, 0x35),  # gris doré
        "accent":      RGBColor(0x4A, 0x38, 0x10),  # olive foncé
        "table_hdr_bg": "1E2010",                    # noir olive
        "table_hdr_txt": RGBColor(0xC8, 0x96, 0x0A), # or
    },

    # ── ONU / CIJ / Rapports internationaux ───────
    # Nations Unies, Cour Internationale de Justice
    # Documents officiels multilatéraux
    "icj": {
        "heading":     RGBColor(0x00, 0x5C, 0x97),  # bleu ONU
        "body":        None,
        "quote":       RGBColor(0x00, 0x66, 0x00),  # vert ONU
        "secondary":   RGBColor(0x4A, 0x6A, 0x8A),  # bleu-gris
        "accent":      RGBColor(0x00, 0x3D, 0x6B),  # bleu ONU foncé
        "table_hdr_bg": "005C97",
        "table_hdr_txt": RGBColor(0xFF, 0xFF, 0xFF),
    },
}

# ══════════════════════════════════════════════════
# MAPPING — adapter selon les couleurs détectées
# à l'Étape 1. Ces valeurs correspondent au livre
# "La Paix, on peut l'éviter" (AES).
# Pour un autre livre, relancer l'Étape 1 et ajuster.
# ══════════════════════════════════════════════════

STYLE = "<STYLE_CHOISI>"   # ex: "cfr", "rand", "le-monde"...
palette = PALETTES[STYLE]

def get_rgb(run):
    try:
        rgb = run.font.color.rgb
        return (rgb[0], rgb[1], rgb[2]) if rgb else None
    except:
        return None

def apply_palette(run, palette):
    """
    Règles de mapping universelles :
    - Texte gras + grande taille → heading (titre)
    - Texte en couleur vive (rouge, bordeaux) → quote (citation)
    - Texte gris neutre → secondary (attribution, note)
    - Texte bleu/vert/couleur → accent
    - Corps de texte (non gras, noir/très foncé) → body (inchangé)
    """
    c = get_rgb(run)
    if c is None:
        return

    r, g, b = c

    # Noir / très foncé + gras = titre/heading
    if (r < 40 and g < 40 and b < 40) and run.bold:
        if palette["heading"]:
            run.font.color.rgb = palette["heading"]
        return

    # Noir / très foncé + non gras = corps → ne pas toucher
    if r < 40 and g < 40 and b < 40:
        return

    # Rouge / bordeaux / brun-rouge → citations
    if r > 100 and g < 60 and b < 60:
        if palette["quote"]:
            run.font.color.rgb = palette["quote"]
        return

    # Or / ambre / jaune (ex: #C8A951, #C8960A) → heading
    if r > 150 and g > 100 and b < 80 and r > g:
        if palette["heading"]:
            run.font.color.rgb = palette["heading"]
        return

    # Gris neutre (r≈g≈b, moyennement foncé) → secondary
    if abs(r-g) < 20 and abs(g-b) < 20 and 40 < r < 180:
        if palette["secondary"]:
            run.font.color.rgb = palette["secondary"]
        return

    # Bleu → accent ou heading
    if b > r and b > g and b > 80:
        if palette["accent"]:
            run.font.color.rgb = palette["accent"]
        return

    # Vert → accent
    if g > r and g > b and g > 80:
        if palette["accent"]:
            run.font.color.rgb = palette["accent"]
        return

def set_cell_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    for old in tcPr.findall(qn('w:shd')):
        tcPr.remove(old)
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

# ── Appliquer ──────────────────────────────────────
doc = Document(SRC)

# Paragraphes
for para in doc.paragraphs:
    for run in para.runs:
        apply_palette(run, palette)

# Tableaux
processed = set()
for table in doc.tables:
    for row_idx, row in enumerate(table.rows):
        is_header = (row_idx == 0)
        for cell in row.cells:
            cid = id(cell._tc)
            if cid in processed:
                continue
            processed.add(cid)
            for para in cell.paragraphs:
                for run in para.runs:
                    if is_header and palette["table_hdr_txt"]:
                        # En-tête : forcer la couleur du texte
                        try:
                            run.font.color.rgb = palette["table_hdr_txt"]
                        except:
                            pass
                    else:
                        apply_palette(run, palette)
            if is_header:
                set_cell_bg(cell, palette["table_hdr_bg"])

doc.save(DST)
print(f"Palette '{STYLE}' appliquée → {DST}")
```

### Étape 3 — Vérifier le résultat

```python
from docx import Document

doc = Document("<FICHIER_DESTINATION>")
colors = {}
for p in doc.paragraphs:
    for run in p.runs:
        try:
            if run.font.color.type:
                c = str(run.font.color.rgb)
                colors[c] = colors.get(c, 0) + 1
        except:
            pass

print(f"Style appliqué : <STYLE_CHOISI>")
print("Couleurs dans le document final :")
for col, n in sorted(colors.items(), key=lambda x: -x[1]):
    print(f"  #{col}: {n} utilisations")
```

---

## Référence visuelle des palettes

### `cfr` — Council on Foreign Relations
```
Titres   ████  #1B3A6B  Bleu navy
Corps    ████  #1A1A1A  Noir
Citations ████  #8B1A1A  Bordeaux sombre
Notes    ████  #5A6A7A  Gris acier
Accent   ████  #C8A000  Or ambre
Headers  ████  #1B3A6B  fond navy / texte blanc
```

### `rand` — RAND / Brookings
```
Titres   ████  #003366  Navy intense
Corps    ████  #1A1A1A  Noir
Citations ████  #CC3300  Rouge-orange
Notes    ████  #666666  Gris neutre
Accent   ████  #336699  Bleu moyen
Headers  ████  #003366  fond navy / texte blanc
```

### `diplomat` — The Diplomat / Foreign Policy
```
Titres   ████  #2C3E6B  Indigo
Corps    ████  #1A1A1A  Noir
Citations ████  #7A3A00  Brun ambre
Notes    ████  #6B6B6B  Gris
Accent   ████  #C87800  Ambre
Headers  ████  #2C3E6B  fond indigo / texte crème
```

### `le-monde` — Le Monde Diplomatique / IFRI
```
Titres   ████  #1A1A2E  Noir-navy
Corps    ████  #1A1A1A  Noir
Citations ████  #8B0000  Rouge sang
Notes    ████  #555555  Gris foncé
Accent   ████  #A0522D  Sienna
Headers  ████  #1A1A2E  fond très foncé / texte blanc cassé
```

### `military` — IISS / Jane's / Military Review
```
Titres   ████  #C8960A  Or militaire
Corps    ████  #1A1A1A  Noir
Citations ████  #9A7820  Or profond
Notes    ████  #7A6535  Gris doré
Accent   ████  #4A3810  Olive foncé
Headers  ████  #1E2010  fond olive noir / texte or
```

### `icj` — ONU / CIJ / Rapports internationaux
```
Titres   ████  #005C97  Bleu ONU
Corps    ████  #1A1A1A  Noir
Citations ████  #006600  Vert ONU
Notes    ████  #4A6A8A  Bleu-gris
Accent   ████  #003D6B  Bleu ONU foncé
Headers  ████  #005C97  fond bleu ONU / texte blanc
```

---

## Notes

- Le **corps de texte** (non gras, couleur très foncée) n'est jamais retouché — la lisibilité prime.
- La logique de détection dans `apply_palette()` est **universelle** : elle fonctionne sur n'importe quel `.docx` avec des couleurs explicites.
- Pour un livre sans couleurs explicites (tout noir par défaut), appliquer d'abord `/book-colors` avec inspection de l'Étape 1, puis définir manuellement les couleurs-source dans le mapping.
- Le style `cfr` est le standard le plus utilisé en géopolitique anglophone et internationale.
- Le style `le-monde` est le plus adapté aux publications francophones de géopolitique critique.
