import os
from subprocess import check_call, CalledProcessError
from tempfile import TemporaryDirectory, mkstemp
from django.shortcuts import render, get_object_or_404
from algopedia.models import Algo, Implementation, Category, Star
from pygments.formatters import LatexFormatter

def generateTex(implementations):
    # TODO options de génération : titre, auteur, mutlicol?, linenos ?, a4paper/letter? marges? tailles, ordre des algos, sections
    # TODO utiliser un template et render_to_string
    # render_to_string('tex/notebook.tex', {'var': 'whatever'}))
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

def generatePdf(implementations):
    """Returns the absolute pathname of the pdf file (to be deleted).
    """
    latex = generateTex(implementations)

    # In a temporary folder, make temporary files
    tmp_folder = TemporaryDirectory()
    os.chdir(tmp_folder.name)
    texfile, texfilename = mkstemp(dir=tmp_folder.name)
    pdffile, pdffilename = mkstemp()
    os.close(pdffile) # it will be overwritten by pdflatex
    # produce and write the TeX code into the temp file
    os.write(texfile, str.encode(latex))
    os.close(texfile)
    # Compile the TeX file with PDFLaTeX
    for _ in range(3):
        check_call(['pdflatex', texfilename, '-no-shell-escape']) # TODO environnement sécurisé
        # TODO catch CalledProcessError
    # Move resulting PDF
    os.rename(texfilename + '.pdf', pdffilename)
    # Remove intermediate dir
    tmp_folder.cleanup()
    return pdffilename
