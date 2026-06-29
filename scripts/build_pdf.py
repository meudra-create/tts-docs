#!/usr/bin/env python3
"""
Build PDF from individual chapter markdown files.
Visual spec : Ardoise & Or, FreeSerif.
"""
import os, re, glob, subprocess, shutil

ARDOISE = "2C3A4A"
GOLD    = "A07820"
DARKRED = "8B1A1A"
CREAM   = "F4EFE4"
GRIS    = "3C3C3C"

SCRATCHPAD  = '/tmp/claude-0/-home-user-tts-docs/e3ecab87-9343-5812-ac40-80d3b0b7d656/scratchpad'
CHAPTER_DIR = '/home/user/tts-docs/content/3.livre/'
OUT_TEX     = os.path.join(SCRATCHPAD, 'book.tex')
OUT_PDF_SRC = os.path.join(SCRATCHPAD, 'book.pdf')
OUT_PDF_DST = '/home/user/tts-docs/la-paix-on-peut-leviter.pdf'

# Pages de partie insérées avant le fichier portant ce numéro
PART_PAGES = {
    4:  ("PARTIE I",   "L'Afrique avant la domination"),
    8:  ("PARTIE II",  "Comment la dépendance a été organisée"),
    14: ("PARTIE III", "La guerre du Sahel"),
    19: ("PARTIE IV",  "La révolution de la souveraineté"),
    25: ("PARTIE V",   "Le réveil panafricain"),
    29: ("PARTIE VI",  "Les défis de demain"),
}

# ─────────────────────────────────────────────────────────────────────────────
# Helpers couleur
# ─────────────────────────────────────────────────────────────────────────────
def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

def rgb_cmd(name, h):
    r, g, b = hex_to_rgb(h)
    return f"\\definecolor{{{name}}}{{rgb}}{{{r:.4f},{g:.4f},{b:.4f}}}"

