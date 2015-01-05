from django import forms


from . import data


class TimeFilterForm(forms.Form):
    OPERATIONS = (
        ('within', '只在勾選的時段內的課'),
        ('except', '不在勾選的時段內的課'),
    )
    operation = forms.ChoiceField(
        choices=OPERATIONS,
        initial='except',
        widget=forms.RadioSelect,
    )
    (
        time1, time2, time3, time4, timen,
        time5, time6, time7, time8, time9,
        timea, timeb, timec
    ) = [
        forms.MultipleChoiceField(
            choices=zip(*[[w + s for w in data.weekdays]]*2),
            widget=forms.CheckboxSelectMultiple,
        )
        for s in data.classsects
    ]


    @property
    def timetable(self):
        return tuple(self['time' + c] for c in data.classsects)
