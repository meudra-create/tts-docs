#!/usr/bin/env python3
"""Ajoute ---ENCADRE---/---FIN--- autour de tous les blocs **TITRE MAJUSCULES** non encore balisés."""

import re
from pathlib import Path

SRC = Path("/home/user/tts-docs/manuscrit-edition/LIVRE-FINAL.md")
text = SRC.read_text(encoding="utf-8")
lines = text.split('\n')

result = []
i = 0
changes = 0

while i < len(lines):
    line = lines[i]

    # Skip already-marked blocks
    if line.strip() == '---ENCADRE---':
        result.append(line)
        i += 1
        while i < len(lines) and lines[i].strip() != '---FIN---':
            result.append(lines[i])
            i += 1
        if i < len(lines):
            result.append(lines[i])  # ---FIN---
        i += 1
        continue

    # Detect standalone **UPPERCASE TITLE** line
    m = re.match(r'^\*\*([A-ZÀÂÉÈÊËÎÏÔÙÛÜÆŒÇ0-9(«\-][^*]{5,})\*\*$', line.strip())
    if m:
        title_line = line
        # Collect content: blank line then bullets/content until double-blank or heading
        content_lines = []
        i += 1
        # Skip leading blank
        while i < len(lines) and not lines[i].strip():
            i += 1
        # Collect until end marker
        while i < len(lines):
            l = lines[i]
            s = l.strip()
            if (re.match(r'^#{1,6} ', l) or
                s == '---ENCADRE---' or
                s == '---FIN---' or
                re.match(r'^\*\*[A-ZÀÂÉÈÊËÎÏÔÙÛÜÆŒÇ0-9(«\-][^*]{5,}\*\*$', s)):
                break
            content_lines.append(l)
            i += 1
        # Strip trailing blanks from content
        while content_lines and not content_lines[-1].strip():
            content_lines.pop()

        # Only wrap if content contains at least one bullet
        has_bullets = any(l.strip().startswith('- ') for l in content_lines)
        if has_bullets:
            result.append('---ENCADRE---')
            result.append('')
            result.append(title_line)
            result.append('')
            result.extend(content_lines)
            result.append('')
            result.append('---FIN---')
            changes += 1
            print(f"  Balisé: {m.group(1)[:60]}")
        else:
            result.append(title_line)
            for cl in content_lines:
                result.append(cl)
        continue

    result.append(line)
    i += 1

SRC.write_text('\n'.join(result), encoding="utf-8")
print(f"\n{changes} blocs balisés.")
