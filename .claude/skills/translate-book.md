# translate-book

Traduit un livre `.docx` entier dans une autre langue en préservant toute la mise en forme (couleurs, gras, italique, tailles de police, tableaux, alignement).

## Usage

```
/translate-book <fichier.docx> <langue-cible>
```

**Exemples :**
```
/translate-book mon-livre.docx "English (US)"
/translate-book mon-livre.docx "Espagnol"
/translate-book mon-livre.docx "Portugais brésilien"
```

Si aucun argument n'est fourni, demande le fichier et la langue cible.

---

## Instructions complètes

### Étape 0 — Vérifier les dépendances

```bash
python3 -c "import docx; print('ok')" 2>/dev/null || pip3 install python-docx -q
```

### Étape 1 — Extraire les métadonnées du document

Lancer ce script Python pour extraire paragraphes + tableaux avec toutes les métadonnées de formatage :

```python
from docx import Document
import json

doc = Document("<FICHIER_SOURCE>")

# Paragraphes
para_data = []
for i, p in enumerate(doc.paragraphs):
    runs_info = []
    for run in p.runs:
        try:
            color = str(run.font.color.rgb) if run.font.color.type else None
        except:
            color = None
        runs_info.append({
            "text": run.text,
            "bold": run.bold,
            "italic": run.italic,
            "color": color,
            "size": str(run.font.size),
        })
    para_data.append({
        "idx": i,
        "full_text": p.text,
        "align": str(p.alignment),
        "style": p.style.name,
        "runs": runs_info,
    })

# Tableaux
table_data = []
for table in doc.tables:
    tbl = []
    for row in table.rows:
        rw = []
        for cell in row.cells:
            cell_paras = []
            for p in cell.paragraphs:
                runs_info = []
                for run in p.runs:
                    try:
                        color = str(run.font.color.rgb) if run.font.color.type else None
                    except:
                        color = None
                    runs_info.append({
                        "text": run.text,
                        "bold": run.bold,
                        "italic": run.italic,
                        "color": color,
                        "size": str(run.font.size),
                    })
                cell_paras.append({"full_text": p.text, "runs": runs_info, "align": str(p.alignment)})
            rw.append(cell_paras)
        tbl.append(rw)
    table_data.append(tbl)

with open("/tmp/book_para_data.json", "w", encoding="utf-8") as f:
    json.dump(para_data, f, ensure_ascii=False, indent=2, default=str)
with open("/tmp/book_table_data.json", "w", encoding="utf-8") as f:
    json.dump(table_data, f, ensure_ascii=False, indent=2, default=str)

print(f"{len(para_data)} paragraphes, {len(table_data)} tableaux extraits.")
```

### Étape 2 — Traduire les paragraphes par lots

Utiliser `claude -p` en lots de **15 paragraphes** max pour éviter les timeouts. Sauvegarder la progression après chaque lot.

```python
import subprocess, json, os, time

with open("/tmp/book_para_data.json", encoding="utf-8") as f:
    para_data = json.load(f)

texts = [p["full_text"] for p in para_data]

PROGRESS_FILE = "/tmp/translation_progress.json"
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, encoding="utf-8") as f:
        translated_paras = json.load(f)
    start_idx = len(translated_paras)
    print(f"Reprise depuis le paragraphe {start_idx}")
else:
    translated_paras = []
    start_idx = 0

SYSTEM = (
    "Translate from <LANGUE_SOURCE> to <LANGUE_CIBLE>. Rules: "
    "keep §§§ as delimiter between paragraphs; "
    "preserve all proper nouns, names, organizations; "
    "<REGLES_SPECIFIQUES_LANGUE>; "
    "return ONLY the translated text with §§§ delimiters, no comments."
)

def translate_batch(batch_texts, timeout=300):
    non_empty = [t for t in batch_texts if t.strip()]
    if not non_empty:
        return batch_texts
    joined = "\n§§§\n".join(batch_texts)
    r = subprocess.run(
        ["claude", "-p", f"{SYSTEM}\n\n{joined}"],
        capture_output=True, text=True, timeout=timeout
    )
    if r.returncode != 0 or not r.stdout.strip():
        return batch_texts
    parts = [p.strip() for p in r.stdout.strip().split("§§§")]
    if len(parts) >= len(batch_texts):
        return parts[:len(batch_texts)]
    parts += batch_texts[len(parts):]
    return parts

BATCH_SIZE = 15
total_batches = (len(texts) - start_idx + BATCH_SIZE - 1) // BATCH_SIZE

for i in range(start_idx, len(texts), BATCH_SIZE):
    batch = texts[i:i+BATCH_SIZE]
    b_num = (i - start_idx) // BATCH_SIZE + 1
    print(f"  Lot {b_num}/{total_batches} (paras {i}-{i+len(batch)-1})...", end=" ", flush=True)
    result = translate_batch(batch)
    translated_paras.extend(result)
    # Sauvegarde progressive
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(translated_paras, f, ensure_ascii=False)
    print(f"ok ({len(translated_paras)}/{len(texts)})", flush=True)
    time.sleep(0.2)

with open("/tmp/translated_paras.json", "w", encoding="utf-8") as f:
    json.dump(translated_paras, f, ensure_ascii=False, indent=2)

print(f"\nParagraphes : {len(translated_paras)}/{len(texts)}")
```

