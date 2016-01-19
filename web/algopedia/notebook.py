import os
from subprocess import check_call, CalledProcessError
from tempfile import TemporaryDirectory, mkstemp
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from algopedia.models import Implementation, Star
from pygments.formatters import LatexFormatter

def generateTex(implementations, params):
    # TODO options de génération : a4paper/letter? marges? tailles, ordre des algos, sections
    context = {
      'style_defs': LatexFormatter().get_style_defs(), # pygments premise
      'title': params.title,
      'author': params.author,
      'stars': implementations,
      'multicols': params.multicol,
      'linenos': params.linenos,
    }
    return render_to_string('algopedia/notebook.tex', context)

def generatePdf(implementations, params):
    """Returns the absolute pathname of the pdf file (to be deleted).
    """
    latex = generateTex(implementations, params)

    # In a temporary folder, make temporary files
    tmp_folder = TemporaryDirectory()
    texfile, texfilename = mkstemp(dir=tmp_folder.name)
    pdffile, pdffilename = mkstemp()
    os.close(pdffile) # it will be overwritten by pdflatex
    # produce and write the TeX code into the temp file
    os.write(texfile, str.encode(latex))
    os.close(texfile)
    # Compile the TeX file with PDFLaTeX
    for _ in range(3):
        check_call(['pdflatex', '-output-directory', tmp_folder.name, '-no-shell-escape', '-halt-on-error', '-interaction', 'batchmode', texfilename]) # TODO environnement sécurisé
        # TODO catch CalledProcessError
    # Move resulting PDF
    os.rename(texfilename + '.pdf', pdffilename)
    # Remove intermediate dir
    tmp_folder.cleanup()
    return pdffilename
