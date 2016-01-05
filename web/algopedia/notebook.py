import os
from subprocess import check_call, CalledProcessError
from tempfile import TemporaryDirectory, mkstemp
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from algopedia.models import Algo, Implementation, Category, Star
from pygments.formatters import LatexFormatter

def generateTex(implementations):
    # TODO options de génération : titre, auteur, mutlicol?, linenos ?, a4paper/letter? marges? tailles, ordre des algos, sections
    context = {
      'style_defs': LatexFormatter().get_style_defs(), # pygments premise
      'title': 'Notebook',
      'author': 'Algopedia',
      'stars': implementations,
      'multicols': 1
    }
    return render_to_string('algopedia/notebook.tex', context)

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
        check_call(['pdflatex', '-no-shell-escape', '-halt-on-error', '-interaction', 'errorstopmode', texfilename]) # TODO environnement sécurisé
        # TODO catch CalledProcessError
    # Move resulting PDF
    os.rename(texfilename + '.pdf', pdffilename)
    # Remove intermediate dir
    tmp_folder.cleanup()
    return pdffilename
