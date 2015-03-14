from django import template
from django.utils.html import format_html

register = template.Library()

# Tag With Default
@register.simple_tag
def tagwd(tag, content, default='無', mute_class='text-muted'):
    return format_html(
        '<{tag}{mute}>{content}</{tag}>',
        tag=tag,
        content=content or default,
        mute='' if content else format_html(' class="{}"', mute_class),
    )
