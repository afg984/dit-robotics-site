from django import template
from django.core.urlresolvers import reverse
from django.utils.html import format_html, mark_safe

register = template.Library()

@register.simple_tag()
def dropdown(display):
    return format_html(
        '<li class="dropdown">'
        '<a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">'
        '{} '
        '<span class="caret"></span>'
        '</a>'
        '<ul class="dropdown-menu" role="menu">',
        display
    )

@register.simple_tag()
def enddropdown():
    return mark_safe('</ul></li>')

@register.simple_tag(takes_context=True)
def navli(context, path, display, available=True):
    classes = []
    if context['request'].path == path:
        classes.append('active')
    if not available:
        classes.append('disabled')
    return format_html(
        '<li{cls}><a href="{href}">{display}</a></li>',
        cls=(
            format_html(' class="{}"'.format(' '.join(classes)))
            if classes
            else ''
        ),
        href=path,
        display=display,
    )

@register.simple_tag(takes_context=True)
def navlio(context, object_, display=None, available=True):
    if display is None:
        display = str(object_)
    return navli(context, object_.get_absolute_url(), display, available)

@register.simple_tag(takes_context=True)
def navlir(context, viewname, *args, **kwargs):
    display = kwargs.pop('display', None)
    available = kwargs.pop('available', True)
    if display is None:
        display = viewname.replace('_', ' ').capitalize()
    path = reverse(viewname, args=args, kwargs=kwargs)
    return navli(context, path, display, available)