> **Si un lot dépasse 300s :** réduire `BATCH_SIZE` à 5 et relancer — le fichier de progression permet de reprendre sans tout recommencer.

### Étape 3 — Traduire les tableaux

```python
import subprocess, json, time

with open("/tmp/book_table_data.json", encoding="utf-8") as f:
    table_data = json.load(f)

SYSTEM = (
    "Translate from <LANGUE_SOURCE> to <LANGUE_CIBLE>. "
    "Keep §§§ delimiters. Preserve proper nouns. "
    "Return ONLY translated text with §§§, no comments."
)

def translate_batch(batch_texts, timeout=180):
    non_empty = [t for t in batch_texts if t.strip()]
    if not non_empty:
        return batch_texts
    joined = "\n§§§\n".join(batch_texts)
    r = subprocess.run(["claude", "-p", f"{SYSTEM}\n\n{joined}"],
                       capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0 or not r.stdout.strip():
        return batch_texts
    parts = [p.strip() for p in r.stdout.strip().split("§§§")]
    if len(parts) >= len(batch_texts):
        return parts[:len(batch_texts)]
    parts += batch_texts[len(parts):]
    return parts

translated_tables = []
for t_idx, tbl in enumerate(table_data):
    print(f"  Tableau {t_idx+1}/{len(table_data)}...", end=" ", flush=True)
    translated_tbl = []
    for row in tbl:
        translated_row = []
        for cell_paras in row:
            cell_texts = [cp["full_text"] for cp in cell_paras]
            translated_row.append(translate_batch(cell_texts) if any(t.strip() for t in cell_texts) else cell_texts)
        translated_tbl.append(translated_row)
    translated_tables.append(translated_tbl)
    print("ok", flush=True)
    time.sleep(0.2)

with open("/tmp/translated_tables.json", "w", encoding="utf-8") as f:
    json.dump(translated_tables, f, ensure_ascii=False, indent=2)

print(f"\nTableaux traduits : {len(translated_tables)}")
```

### Étape 4 — Reconstruire le document traduit

Ouvrir le document source, remplacer le texte de chaque run en conservant le formatage original, puis appliquer la palette de couleurs de la couverture.

