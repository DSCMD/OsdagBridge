# =============================================================================
# OsdagBridge — Centralized Report Styling & Layout Helpers
# =============================================================================
r"""
Centralized visual design system for OsdagBridge LaTeX/PDF reports.

Provides:
- Page geometry & margin constants (preventing footer/longtable collisions)
- Brand color palette & typography tokens
- Preamble & header/footer builders
- Reusable LongTable / Tabular builders with:
  * Guaranteed fit within A4 printable width (15.92 cm at 1 in margins)
  * Automatic repeating headers across page breaks (\endfirsthead / \endhead)
  * Consistent cell padding, header shading, borders, and typography
"""

from typing import Iterable, Optional, Sequence


# ---------------------------------------------------------------------------
# 1. Design Tokens: Colors, Dimensions & Typography
# ---------------------------------------------------------------------------

COLORS = {
    "primary_hex": "91B014",       # Osdag signature green
    "header_bg": "osdagGreen!14",  # Subtle tinted header fill
    "subhdr_bg": "gray!12",        # Section divider row fill
    "border_gray": "gray!65",
    "pass_text": "black",
    "fail_text": "red",
    "warn_text": "orange!85!black",
}

# A4 paper = 21.0 cm wide x 29.7 cm high.
# With left=1.0in (2.54cm) and right=1.0in (2.54cm), printable \textwidth = 15.92 cm.
PAGE_GEOMETRY = {
    "paper": "a4paper",
    "top": "0.95in",
    "bottom": "1.10in",
    "left": "1.0in",
    "right": "1.0in",
    "headheight": "16pt",
    "headsep": "18pt",
    "footskip": "38pt",
}

# Safe two-column Key-Value widths:
# 5.4 cm + 9.5 cm + 4 * 6pt (~0.85 cm padding) + rules (~0.07 cm) = 15.82 cm <= 15.92 cm
KV_COL_SPEC = "|L{5.4cm}|L{9.5cm}|"
KV_WIDE_PARAM_COL_SPEC = "|L{6.8cm}|L{8.1cm}|"

TABLE_SPACING = {
    "tabcolsep": "6pt",
    "arraystretch": "1.18",
    "arrayrulewidth": "0.5pt",
    "extrarowheight": "0.8pt",
    "lt_pre": "4pt",
    "lt_post": "8pt",
    "needspace": "6\\baselineskip",
}


# ---------------------------------------------------------------------------
# 2. Preamble & Page Style Builders
# ---------------------------------------------------------------------------

