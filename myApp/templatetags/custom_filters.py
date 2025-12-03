"""
Custom template filters for the Maria Gregory website
"""
from django import template

register = template.Library()


@register.filter
def replace(value, arg):
    """
    Replaces all occurrences of a substring in a string.
    Usage: {{ value|replace:"old:new" }}
    """
    if not value:
        return value
    
    try:
        old, new = arg.split(':')
        return value.replace(old, new)
    except (ValueError, AttributeError):
        return value


@register.filter
def to_field_name(value):
    """
    Converts a label to a valid field name (lowercase, spaces to underscores).
    Usage: {{ field.label|to_field_name }}
    """
    if not value:
        return ''
    return value.lower().replace(' ', '_').replace('-', '_')