```python
from docx import Document
from docx.shared import RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import json

SRC = "<FICHIER_SOURCE>"
DST = "<FICHIER_DESTINATION>"

with open("/tmp/book_para_data.json", encoding="utf-8") as f:
    para_data = json.load(f)
with open("/tmp/translated_paras.json", encoding="utf-8") as f:
    translated_paras = json.load(f)
with open("/tmp/book_table_data.json", encoding="utf-8") as f:
    table_data = json.load(f)
with open("/tmp/translated_tables.json", encoding="utf-8") as f:
    translated_tables = json.load(f)

# Palette couleurs (à adapter selon la couverture du livre)
GOLD       = RGBColor(0xC8, 0x96, 0x0A)  # titres principaux
GOLD_QUOTE = RGBColor(0x9A, 0x78, 0x20)  # citations
GOLD_GRAY  = RGBColor(0x7A, 0x65, 0x35)  # textes secondaires
DARK_AMBER = RGBColor(0x4A, 0x38, 0x10)  # sous-titres
NEAR_BLACK = RGBColor(0x1A, 0x1A, 0x0A)  # quasi-noir
TABLE_HDR_BG = "1E2010"                  # fond en-têtes tableaux

def map_color(rgb_str, is_bold):
    """Mappe la couleur originale vers la palette couverture."""
    if rgb_str is None:
        return None
    c = rgb_str.upper()
    if c == "1A1A1A": return GOLD if is_bold else None
    if c == "000000": return NEAR_BLACK
    if c in ("C8A951", "C8960A"): return GOLD
    if c == "8B1A1A": return GOLD_QUOTE
    if c == "888888": return GOLD_GRAY
    if c == "1C2340": return DARK_AMBER
    if c in ("2E74B5", "2D6A4F"): return GOLD
    return None

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

doc = Document(SRC)

# Paragraphes
for i, (para, trans_text) in enumerate(zip(doc.paragraphs, translated_paras)):
    orig_runs = para_data[i]["runs"]
    for run in para.runs:
        run.text = ""
    if not para.runs:
        run = para.add_run(trans_text)
    else:
        para.runs[0].text = trans_text
        for run in para.runs[1:]:
            run.text = ""
        run = para.runs[0]
    if orig_runs:
        is_bold = orig_runs[0].get("bold") or False
        new_color = map_color(orig_runs[0].get("color"), is_bold)
        if new_color:
            try:
                run.font.color.rgb = new_color
            except:
                pass

# Tableaux
processed = set()
for table, trans_tbl, orig_tbl in zip(doc.tables, translated_tables, table_data):
    for row_idx, (row, trans_row, orig_row) in enumerate(zip(table.rows, trans_tbl, orig_tbl)):
        is_header = (row_idx == 0)
        for cell, trans_texts, orig_cell_paras in zip(row.cells, trans_row, orig_row):
            cell_id = id(cell._tc)
            if cell_id in processed:
                continue
            processed.add(cell_id)
            for p_idx, (para, trans_text) in enumerate(zip(cell.paragraphs, trans_texts)):
                if not para.runs:
                    para.add_run(trans_text)
                else:
                    para.runs[0].text = trans_text
                    for r in para.runs[1:]:
                        r.text = ""
                    if p_idx < len(orig_cell_paras) and orig_cell_paras[p_idx]["runs"]:
                        orig_run = orig_cell_paras[p_idx]["runs"][0]
                        new_color = map_color(orig_run.get("color"), orig_run.get("bold") or False)
                        if new_color:
                            try:
                                para.runs[0].font.color.rgb = new_color
                            except:
                                pass
            if is_header:
                set_cell_bg(cell, TABLE_HDR_BG)

doc.save(DST)
print(f"Document sauvegardé : {DST}")
```

### Étape 5 — Nettoyer et vérifier

```bash
# Vérifier que le fichier est valide
python3 -c "
from docx import Document
doc = Document('<FICHIER_DESTINATION>')
print(f'OK — {len(doc.paragraphs)} paragraphes, {len(doc.tables)} tableaux')
# Échantillon
for p in doc.paragraphs[:5]:
    if p.text.strip():
        print(f'  {p.text[:80]!r}')
"

# Supprimer les fichiers temporaires
rm -f /tmp/book_para_data.json /tmp/book_table_data.json \
      /tmp/translated_paras.json /tmp/translated_tables.json \
      /tmp/translation_progress.json
```

---

## Notes importantes

### Règles de terminologie par langue

**Vers l'anglais (US) :**
```
CEDEAO→ECOWAS; franc CFA→CFA franc; US spelling (analyze, recognize, center, color)
```

**Vers l'espagnol :**
```
CEDEAO→CEDEAO; franc CFA→franco CFA; vosotros→ustedes (latinoaméricain)
```

**Vers le portugais brésilien :**
```
CEDEAO→CEDEAO; franc CFA→franco CFA; ortographe brésilienne (não européenne)
```

### Gestion des timeouts

- Si un lot dépasse le délai → réduire `BATCH_SIZE` à **5** et relancer
- Le fichier `/tmp/translation_progress.json` permet de reprendre sans recommencer
- Les paragraphes très longs (>2000 chars) peuvent nécessiter `timeout=600`

### Palette de couleurs

La palette `map_color()` est calibrée pour la couverture de **ce projet** :
- Titres `#1A1A1A` gras → or `#C8960A`
- Citations `#8B1A1A` bordeaux → ambre `#9A7820`  
- Secondaires `#888888` gris → gris doré `#7A6535`

Pour un autre livre, adapter les valeurs hex dans `map_color()` selon les couleurs de la couverture.