def build_preamble(
    project_name_tex: str,
    job_number_tex: str,
    report_date_tex: str,
    report_version_tex: str = "Rev 0",
) -> str:
    """Return the complete, standardized LaTeX document preamble."""
    geom_opts = ", ".join(f"{k}={v}" for k, v in PAGE_GEOMETRY.items() if k != "paper")
    return rf"""
\documentclass[12pt,{PAGE_GEOMETRY['paper']}]{{report}}

% Geometry & Margins (configured to prevent footer/table overlap)
\usepackage[{PAGE_GEOMETRY['paper']}, {geom_opts}]{{geometry}}

% Core Packages
\usepackage{{graphicx}}
\usepackage{{amsmath}}
\usepackage{{amssymb}}
\usepackage{{booktabs}}
\usepackage{{array}}
\usepackage{{tabularx}}
\usepackage{{float}}
\usepackage{{fancyhdr}}
\usepackage[hidelinks]{{hyperref}}
\usepackage[table]{{xcolor}}
\usepackage{{setspace}}
\usepackage{{enumitem}}
\usepackage{{caption}}
\usepackage{{subcaption}}
\usepackage{{multirow}}
\usepackage{{colortbl}}
\usepackage{{longtable}}
\usepackage{{titlesec}}
\usepackage{{titletoc}}
\usepackage{{lastpage}}
\usepackage{{makecell}}
\usepackage{{etoolbox}}
\usepackage{{needspace}}

% Caption Styling
\captionsetup{{
    labelfont=bf,
    textfont=bf,
    justification=raggedright,
    singlelinecheck=false,
    format=plain,
    skip=4pt
}}

\numberwithin{{table}}{{chapter}}
\numberwithin{{figure}}{{chapter}}

% Global Table Spacing & Alignment
\setlength{{\LTleft}}{{\fill}}
\setlength{{\LTright}}{{\fill}}
\setlength{{\tabcolsep}}{{{TABLE_SPACING['tabcolsep']}}}
\renewcommand{{\arraystretch}}{{{TABLE_SPACING['arraystretch']}}}
\setlength{{\LTpre}}{{{TABLE_SPACING['lt_pre']}}}
\setlength{{\LTpost}}{{{TABLE_SPACING['lt_post']}}}
\setlength{{\arrayrulewidth}}{{{TABLE_SPACING['arrayrulewidth']}}}
\setlength{{\extrarowheight}}{{{TABLE_SPACING['extrarowheight']}}}

% Prevent orphaned table headers or bottom-margin collisions
\BeforeBeginEnvironment{{table}}{{\needspace{{{TABLE_SPACING['needspace']}}}}}
\BeforeBeginEnvironment{{longtable}}{{\needspace{{{TABLE_SPACING['needspace']}}}}}

% Brand Color Definitions
\definecolor{{osdagGreen}}{{HTML}}{{{COLORS['primary_hex']}}}
\colorlet{{osdagTableHeader}}{{{COLORS['header_bg']}}}
\colorlet{{osdagSubHeader}}{{{COLORS['subhdr_bg']}}}

% Running Header & Footer Styles
\fancypagestyle{{main}}{{
  \fancyhf{{}}
  \fancyhead[L]{{\small {project_name_tex} $|$ {job_number_tex}}}
  \fancyhead[R]{{\small {report_date_tex} $|$ {report_version_tex}}}
  \fancyfoot[L]{{\small Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}}
  \fancyfoot[R]{{\small Page \thepage\ of \pageref{{LastPage}}}}
  \renewcommand{{\headrule}}{{\color{{osdagGreen}}\hrule width\headwidth height 1pt \vspace{{2pt}}}}
  \renewcommand{{\footrule}}{{%
    \ifbool{{hasSDonPage}}{{%
      \vspace{{-16pt}}%
      \hbox to \headwidth{{\textcolor{{black}}{{\footnotesize\textit{{* Software default value}}}}\hfil}}%
      \vspace{{3pt}}%
    }}{{%
      \vspace{{-4pt}}%
    }}%
    \color{{osdagGreen}}\hrule width\headwidth height 1pt \vspace{{4pt}}%
  }}
}}

\fancypagestyle{{plain}}{{
  \fancyhf{{}}
  \fancyhead[L]{{\small {project_name_tex} $|$ {job_number_tex}}}
  \fancyhead[R]{{\small {report_date_tex} $|$ {report_version_tex}}}
  \fancyfoot[L]{{\small Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}}
  \fancyfoot[R]{{\small Page \thepage\ of \pageref{{LastPage}}}}
  \renewcommand{{\headrule}}{{\color{{osdagGreen}}\hrule width\headwidth height 1pt \vspace{{2pt}}}}
  \renewcommand{{\footrule}}{{%
    \ifbool{{hasSDonPage}}{{%
      \vspace{{-16pt}}%
      \hbox to \headwidth{{\textcolor{{black}}{{\footnotesize\textit{{* Software default value}}}}\hfil}}%
      \vspace{{3pt}}%
    }}{{%
      \vspace{{-4pt}}%
    }}%
    \color{{osdagGreen}}\hrule width\headwidth height 1pt \vspace{{4pt}}%
  }}
}}

\fancypagestyle{{firstpage}}{{
  \fancyhf{{}}
  \renewcommand{{\headrulewidth}}{{0pt}}
  \fancyfoot[L]{{\small Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}}
  \fancyfoot[R]{{\small Page \thepage\ of \pageref{{LastPage}}}}
  \renewcommand{{\footrule}}{{\vspace{{-4pt}}\color{{osdagGreen}}\hrule width\headwidth height 1pt \vspace{{4pt}}}}
}}

\pagestyle{{main}}
\setstretch{{1.15}}

% Custom Column Helpers
\newcommand{{\placeholder}}[1]{{\textit{{\textless #1\textgreater}}}}
\newcommand{{\todo}}[1]{{\colorbox{{yellow}}{{TODO: #1}}}}
\newcolumntype{{L}}[1]{{>{{\raggedright\arraybackslash}}p{{#1}}}}
\newcolumntype{{C}}[1]{{>{{\centering\arraybackslash}}p{{#1}}}}
\newcolumntype{{R}}[1]{{>{{\raggedleft\arraybackslash}}p{{#1}}}}

% Software-default footnote tracker
\newbool{{hasSDonPage}}
\boolfalse{{hasSDonPage}}
\newcommand{{\markSD}}{{\global\booltrue{{hasSDonPage}}}}
\newcommand{{\sdstar}}{{\textsuperscript{{*}}\markSD{{}}}}
\AddToHook{{shipout/before}}{{\global\boolfalse{{hasSDonPage}}}}

\title{{\Large\textbf{{OsdagBridge}} \\ \normalsize Open Source Software for Steel Girder Bridge Design \\ \vspace{{2cm}} \large Design Report}}
\author{{}}
\date{{}}

\begin{{document}}
"""


