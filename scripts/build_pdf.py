#!/usr/bin/env python3
"""
Build a LaTeX source from the LIVREFINAL markdown + supplementary chapters,
applying the full Ardoise & Or visual spec, then compile with xelatex.
"""
import os, re, glob

ARDOISE = "2C3A4A"
GOLD    = "A07820"
DARKRED = "8B1A1A"
CREAM   = "F4EFE4"
GRIS    = "3C3C3C"
WHITE   = "FFFFFF"

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255 for i in (0,2,4))

def rgb_cmd(name, h):
    r,g,b = hex_to_rgb(h)
    return f"\\definecolor{{{name}}}{{rgb}}{{{r:.4f},{g:.4f},{b:.4f}}}"

LATEX_HEADER = r"""\documentclass[11pt,a4paper]{article}
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

\geometry{margin=2.5cm, top=2.5cm, bottom=2.5cm}
\setstretch{1.3}

\setmainfont{FreeSerif}[
  BoldFont = FreeSerif Bold,
  ItalicFont = FreeSerif Italic,
  BoldItalicFont = FreeSerif Bold Italic
]

""" + rgb_cmd("ardoise", ARDOISE) + "\n" \
   + rgb_cmd("gold", GOLD) + "\n" \
   + rgb_cmd("darkred", DARKRED) + "\n" \
   + rgb_cmd("cream", CREAM) + "\n" \
   + rgb_cmd("gris", GRIS) + "\n" \
   + r"""
% H1: bandeau plein ardoise + blanc capitales + filet or en bas
\titleformat{\section}
  {\color{white}\bfseries\large\MakeUppercase}
  {}
  {0pt}
  {\colorbox{ardoise}{\parbox{\dimexpr\linewidth-2\fboxsep\relax}{\vspace{3pt}#1\vspace{3pt}}}}
  [\vspace{1pt}{\color{gold}\hrule height 1.5pt}\vspace{4pt}]

% H2: texte ardoise + filet or en bas
\titleformat{\subsection}
  {\color{ardoise}\bfseries\normalsize}
  {}
  {0pt}
  {#1}
  [\vspace{1pt}{\color{gold}\hrule height 0.9pt}\vspace{4pt}]

% H3: texte ardoise gras
\titleformat{\subsubsection}
  {\color{ardoise}\bfseries\small}
  {}
  {0pt}
  {#1}

% Encadré style: header ardoise + corps crème + bordure ardoise 0.9pt
\newmdenv[
  linecolor=ardoise,
  linewidth=0.9pt,
  backgroundcolor=cream,
  innerleftmargin=6pt,
  innerrightmargin=6pt,
  innertopmargin=4pt,
  innerbottommargin=4pt,
  skipabove=6pt,
  skipbelow=6pt
]{encadre}

\newcommand{\encadretitle}[1]{%
  \noindent\colorbox{ardoise}{\parbox{\linewidth}{%
    \vspace{3pt}\color{white}\bfseries\small\MakeUppercase{#1}\vspace{3pt}%
  }}%
  \vspace{0pt}%
}

% Citation en rouge foncé italique
\newenvironment{citblock}
  {\begin{quote}\color{darkred}\itshape\small}
  {\end{quote}}

% Séparateur étoile or
\newcommand{\separator}{%
  \begin{center}\color{gold}\large ★★★\end{center}%
}

\pagestyle{fancy}
\fancyhf{}
\rhead{\color{ardoise}\small LA PAIX, ON PEUT L'ÉVITER}
\lhead{\color{gold}\small BEN--H2O}
\cfoot{\thepage}
\renewcommand{\headrulewidth}{0.9pt}
\renewcommand{\headrule}{\color{gold}\hrule}

% Suppress automatic section numbering at all levels
\setcounter{secnumdepth}{-2}

\begin{document}

\begin{titlepage}
\pagecolor{ardoise}
\color{white}
\vspace*{4cm}
\begin{center}
{\Huge\bfseries\MakeUppercase{La paix, on peut l'éviter}}\\[1cm]
{\large\color{gold} Enquête sur la naissance de l'Alliance des États du Sahel}\\[2cm]
{\Large BEN--H2O}\\[0.5cm]
{\color{gold} — 2026 —}
\end{center}
\vfill
\begin{center}
{\small\color{gold} © 2026 BEN--H2O — Tous droits réservés.}
\end{center}
\end{titlepage}
\pagecolor{white}
\color{black}

\newpage
\tableofcontents
\newpage
"""

LATEX_FOOTER = r"""
\end{document}
"""