# ─────────────────────────────────────────────────────────────────────────────
# En-tête LaTeX
# ─────────────────────────────────────────────────────────────────────────────
LATEX_HEADER = (
r"""\documentclass[11pt,a4paper]{article}
\usepackage{fontspec}
\usepackage{xcolor}
\usepackage{geometry}
\usepackage{mdframed}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{colortbl}
\usepackage{titlesec}
\usepackage{setspace}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{microtype}
\usepackage{hyperref}

\geometry{left=2.5cm, right=2.0cm, top=2.5cm, bottom=2.5cm}
\setstretch{1.5}
\frenchspacing
\setlength{\headheight}{16pt}
\setlength{\parindent}{1cm}
\setlength{\parskip}{3pt}

\setmainfont{FreeSerif}[
  BoldFont      = FreeSerif Bold,
  ItalicFont    = FreeSerif Italic,
  BoldItalicFont = FreeSerif Bold Italic
]

"""
+ rgb_cmd("ardoise", ARDOISE) + "\n"
+ rgb_cmd("gold",    GOLD)    + "\n"
+ rgb_cmd("darkred", DARKRED) + "\n"
+ rgb_cmd("cream",   CREAM)   + "\n"
+ rgb_cmd("gris",    GRIS)    + "\n"
+ r"""
% ── Bandeau de chapitre : liseré or en haut + fond ardoise + texte blanc centré ──
\newcommand{\chapterbanner}[1]{%
  \noindent
  \begin{minipage}{\linewidth}
    {\color{gold}\rule{\linewidth}{2.5pt}}\\[-3pt]%
    \colorbox{ardoise}{%
      \parbox{\dimexpr\linewidth-2\fboxsep\relax}{%
        \centering\vspace{14pt}%
        {\color{white}\large\addfontfeature{LetterSpace=8}\MakeUppercase{#1}}%
        \vspace{14pt}%
      }%
    }%
    \\[-3pt]{\color{gold}\rule{\linewidth}{1pt}}%
  \end{minipage}%
}

% H2 : ardoise + filet or (sans gras)
\titleformat{\subsection}[block]
  {\color{ardoise}\mdseries\normalsize\addfontfeature{LetterSpace=4}}{}
  {0pt}{}
  [\vspace{2pt}{\color{gold}\hrule height 0.9pt}\vspace{5pt}]
\titlespacing*{\subsection}{0pt}{18pt}{8pt}

% H3 : ardoise (sans gras)
\titleformat{\subsubsection}[block]
  {\color{ardoise}\mdseries\small\itshape}{}
  {0pt}{}
\titlespacing*{\subsubsection}{0pt}{12pt}{5pt}

% ── Citation : filet or gauche (2 pt) + texte rouge italique aéré ──
\newmdenv[
  topline=false, bottomline=false, rightline=false, leftline=true,
  linewidth=0.5pt,
  linecolor=gold,
  backgroundcolor=white,
  innerleftmargin=18pt,
  innerrightmargin=6pt,
  innertopmargin=10pt,
  innerbottommargin=10pt,
  skipabove=14pt,
  skipbelow=14pt,
  leftmargin=0pt,
  rightmargin=0pt
]{citblock}

% ── Séparateur typographique or ──
\newcommand{\separator}{%
  \vspace{10pt}%
  \begin{center}{\color{gold}\large *\enspace *\enspace *}\end{center}%
  \vspace{8pt}%
}

% ── Filet de section (horizontal rule ---) ──
\newcommand{\sectionrule}{%
  \vspace{8pt}{\color{gold}\noindent\rule{\linewidth}{0.4pt}}\vspace{8pt}%
}

% ── Page de partie (page blanche centrée) ──
\newcommand{\partpage}[2]{%
  \clearpage
  \thispagestyle{empty}
  \null\vfill
  \begin{center}
    {\fontsize{12}{14}\selectfont\color{ardoise}%
     \addfontfeature{LetterSpace=14}\MakeUppercase{#1}}\\[1.4cm]
    {\fontsize{26}{32}\selectfont\color{ardoise}\MakeUppercase{#2}}\\[1.6cm]
    {\color{gold}\rule{8cm}{1.5pt}}
  \end{center}
  \vfill\vfill
  \clearpage
}

\pagestyle{fancy}
\fancyhf{}
\rhead{\color{ardoise}\small LA PAIX, ON PEUT L'ÉVITER}
\lhead{\color{gold}\small BEN--H2O}
\cfoot{\thepage}
\renewcommand{\headrulewidth}{0.9pt}
\renewcommand{\headrule}{\color{gold}\hrule}

\setcounter{secnumdepth}{-2}
\hypersetup{hidelinks}

\begin{document}

% ── Page de titre ──
\begin{titlepage}
\pagecolor{ardoise}
\color{white}
\vspace*{4cm}
\begin{center}
{\Huge\bfseries\MakeUppercase{La paix, on peut l'éviter}}\\[1cm]
{\large\color{gold} Enquête sur la naissance de l'Alliance des États du Sahel}\\[2cm]
{\Large BEN--H2O}\\[0.5cm]
{\color{gold} --- 2026 ---}
\end{center}
\vfill
\begin{center}
{\small\color{gold} \copyright{} 2026 BEN--H2O --- Tous droits réservés.}
\end{center}
\end{titlepage}
\pagecolor{white}
\color{black}

\newpage
\tableofcontents
\newpage
""")

LATEX_FOOTER = r"\end{document}" + "\n"

