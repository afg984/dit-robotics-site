from django.forms.forms import BoundField

class BSBoundField(BoundField):
    def css_classes(self, extra_classes=None):
        if hasattr(extra_classes, 'split'):
            extra_classes = extra_classes.split()
        extra_classes = set(extra_classes or [])
        extra_classes.add('form-group')
        return super().css_classes(extra_classes)


def simpleFactory(cls):
    class BSWrapperForm(cls):
        def __init__(self, *args, **kw):
            super(cls, self).__init__(*args, **kw)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

        def as_bs(self):
            "Returns this form rendered as HTML <div>s."
            return self._html_output(
            normal_row='<div%(html_class_attr)s>%(label)s %(errors)s%(field)s%(help_text)s</div>',
            error_row='%s',
            row_ender='</div>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=False
            )

        def __getitem__(self, name):
            try:
                field = self.fields[name]
            except KeyError:
                raise KeyError(
                    "Key %r not found in %s" % (name, self.__class__.__name__))
            return BSBoundField(self, field, name)

    return BSWrapperForm

