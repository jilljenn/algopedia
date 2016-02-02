from django import template
from random import choice
import string

register = template.Library()

@register.inclusion_tag('algopedia/tag_checkbox_star.html', takes_context=True)
def checkbox_star(context, id):
    """ Customized tag to generate a star checkbox
    id : id of the implementation
    the star is checked if its id is in context['stars']
    """
    return {
      'request' : context['request'],
      'stars' : context.get('stars', []),
      'id' : id
    }

@register.inclusion_tag('algopedia/tag_implementation_descr.html', takes_context=True)
def implementation_descr(context, implem):
    return {
      'request' : context['request'],
      'user' : context['user'],
      'implem' : implem,
      'stars' : context.get('stars', []),
    }

@register.assignment_tag()
def random_id(length=5):
    """Returns a random identifier of size [size]"""
    return ''.join(choice(string.ascii_letters + string.digits) for _ in range(length))