# ---------------------------------------------------------------------------
# 3. Reusable LongTable / Tabular Builders
# ---------------------------------------------------------------------------

def _format_header_row(headers: Sequence[str]) -> str:
    cells = [rf"\textbf{{{h}}}" if h else "" for h in headers]
    return r"\rowcolor{osdagTableHeader}" + "\n" + " & ".join(cells) + r" \\[6pt]"


def build_styled_longtable(
    caption: str,
    headers: Sequence[str],
    rows: Iterable[Sequence[str]],
    col_spec: str = KV_COL_SPEC,
    note: Optional[str] = None,
    raw_rows_tex: Optional[str] = None,
    space_before: str = "0.8em",
) -> str:
    r"""
    Build a standardized LaTeX longtable with:
    - Tinted header row (\rowcolor{osdagTableHeader})
    - Automatic header repetition across page breaks (\endfirsthead / \endhead)
    - Consistent row spacing and horizontal rules
    - Optional italicized footnote block directly beneath the table
    """
    n_cols = max(1, len(headers))
    hdr_tex = _format_header_row(headers)

    if raw_rows_tex is not None:
        body_tex = raw_rows_tex.strip()
    else:
        formatted_rows = []
        for row in rows:
            joined = " & ".join(str(cell) for cell in row)
            formatted_rows.append(joined + r" \\[6pt]" + "\n" + r"\hline")
        body_tex = "\n".join(formatted_rows)

    lt_tex = (
        rf"\begin{{longtable}}{{{col_spec}}}" + "\n"
        rf"\caption{{{caption}}}\\ [4pt]" + "\n"
        r"\hline" + "\n"
        + hdr_tex + "\n"
        r"\hline" + "\n"
        r"\endfirsthead" + "\n\n"
        rf"\multicolumn{{{n_cols}}}{{l}}{{\small\textit{{(Continued) {caption}}}}}\\" + "\n"
        r"\hline" + "\n"
        + hdr_tex + "\n"
        r"\hline" + "\n"
        r"\endhead" + "\n\n"
        r"\hline" + "\n"
        r"\endfoot" + "\n\n"
        r"\hline" + "\n"
        r"\endlastfoot" + "\n\n"
        + body_tex + "\n"
        r"\end{longtable}"
    )

    parts = []
    if space_before:
        parts.append(rf"\vspace{{{space_before}}}")
    parts.append(lt_tex)
    if note:
        parts.append(rf"\noindent\textit{{Note: {note}}}")
    return "\n".join(parts)


def build_kv_longtable(
    caption: str,
    kv_rows: Sequence[Sequence[str]],
    col_spec: str = KV_COL_SPEC,
    headers: Sequence[str] = ("Parameter", "Value"),
    note: Optional[str] = None,
    space_before: str = "0.8em",
) -> str:
    """Convenience wrapper for two-column Parameter / Value longtables."""
    formatted_rows = [
        [rf"\textnormal{{{param}}}", val] for param, val in kv_rows
    ]
    return build_styled_longtable(
        caption=caption,
        headers=headers,
        rows=formatted_rows,
        col_spec=col_spec,
        note=note,
        space_before=space_before,
    )


def build_kv_tabular(
    kv_rows: Sequence[Sequence[str]],
    col_spec: str = KV_COL_SPEC,
    headers: Optional[Sequence[str]] = ("Parameter", "Value"),
) -> str:
    """Build a compact non-floating two-column tabular block."""
    lines = [rf"\begin{{tabular}}{{{col_spec}}}", r"\hline"]
    if headers:
        lines.append(_format_header_row(headers))
        lines.append(r"\hline")
    for param, val in kv_rows:
        lines.append(rf"{param} & {val} \\[6pt]")
        lines.append(r"\hline")
    lines.append(r"\end{tabular}")
    return "\n".join(lines)
