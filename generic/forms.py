from django import forms
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.contrib.auth.forms import ReadOnlyPasswordHashWidget


class StaticWidget(ReadOnlyPasswordHashWidget):
    def render(self, name, value, attrs):
        return format_html('<div{}>{}</div>',
            flatatt(self.build_attrs(attrs)),
            value
        )


class StaticField(forms.Field):
    widget = StaticWidget
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('required', False)
        super().__init__(*args, **kwargs)

    def bound_data(self, data, initial):
        return initial

    def _has_changed(self, initial, data):
        return False
