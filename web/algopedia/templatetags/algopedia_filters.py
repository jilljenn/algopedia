from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def latex_escape(value):
    CHARS = {
      '&':  r'\&',
      '%':  r'\%', 
      '$':  r'\$', 
      '#':  r'\#', 
      '_':  r'\_', 
      '{':  r'\{', 
      '}':  r'\}',
      '~':  r'\textasciitilde{}', 
      '^':  r'\^{}', 
      '\\': r'\textbackslash{}',
    }
    return "".join([CHARS.get(char, char) for char in value])