def escape_latex(text):
    """Escape special LaTeX characters."""
    replacements = [
        ('\\', r'\textbackslash{}'),
        ('&', r'\&'),
        ('%', r'\%'),
        ('$', r'\$'),
        ('#', r'\#'),
        ('^', r'\^{}'),
        ('_', r'\_'),
        ('{', r'\{'),
        ('}', r'\}'),
        ('~', r'\textasciitilde{}'),
        ('«', r'\guillemotleft{}'),
        ('»', r'\guillemotright{}'),
        ('—', '---'),
        ('–', '--'),
        ('★', r'$\bigstar$'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text

def md_inline(text):
    """Convert inline markdown formatting to LaTeX."""
    text = escape_latex(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    text = re.sub(r'\*(.+?)\*',     r'\\textit{\1}', text)
    text = re.sub(r'`(.+?)`',       r'\\texttt{\1}', text)
    return text

def parse_chapter(md_text):
    """Parse markdown chapter to LaTeX."""
    lines = md_text.split('\n')
    out = []
    i = 0
    quote_buf = []

    def flush_quote():
        if quote_buf:
            clean = '\n'.join(quote_buf).strip()
            clean = re.sub(r'^> ?', '', clean, flags=re.MULTILINE)
            out.append(r'\begin{citblock}')
            out.append(md_inline(clean))
            out.append(r'\end{citblock}')
            quote_buf.clear()

    while i < len(lines):
        line = lines[i]

        if not line.strip() or line.strip() == r'\newpage':
            flush_quote()
            out.append('')
            i += 1; continue

        if line.startswith('# '):
            flush_quote()
            out.append(r'\newpage')
            out.append(r'\section{' + md_inline(line[2:].strip()) + '}')
            i += 1; continue

        if line.startswith('## '):
            flush_quote()
            out.append(r'\subsection{' + md_inline(line[3:].strip()) + '}')
            i += 1; continue

        if line.startswith('### '):
            flush_quote()
            out.append(r'\subsubsection{' + md_inline(line[4:].strip()) + '}')
            i += 1; continue

        # Pandoc simple-table: RULE → title → RULE → body → RULE
        # Only trigger when the NEXT non-blank line is a bold title immediately
        # followed by another rule (gap ≤ 3 lines). Otherwise it's a plain separator.
        if re.match(r'^\s*-{20,}\s*$', line):
            flush_quote()
            # Peek: check if next non-blank is **TITLE** AND the line after is a rule
            peek = i + 1
            while peek < len(lines) and not lines[peek].strip():
                peek += 1
            title_line = lines[peek].strip() if peek < len(lines) else ''
            next_peek = peek + 1
            while next_peek < len(lines) and not lines[next_peek].strip():
                next_peek += 1
            rule_after = (next_peek < len(lines) and
                          re.match(r'^\s*-{20,}\s*$', lines[next_peek]))
            is_table = (bool(re.match(r'^\*\*(.+?)\*\*$', title_line)) and rule_after
                        and next_peek - i <= 5)
            if not is_table:
                # Plain horizontal separator — just skip
                i += 1; continue
            # It's a three-rule table: consume title + separator rule
            title_m = re.match(r'^\*\*(.+?)\*\*$', title_line)
            title = title_m.group(1)
            j = next_peek + 1  # after the separator rule
            # Collect body until closing rule
            body_rows = []
            body_buf = []
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
                j += 1  # consume closing rule
            out.append(r'\encadretitle{' + escape_latex(title) + '}')
            out.append(r'\begin{encadre}')
            if body_rows:
                out.append(r'\begin{itemize}[leftmargin=*,itemsep=2pt]')
                for r in body_rows:
                    out.append(r'  \item {\small\color{gris} ' + md_inline(r) + '}')
                out.append(r'\end{itemize}')
            out.append(r'\end{encadre}')
            i = j; continue

        if re.match(r'^---+$', line.strip()):
            flush_quote(); i += 1; continue

        if line.strip() == '★★★':
            flush_quote()
            out.append(r'\separator{}')
            i += 1; continue

        if line.startswith('>'):
            quote_buf.append(re.sub(r'^> ?', '', line))
            i += 1; continue

        if re.match(r'^[-*] ', line):
            flush_quote()
            if not out or out[-1] != r'\begin{itemize}':
                out.append(r'\begin{itemize}[leftmargin=*]')
            out.append(r'  \item ' + md_inline(line[2:].strip()))
            # peek: if next line is not a bullet, close list
            if i+1 >= len(lines) or not re.match(r'^[-*] ', lines[i+1]):
                out.append(r'\end{itemize}')
            i += 1; continue

        if re.match(r'^\d+\. ', line):
            flush_quote()
            out.append(r'\begin{enumerate}[leftmargin=*]')
            out.append(r'  \item ' + md_inline(re.sub(r'^\d+\. ', '', line)))
            j = i+1
            while j < len(lines) and re.match(r'^\d+\. ', lines[j]):
                out.append(r'  \item ' + md_inline(re.sub(r'^\d+\. ', '', lines[j])))
                j += 1
            out.append(r'\end{enumerate}')
            i = j; continue

        # Bold-only line → encadré
        bm = re.match(r'^\*\*(.+?)\*\*\s*$', line.strip())
        if bm:
            flush_quote()
            title = bm.group(1)
            rows = []; j = i + 1
            while j < len(lines) and j < i + 35:
                nl = lines[j].strip()
                if not nl: j += 1; break
                if re.match(r'^[-*\d]', nl):
                    content = re.sub(r'^[-*]\s+|^\d+\.\s+', '', nl)
                    content = re.sub(r'\*\*(.+?)\*\*', r'\1', content)
                    content = re.sub(r'\*(.+?)\*',     r'\1', content)
                    rows.append(content); j += 1
                else: break
            if rows:
                out.append(r'\encadretitle{' + escape_latex(title) + '}')
                out.append(r'\begin{encadre}')
                out.append(r'\begin{itemize}[leftmargin=*,itemsep=1pt]')
                for r in rows:
                    out.append(r'  \item {\small\color{gris} ' + escape_latex(r) + '}')
                out.append(r'\end{itemize}')
                out.append(r'\end{encadre}')
                i = j
            else:
                out.append(r'{\color{ardoise}\textbf{' + md_inline(title) + '}}')
                i += 1
            continue

        flush_quote()
        text = md_inline(line.strip())
        if text:
            out.append(text + '\n')
        i += 1

    flush_quote()
    return '\n'.join(out)

# ─── Assemble document ────────────────────────────────────────────────────────

# Read LIVREFINAL original (chapters 1-31 etc.)
with open('/tmp/claude-0/-home-user-tts-docs/e3ecab87-9343-5812-ac40-80d3b0b7d656/scratchpad/livrefinal_full.md', 'r') as f:
    livrefinal_md = f.read()

# Strip the YAML-like header (first lines before first #)
livrefinal_body = livrefinal_md[livrefinal_md.find('# AVANT-PROPOS'):]

# Supplementary chapters
chapter_dir = '/home/user/tts-docs/content/3.livre/'
supp_files = sorted(
    [f for f in glob.glob(os.path.join(chapter_dir, '[0-9]*.md'))
     if int(os.path.basename(f).split('.')[0]) >= 40],
    key=lambda x: int(os.path.basename(x).split('.')[0])
)

supp_content = ''
for filepath in supp_files:
    with open(filepath, 'r') as f:
        content = f.read()
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3: content = parts[2].strip()
    supp_content += '\n\n' + content

# Combine
all_md = livrefinal_body + '\n\n---\n\n' + supp_content

# Strip pandoc backslash-escapes of literal punctuation (\' \" \* \$ \~ \[ \] \@ ...)
all_md = re.sub(r'\\([\'"$~\[\]@*`#%&_{}])', r'\1', all_md)

print("Parsing markdown to LaTeX...")
body_latex = parse_chapter(all_md)

latex_doc = LATEX_HEADER + body_latex + LATEX_FOOTER

out_tex = '/tmp/claude-0/-home-user-tts-docs/e3ecab87-9343-5812-ac40-80d3b0b7d656/scratchpad/book.tex'
with open(out_tex, 'w', encoding='utf-8') as f:
    f.write(latex_doc)

print(f"LaTeX source written: {len(latex_doc)} chars")
print("Compiling with xelatex (pass 1/2)...")
import subprocess
result = subprocess.run(
    ['xelatex', '-interaction=nonstopmode', '-output-directory',
     '/tmp/claude-0/-home-user-tts-docs/e3ecab87-9343-5812-ac40-80d3b0b7d656/scratchpad/',
     out_tex],
    capture_output=True, text=True
)
if result.returncode != 0:
    print("xelatex errors:")
    # Show last 30 lines of log
    print('\n'.join(result.stdout.split('\n')[-30:]))
else:
    print("Pass 1 OK — running pass 2 for TOC...")
    subprocess.run(
        ['xelatex', '-interaction=nonstopmode', '-output-directory',
         '/tmp/claude-0/-home-user-tts-docs/e3ecab87-9343-5812-ac40-80d3b0b7d656/scratchpad/',
         out_tex],
        capture_output=True, text=True
    )
    import shutil
    src = '/tmp/claude-0/-home-user-tts-docs/e3ecab87-9343-5812-ac40-80d3b0b7d656/scratchpad/book.pdf'
    dst = '/home/user/tts-docs/la-paix-on-peut-leviter.pdf'
    shutil.copy(src, dst)
    size = os.path.getsize(dst)
    print(f"PDF saved: {dst}  ({size/1024:.0f} KB)")
