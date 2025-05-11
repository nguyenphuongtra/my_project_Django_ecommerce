from django import template
from django.template.defaultfilters import floatformat

register = template.Library()

@register.filter(name='vnd')
def vnd(value):
    """Format a number as Vietnamese Dong currency."""
    if value is None:
        return ''
    
    try:
        numeric_value = float(value)
        formatted_value = floatformat(numeric_value, 0)
        
        parts = []
        while formatted_value:
            if len(formatted_value) > 3:
                parts.append(formatted_value[-3:])
                formatted_value = formatted_value[:-3]
            else:
                parts.append(formatted_value)
                break
        
        parts.reverse()
        formatted_value = '.'.join(parts)
        
        return f"{formatted_value}₫"
    except (ValueError, TypeError):
        return value 