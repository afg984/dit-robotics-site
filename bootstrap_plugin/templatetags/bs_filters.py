from bs4 import BeautifulSoup

from django import template
from django.utils.html import mark_safe #, conditional_escape

register = template.Library()


class IncorrectTagsSupported(Exception):
    pass


@register.filter
def bs_form_control(value):
    svalue = str(value)
    soup = BeautifulSoup(svalue, "html.parser")
    childrens = list(soup.html.body.children)
    if len(childrens) != 1:
        raise IncorrectTagsSupported(len(childrens), value)
    tag = childrens[0]
    try:
        tag.attrs['class'].append('form-control')
    except:
        tag.attrs['class'] = 'form-control'
    return mark_safe(str(tag))
