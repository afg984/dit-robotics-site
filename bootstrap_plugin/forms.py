
class FormatterForm:
    def as_div(self):
        "Returns this form rendered as HTML <div>s."
        return self._html_output(
                al_row='<div%(html_class_attr)s>%(label)s %(field)s%(help_text)s</p>',
            error_row='%s',
            row_ender='</div>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True
        )
