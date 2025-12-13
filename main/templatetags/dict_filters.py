"""
Template filterek szótárak kezeléséhez.
"""
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Egy szótárból lekér egy értéket kulcs alapján.
    Template-ekben használható: {{ my_dict|get_item:key }}
    """
    if dictionary and key:
        return dictionary.get(key, "")
    return ""
