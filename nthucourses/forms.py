from django import forms


from . import data


class CourseFilterForm(forms.Form):
    OPERATIONS = (
        ('within', '只在勾選的時段內的課'),
        ('except', '不在勾選的時段內的課'),
    )
    operation = forms.ChoiceField(
        choices=OPERATIONS,
        initial='except',
        widget=forms.RadioSelect,
    )
    times = forms.MultipleChoiceField(
        choices=zip(*[data.times]*2),
        widget=forms.CheckboxSelectMultiple,
    )


    @property
    def timetable(self):
        return [
            [
                self['times'][x * len(data.classsects) + y]
                for x in range(len(data.weekdays))
            ]
            for y in range(len(data.classsects))
        ]

    @property
    def selected_times(self):
        return self.cleaned_data.get('times', [])
