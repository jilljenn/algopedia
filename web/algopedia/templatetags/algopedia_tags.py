from django import template
from random import choice
import string

register = template.Library()

@register.inclusion_tag('algopedia/tag_checkbox_star.html', takes_context=True)
def checkbox_star(context, stars, id):
    """ Customized tag to generate a star checkbox
    stars : either a list of ids or a boolean
    id : id of the implementation
    the star is checked if the id is in stars or if stars is true
    """
    return {
      'request' : context['request'],
      'stars' : stars,
      'id' : id
    }

@register.inclusion_tag('algopedia/tag_implementation_descr.html', takes_context=True)
def implementation_descr(context, implem, stars):
    return {
      'request' : context['request'],
      'user' : context['user'],
      'implem' : implem,
      'stars' : stars,
    }

@register.assignment_tag()
def random_id(length=5):
    """Returns a random identifier of size [size]"""
    return ''.join(choice(string.ascii_letters + string.digits) for _ in range(length))
