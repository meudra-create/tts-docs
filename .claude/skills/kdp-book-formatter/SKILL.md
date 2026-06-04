---
name: kdp-book-formatter
description: >
  Formate un fichier DOCX selon les spécifications du livre
  "PEACE, WE CAN PREVENT IT" (BEN-H2O, 2026) pour impression KDP 6×9.
  Applique la mise en page, les polices, les couleurs, les encadrés stylisés,
  les marges miroir et les numéros de page.
  Invoke with: /kdp-book-formatter [input.docx] [output.docx]
---

# KDP Book Formatter Skill

## Usage

```
/kdp-book-formatter
/kdp-book-formatter input.docx
/kdp-book-formatter input.docx output.docx
```

When invoked, run `.claude/skills/kdp-book-formatter/kdp_formatter.py`
with the provided arguments (defaults: input = PEACE_KDP_FINAL.docx,
output = PEACE_KDP_PRINT.docx).

## What this skill does

1. **Page layout** — KDP 6×9", mirror margins (gutter 0.875", outside 0.625", top/bottom 0.75")
2. **Typography** — Garamond 11pt body, 1.15 line spacing, 6pt after paragraphs
3. **First-paragraph rule** — no indent after headings; 0.25" first-line indent elsewhere
4. **Styled callout tables** — dark navy (#1A1A2E) header / cream (#F5F5F0) body / gold (#C8A000) border
5. **Duplicate-title cleanup** — removes SubHeading paragraphs that duplicate a table header
6. **Running header** — book title, centred, 8pt, grey rule beneath
7. **Footer** — centred automatic page number
8. **Widow/orphan control** — every paragraph; headings keep-with-next
9. **Mirror margins flag** — applied via document settings XML

## Colour palette

| Token            | Hex       | Usage                        |
|------------------|-----------|------------------------------|
| `DARK_NAVY`      | `#1A1A2E` | Table header fill, body text |
| `CREAM_TEXT`     | `#E8E0D0` | Table header text            |
| `CREAM_BODY`     | `#F5F5F0` | Table body fill              |
| `GOLD_BORDER`    | `#C8A000` | Table outer border           |
| `GOLD_INNER`     | `#C8A951` | Table header top/bottom rule |
| `HEADER_GREY`    | `#555555` | Running header text          |

## Paragraph styles used in this book

| Style name      | Role                                      |
|-----------------|-------------------------------------------|
| `Normal`        | Body text — Garamond 11pt                 |
| `FirstPara`     | Opening para of chapter (no indent)       |
| `Heading 1`     | Part title                                |
| `Heading 2`     | Chapter title                             |
| `PartNumber`    | "PART I / II …" label                     |
| `SubHeading`    | In-chapter section title (italic)         |
| `BookQuote`     | Block quotation                           |
| `Attribution`   | Quote attribution line                    |
| `Separator`     | ★ ★ ★ scene break                        |
| `FirstPara`     | First paragraph after heading             |
| `ChapterTag`    | Chapter subtitle tag line                 |
| `ForewordHead`  | FOREWORD / EPILOGUE heading               |
| `BackMatterHead`| Sources, glossary section headings        |
| `EpigraphAttrib`| Epigraph attribution                      |
| `Epigraph`      | Opening epigraph text                     |

## Styled table builder

To add a new callout box anywhere in the document, call
`make_styled_table(rows)` from the formatter module where
`rows[0]` is the header and `rows[1:]` are body rows.
All-caps short rows inside the body are auto-detected as sub-headers
and rendered with the same dark-navy style.

## Re-running

```bash
python3 .claude/skills/kdp-book-formatter/kdp_formatter.py \
        input.docx output.docx
```
