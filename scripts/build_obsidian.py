#!/usr/bin/env python3
"""Génère un dossier-coffre Obsidian depuis les chapitres markdown.
Notes propres (titre lisible), frontmatter enrichi (tags, partie),
liens [[wikilink]] entre chapitres, et un Index (Map of Content)."""
import os, re, glob, shutil

SRC = "/home/user/tts-docs/content/3.livre"
OUT = "/home/user/tts-docs/obsidian-vault/La paix on peut l'eviter"

# Pages de partie (depuis build_pdf.py PART_PAGES) : num chapitre -> (label, titre)
PART_PAGES = {
    4:  ("Partie I",   "L'Afrique avant la domination"),
    8:  ("Partie II",  "Comment la dépendance a été organisée"),
    14: ("Partie III", "La guerre du Sahel"),
    19: ("Partie IV",  "La révolution de la souveraineté"),
    25: ("Partie V",   "Le réveil panafricain"),
    29: ("Partie VI",  "Les défis de demain"),
}

def slug_to_title(md_text, fallback):
    """Récupère le titre : frontmatter title > premier H1 > nom de fichier."""
    m = re.search(r'^title:\s*[\'"]?(.+?)[\'"]?\s*$', md_text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    h1 = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    if h1:
        return h1.group(1).strip()
    return fallback

def safe_filename(name):
    """Obsidian/OS-safe : retire les caractères interdits."""
    name = re.sub(r'[\\/:*?"<>|#\^\[\]]', '', name)
    return re.sub(r'\s+', ' ', name).strip()

def strip_frontmatter(md):
    if md.startswith('---'):
        parts = md.split('---', 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return md

# ── Préparation ────────────────────────────────────────────────────────────
if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)

files = sorted(glob.glob(os.path.join(SRC, "[0-9]*.md")),
               key=lambda x: int(os.path.basename(x).split('.')[0]))

notes = []        # (num, title, filename, partie_label)
current_part = ("Préliminaires", "")

for fp in files:
    num = int(os.path.basename(fp).split('.')[0])
    with open(fp, 'r', encoding='utf-8') as f:
        raw = f.read()
    if num in PART_PAGES:
        current_part = PART_PAGES[num]
    title = slug_to_title(raw, os.path.basename(fp))
    note_name = safe_filename(f"{num:02d} — {title}")[:90]
    notes.append((num, title, note_name, current_part[0], current_part[1]))

# ── Écriture des notes ─────────────────────────────────────────────────────
for idx, (num, title, note_name, part_label, part_title) in enumerate(notes):
    fp = files[idx]
    with open(fp, 'r', encoding='utf-8') as f:
        body = strip_frontmatter(f.read())
    # retire le premier H1 dupliqué (le titre de note suffit) — on le garde en fait
    prev_link = f"[[{notes[idx-1][2]}]]" if idx > 0 else "—"
    next_link = f"[[{notes[idx+1][2]}]]" if idx < len(notes)-1 else "—"
    tag_part = re.sub(r'[^a-zA-Z0-9]+', '-', part_label.lower()).strip('-')
    fm = (
        "---\n"
        f"title: \"{title}\"\n"
        f"chapitre: {num}\n"
        f"partie: \"{part_label} — {part_title}\"\n"
        f"tags: [livre/la-paix-on-peut-leviter, {tag_part}]\n"
        "---\n\n"
    )
    nav = f"> [[Index]] · ‹ {prev_link} · {next_link} ›\n\n"
    with open(os.path.join(OUT, note_name + ".md"), 'w', encoding='utf-8') as f:
        f.write(fm + nav + body + "\n")

# ── Index / Map of Content ─────────────────────────────────────────────────
lines = [
    "---",
    "title: \"La paix, on peut l'éviter — Index\"",
    "tags: [livre/la-paix-on-peut-leviter, index, moc]",
    "---", "",
    "# La paix, on peut l'éviter",
    "",
    "*De Berlin à l'Alliance des États du Sahel — anatomie d'une domination "
    "et d'une rupture.*",
    "",
    f"**{len(notes)} chapitres.** Carte de navigation du livre.",
    "",
]
last_part = None
for num, title, note_name, part_label, part_title in notes:
    key = (part_label, part_title)
    if key != last_part:
        head = part_label if not part_title else f"{part_label} — {part_title}"
        lines.append("")
        lines.append(f"## {head}")
        lines.append("")
        last_part = key
    lines.append(f"- [[{note_name}|{num:02d}. {title}]]")
lines.append("")
with open(os.path.join(OUT, "Index.md"), 'w', encoding='utf-8') as f:
    f.write("\n".join(lines))

print(f"Coffre généré : {OUT}")
print(f"  {len(notes)} notes de chapitre + Index.md")
