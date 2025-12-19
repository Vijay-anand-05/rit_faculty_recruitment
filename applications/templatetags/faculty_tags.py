from django import template

register = template.Library()

@register.filter
def count_level(items, level):
    if not items:
        return 0
    return sum(1 for i in items if getattr(i, "level", None) == level)