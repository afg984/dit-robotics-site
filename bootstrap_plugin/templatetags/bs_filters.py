from bs4 import BeautifulSoup

from django import template
from django.utils.html import mark_safe #, conditional_escape

register = template.Library()


class IncorrectTagsSupported(Exception):
    pass


@register.filter
def add_class(value, class_):
    class_ = class_.split()
    svalue = str(value)
    soup = BeautifulSoup(svalue, "html.parser")
    childrens = list(soup.children)
    if len(childrens) != 1:
        raise IncorrectTagsSupported(len(childrens), value)
    tag = childrens[0]
    try:
        tag.attrs['class'].extend(class_)
    except KeyError:
        tag.attrs['class'] = class_
    return mark_safe(str(tag))

@register.filter
def bs_form_control(value):
    return add_class(value, 'form-control')
