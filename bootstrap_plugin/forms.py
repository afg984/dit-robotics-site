from django.forms.forms import BoundField

def bsCssClasses(self):
    return super(BoundField, self).css_classes('form-group')

def simpleFactory(cls):
    class BSWrapperForm(cls):
        def __init__(self, *args, **kw):
            super(cls, self).__init__(*args, **kw)
            for name, field in self.fields.items():
                self[name].css_classes = bsCssClasses
                field.widget.attrs['class'] = 'form-control'

        def as_bs(self):
            "Returns this form rendered as HTML <div>s."
            return self._html_output(
            normal_row='<div class="form-group"%(html_class_attr)s>%(label)s %(field)s%(help_text)s</div>',
            error_row='%s',
            row_ender='</div>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=False
        )
    return BSWrapperForm
