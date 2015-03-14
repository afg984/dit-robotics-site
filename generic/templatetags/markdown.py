from django import template
from django.utils.html import mark_safe
from markdown import markdown as markdown_function

register = template.Library()

@register.filter
def markdown(text):
    return mark_safe(markdown_function(text, safe_mode='escape'))
