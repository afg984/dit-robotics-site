from bs4 import BeautifulSoup

from django import template
from django.utils.html import mark_safe #, conditional_escape

register = template.Library()


class IncorrectTagsSupported(Exception):
    pass


def get_one_tag(s):
    soup = BeautifulSoup(str(s), 'html.parser')
    childrens = list(soup.children)
    if len(childrens) != 1:
        raise IncorrectTagsSupported(len(childrens), s)
    return childrens[0]


@register.filter
def settagattr(value, s):
    attr, data = s.split('=')
    tag = get_one_tag(value)
    tag.attrs[attr] = data
    return mark_safe(str(tag))


@register.filter
def add_class(value, class_):
    class_ = class_.split()
    tag = get_one_tag(value)
    try:
        tag.attrs['class'].extend(class_)
    except KeyError:
        tag.attrs['class'] = class_
    return mark_safe(str(tag))


@register.filter
def bs_form_control(value):
    return add_class(value, 'form-control')


@register.filter
def map_message_level(value):
    return {
        10: 'debug',
        20: 'info',
        25: 'success',
        30: 'warning',
        40: 'debug',
    }.get(value, value)
