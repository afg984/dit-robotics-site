from django import template
from django.core.urlresolvers import reverse
from django.utils.html import format_html, mark_safe

register = template.Library()

@register.filter
def isview(request, name):
    return request.path == reverse(name)

@register.simple_tag(takes_context=True)
def nav_li(context, view, display=None):
    if display is None:
        display = view.replace('_', ' ').capitalize()
    href = reverse(view)
    return format_html(
        '<li{cls}><a href="{href}">{display}</a></li>',
        cls=mark_safe(' class="active"') if context['request'].path == href else '',
        href=href,
        display=display,
    )

@register.simple_tag(takes_context=True)
def caiv(context, view): #class="active" if view
    if context['request'].path == reverse(view):
        return mark_safe(' class="active"')
    else:
        return ''
