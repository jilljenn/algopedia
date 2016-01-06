from django import template

register = template.Library()

@register.inclusion_tag('algopedia/tag_checkbox_star.html')
def checkbox_star(stars, id):
    """ Customized tag to generate a star checkbox
    stars : either a list of ids or a boolean
    id : id of the implementation
    the star is checked if the id is in stars or if stars is true
    """
    return {
      'stars' : stars,
      'id' : id
    }
