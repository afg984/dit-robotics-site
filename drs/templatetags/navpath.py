from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.filter
def isview(request, name):
    return request.path == reverse(name)