# ─────────────────────────────────────────────────────────────────────────────
# Échappement LaTeX
# ─────────────────────────────────────────────────────────────────────────────
def escape_latex(text):
    replacements = [
        ('\\', r'\textbackslash{}'),
        ('&',  r'\&'),
        ('%',  r'\%'),
        ('$',  r'\$'),
        ('#',  r'\#'),
        ('^',  r'\^{}'),
        ('_',  r'\_'),
        ('{',  r'\{'),
        ('}',  r'\}'),
        ('~',  r'\textasciitilde{}'),
        ('«',  r'\guillemotleft{}'),
        ('»',  r'\guillemotright{}'),
        ('—',  '---'),
        ('–',  '--'),
        ('★',  r'$\bigstar$'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text

def md_inline(text):
    text = escape_latex(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'{\\color{ardoise}\1}', text)
    text = re.sub(r'\*(.+?)\*',     r'\\textit{\1}', text)
    text = re.sub(r'`(.+?)`',       r'\\texttt{\1}', text)
    return text

# ─────────────────────────────────────────────────────────────────────────────
# Rendu d'un encadré (tableau avec header ardoise + lignes crème séparées)
# ─────────────────────────────────────────────────────────────────────────────
def render_table(title, rows):
    """
    Génère un tableau style photo :
    - Header : fond ardoise, texte blanc gras majuscules
    - Lignes  : fond crème, séparées par filet ardoise fin
    - Bordure extérieure ardoise fine
    """
    col = r'\dimexpr\linewidth-14pt\relax'
    lines = []
    lines.append(r'{%')
    lines.append(r'\arrayrulecolor{ardoise}%')
    lines.append(r'\setlength{\arrayrulewidth}{0.6pt}%')
    lines.append(r'\renewcommand{\arraystretch}{1.6}%')
    lines.append(r'\noindent\begin{tabular}{|p{' + col + r'}|}')
    lines.append(r'\hline')
    # Header row
    escaped_title = escape_latex(title)
    lines.append(
        r'\cellcolor{ardoise}{\color{white}\bfseries\small\MakeUppercase{'
        + escaped_title + r'}} \\')
    lines.append(r'\hline')
    # Data rows
    for row in rows:
        lines.append(
            r'\cellcolor{cream}{\color{gris}\small ' + md_inline(row) + r'} \\')
        lines.append(r'\hline')
    lines.append(r'\end{tabular}%')
    lines.append(r'\vspace{8pt}%')
    lines.append(r'}')
    return '\\par\\noindent\n' + '\n'.join(lines) + '\n\\par'

# ─────────────────────────────────────────────────────────────────────────────
# Rendu d'un tableau markdown à pipes (multi-colonnes), même habillage
# ─────────────────────────────────────────────────────────────────────────────
def render_pipe_table(header, rows):
    """
    Tableau multi-colonnes (| a | b | c |) au style ardoise/crème :
    - Ligne d'en-tête : fond ardoise, texte blanc gras
    - Lignes de données : fond crème, texte gris, filets ardoise fins
    """
    n = max(1, len(header))
    colw = r'\dimexpr(\linewidth-' + str(14 * n) + r'pt)/' + str(n) + r'\relax'
    colspec = '|' + '|'.join([r'p{' + colw + r'}'] * n) + '|'
    out = []
    out.append(r'{%')
    out.append(r'\arrayrulecolor{ardoise}%')
    out.append(r'\setlength{\arrayrulewidth}{0.6pt}%')
    out.append(r'\renewcommand{\arraystretch}{1.45}%')
    out.append(r'\noindent\footnotesize\begin{tabular}{' + colspec + r'}')
    out.append(r'\hline')
    hcells = [r'\cellcolor{ardoise}{\color{white}\bfseries ' + md_inline(c) + r'}'
              for c in header]
    out.append(' & '.join(hcells) + r' \\')
    out.append(r'\hline')
    for row in rows:
        cells = [r'\cellcolor{cream}{\color{gris} ' + md_inline(c) + r'}'
                 for c in row[:n]]
        while len(cells) < n:
            cells.append(r'\cellcolor{cream}{}')
        out.append(' & '.join(cells) + r' \\')
        out.append(r'\hline')
    out.append(r'\end{tabular}%')
    out.append(r'\vspace{8pt}%')
    out.append(r'}')
    return '\\par\\noindent\n' + '\n'.join(out) + '\n\\par'

def _split_pipe_row(line):
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    return [c.strip() for c in s.split('|')]

# ─────────────────────────────────────────────────────────────────────────────
# Parseur markdown → LaTeX
# ─────────────────────────────────────────────────────────────────────────────
def parse_chapter(md_text):
    lines = md_text.split('\n')
    out   = []
    i     = 0
    quote_buf = []

    def flush_quote():
        if quote_buf:
            clean = '\n'.join(quote_buf).strip()
            clean = re.sub(r'^> ?', '', clean, flags=re.MULTILINE)
            out.append(r'\begin{citblock}')
            out.append(
                r'{\color{darkred}\itshape\setstretch{1.5} '
                + md_inline(clean) + r'}')
            out.append(r'\end{citblock}')
            quote_buf.clear()

    while i < len(lines):
        line = lines[i]

        # Ligne vide
        if not line.strip():
            flush_quote()
            out.append('')
            i += 1
            continue

        # H1 → bandeau de chapitre (direct, sans passer par \titleformat)
        if line.startswith('# '):
            flush_quote()
            title = md_inline(line[2:].strip())
            out.append(r'\newpage')
            out.append(r'\phantomsection')
            out.append(r'\addcontentsline{toc}{section}{' + title + '}')
            out.append(r'\chapterbanner{' + title + '}')
            out.append(r'\vspace{14pt}')
            out.append(r'\noindent')
            i += 1
            continue

        # H2
        if line.startswith('## '):
            flush_quote()
            out.append(r'\subsection{' + md_inline(line[3:].strip()) + '}')
            out.append(r'\noindent')
            i += 1
            continue

        # H3
        if line.startswith('### '):
            flush_quote()
            out.append(r'\subsubsection{' + md_inline(line[4:].strip()) + '}')
            out.append(r'\noindent')
            i += 1
            continue

        # Tableau markdown à pipes : | a | b |  puis  |---|---|  puis lignes
        if (re.match(r'^\s*\|.*\|\s*$', line)
                and i + 1 < len(lines)
                and re.match(r'^\s*\|[\s:|\-]+\|\s*$', lines[i + 1])
                and '-' in lines[i + 1]):
            flush_quote()
            header = _split_pipe_row(line)
            j = i + 2
            body = []
            while j < len(lines) and re.match(r'^\s*\|.*\|\s*$', lines[j]):
                body.append(_split_pipe_row(lines[j]))
                j += 1
            out.append(render_pipe_table(header, body))
            i = j
            continue

        # Séparateur horizontal --- → filet or fin
        if re.match(r'^-{3,}\s*$', line.strip()):
            flush_quote()
            out.append(r'\sectionrule{}')
            i += 1
            continue

        # Tableau pandoc : RULE (20+ tirets) → **TITRE** → RULE → lignes → RULE
        if re.match(r'^\s*-{20,}\s*$', line):
            flush_quote()
            peek = i + 1
            while peek < len(lines) and not lines[peek].strip():
                peek += 1
            title_line = lines[peek].strip() if peek < len(lines) else ''
            next_peek  = peek + 1
            while next_peek < len(lines) and not lines[next_peek].strip():
                next_peek += 1
            rule_after = (next_peek < len(lines) and
                          re.match(r'^\s*-{20,}\s*$', lines[next_peek]))
            is_table = (bool(re.match(r'^\*\*(.+?)\*\*$', title_line))
                        and rule_after and next_peek - i <= 5)
            if not is_table:
                i += 1
                continue
            title_m = re.match(r'^\*\*(.+?)\*\*$', title_line)
            title   = title_m.group(1)
            j       = next_peek + 1
            body_rows, body_buf = [], []
            while j < len(lines) and not re.match(r'^\s*-{20,}\s*$', lines[j]):
                ln = lines[j].strip()
                if not ln:
                    if body_buf:
                        body_rows.append(' '.join(body_buf))
                        body_buf = []
                else:
                    if not re.match(r'^#{1,4} ', ln):
                        body_buf.append(ln)
                j += 1
            if body_buf:
                body_rows.append(' '.join(body_buf))
            if j < len(lines):
                j += 1
            out.append(render_table(title, body_rows))
            i = j
            continue

        # Séparateur ★★★ ou * * *
        if line.strip() in ('★★★', '* * *', '\* \* \*'):
            flush_quote()
            out.append(r'\separator{}')
            i += 1
            continue

        # Citation >
        if line.startswith('>'):
            quote_buf.append(re.sub(r'^> ?', '', line))
            i += 1
            continue

        # Liste à puces (inclut les sous-items indentés — tout aplatit en itemize)
        if re.match(r'^[ \t]*[-*] ', line):
            flush_quote()
            # collect consecutive bullet lines (any indent level)
            items = []
            while i < len(lines) and re.match(r'^[ \t]*[-*] ', lines[i]):
                raw = re.sub(r'^[ \t]*[-*] ', '', lines[i])
                items.append(md_inline(raw.strip()))
                i += 1
            out.append(r'\begin{itemize}[leftmargin=*]')
            for it in items:
                out.append(r'  \item ' + it)
            out.append(r'\end{itemize}')
            continue

        # Liste numérotée
        if re.match(r'^\d+\. ', line):
            flush_quote()
            out.append(r'\begin{enumerate}[leftmargin=*]')
            out.append(r'  \item ' + md_inline(re.sub(r'^\d+\. ', '', line)))
            j = i + 1
            while j < len(lines) and re.match(r'^\d+\. ', lines[j]):
                out.append(r'  \item ' + md_inline(re.sub(r'^\d+\. ', '', lines[j])))
                j += 1
            out.append(r'\end{enumerate}')
            i = j
            continue

        # Ligne uniquement en gras → encadré avec liste qui suit
        bm = re.match(r'^\*\*(.+?)\*\*\s*$', line.strip())
        if bm:
            flush_quote()
            title = bm.group(1)
            rows, j = [], i + 1
            while j < len(lines) and j < i + 35:
                nl = lines[j].strip()
                if not nl:
                    j += 1
                    break
                if re.match(r'^[-*\d]', nl):
                    content = re.sub(r'^[-*]\s+|^\d+\.\s+', '', nl)
                    content = re.sub(r'\*\*(.+?)\*\*', r'\1', content)
                    content = re.sub(r'\*(.+?)\*',     r'\1', content)
                    rows.append(content)
                    j += 1
                else:
                    break
            if rows:
                out.append(render_table(title, rows))
                i = j
            else:
                out.append(r'{\color{ardoise}' + md_inline(title) + '}')
                i += 1
            continue

        # Paragraphe normal
        flush_quote()
        text = md_inline(line.strip())
        if text:
            out.append(text + '\n')
        i += 1

    flush_quote()
    return '\n'.join(out)

# ─────────────────────────────────────────────────────────────────────────────
# Assemblage du document
# ─────────────────────────────────────────────────────────────────────────────
print("Assemblage des chapitres...")

# Tous les fichiers numérotés (hors index.md)
all_files = sorted(
    [f for f in glob.glob(os.path.join(CHAPTER_DIR, '[0-9]*.md'))
     if 'index' not in os.path.basename(f)],
    key=lambda x: int(os.path.basename(x).split('.')[0])
)

latex_chunks = []

for filepath in all_files:
    fnum = int(os.path.basename(filepath).split('.')[0])

    # Injecter la page de partie en LaTeX brut AVANT le chapitre
    if fnum in PART_PAGES:
        label, title = PART_PAGES[fnum]
        latex_chunks.append(f'\\partpage{{{label}}}{{{escape_latex(title)}}}\n')

    # Lire et nettoyer le frontmatter YAML
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[2].strip()

    # Nettoyer les échappements pandoc
    content = re.sub(r'\\([\'"$~\[\]@*`#%&_{}])', r'\1', content)

    fname = os.path.basename(filepath)
    print(f"  ✓ {fnum}: {fname[:55]}")
    # Convertir ce chapitre en LaTeX puis l'ajouter
    latex_chunks.append(parse_chapter(content))

print("Conversion markdown → LaTeX...")
body_latex = '\n\n'.join(latex_chunks)

latex_doc = LATEX_HEADER + body_latex + LATEX_FOOTER

with open(OUT_TEX, 'w', encoding='utf-8') as f:
    f.write(latex_doc)
print(f"Source LaTeX : {len(latex_doc):,} caractères")

# ─────────────────────────────────────────────────────────────────────────────
# Compilation xelatex (2 passes pour la table des matières)
# ─────────────────────────────────────────────────────────────────────────────
def xelatex(pass_num):
    print(f"xelatex passe {pass_num}/2...")
    r = subprocess.run(
        ['xelatex', '-interaction=nonstopmode',
         '-output-directory', SCRATCHPAD, OUT_TEX],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        print("ERREURS xelatex :")
        print('\n'.join(r.stdout.split('\n')[-40:]))
        return False
    return True

if xelatex(1) and xelatex(2):
    shutil.copy(OUT_PDF_SRC, OUT_PDF_DST)
    size = os.path.getsize(OUT_PDF_DST)
    pages_line = [l for l in open(OUT_PDF_SRC.replace('.pdf', '.log'), errors='ignore')
                  if 'Output written' in l]
    print(pages_line[0].strip() if pages_line else '')
    print(f"PDF sauvegardé : {OUT_PDF_DST}  ({size/1024:.0f} KB)")
