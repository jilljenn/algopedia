from django.shortcuts import render, get_object_or_404
from algopedia.models import Algo, Implementation, Category, Star
from pygments.formatters import LatexFormatter

def generateNotebook(implementations):
    # TODO options de génération : titre, auteur, mutlicol?, linenos ?, a4paper/letter? marges? tailles, ordre des algos, sections
    # premise
    latex = r"""\documentclass[8pt]{extarticle}
\usepackage{fancyvrb}
%\usepackage{listings}
\usepackage{color}
\usepackage[utf8]{inputenc}
\usepackage[a4paper]{geometry}
\geometry{
  left=15mm,
  right=7mm,
  top=7mm,
  bottom=15mm
}
%\usepackage{multicol}
%\setlength{\columnsep}{1cm}
%\def\@xobeysp{\mbox{}\space}
"""
    # pygments premise
    latex += LatexFormatter().get_style_defs()
    # title and table of contents
    latex += r"""
\title{Notebook}
\author{}
\date\today

\begin{document}

\maketitle
%\begin{multicols}{2}
\tableofcontents
%\end{multicols}

%\begin{multicols}{2}
"""

    for implem in implementations:
        latex += "\subsection{" + implem.implementation.algo.name + "}\n" # TODO injection latex
        latex += implem.implementation.get_code_tex()

    # end
    latex += r"""
%\end{multicols}
\end{document}
"""
    return latex
